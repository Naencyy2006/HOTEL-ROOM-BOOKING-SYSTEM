# views/receptionist.py
# User interface module for Receptionist operations

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.receptionist_service import ReceptionistService
from database import db

class ReceptionistView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HOTEL MANAGEMENT SYSTEM - RECEPTIONIST PANEL")
        self.geometry("1050x680")
        self.minsize(950, 600)

        # Initialize service instance for business logic processing
        self.service = ReceptionistService()
        self.room_types_map = {}  # Mapping display string to room_type_id

        # Configure Theme and Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # Create Notebook container for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize Tabs
        self.tab_reservations = ttk.Frame(self.notebook)
        self.tab_walkin = ttk.Frame(self.notebook)
        self.tab_checkin_checkout = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_reservations, text=" 📋 Reservation List ")
        self.notebook.add(self.tab_walkin, text=" ➕ Walk-in Booking ")
        self.notebook.add(self.tab_checkin_checkout, text=" 🔑 Check-in / Check-out ")

        # Build UI layout for each Tab
        self._build_reservations_tab()
        self._build_walkin_tab()
        self._build_checkin_checkout_tab()

        # Load initial data
        self.load_room_types()
        self.load_reservations()

    def _configure_styles(self):
        """Configure font styles and widget themes"""
        self.style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[12, 6])
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#1E3A8A")
        self.style.configure("SubHeader.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#1E3A8A")
        self.style.configure("Treeview.Heading", font=("Arial", 9, "bold"), background="#E5E7EB")
        self.style.configure("Treeview", rowheight=26)

    def load_room_types(self):
        """Fetch available room types to populate the room type dropdown list"""
        connection = db.get_connection()
        if not connection:
            return

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT room_type_id, type_name, price_per_night FROM room_types")
            room_types = cursor.fetchall()
            
            self.room_types_map.clear()
            combobox_values = []
            
            for rt in room_types:
                display_str = f"ID {rt['room_type_id']} - {rt['type_name']} ({rt['price_per_night']:,.0f} VND)"
                self.room_types_map[display_str] = rt['room_type_id']
                combobox_values.append(display_str)

            self.cbo_w_roomtype['values'] = combobox_values
            if combobox_values:
                self.cbo_w_roomtype.current(0)
        except Exception as e:
            print(f"Error loading room types: {e}")
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # TAB 1: RESERVATIONS LIST
    # ==========================================
    def _build_reservations_tab(self):
        # Search / Filter Panel
        filter_frame = ttk.LabelFrame(self.tab_reservations, text=" Search & Filter ", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="Status:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cbo_filter_status = ttk.Combobox(
            filter_frame, 
            values=["All", "Pending Payment", "Confirmed", "Checked-in", "Completed", "Canceled"],
            state="readonly", width=15
        )
        self.cbo_filter_status.current(0)
        self.cbo_filter_status.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Guest Name:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.txt_filter_name = ttk.Entry(filter_frame, width=20)
        self.txt_filter_name.grid(row=0, column=3, padx=5, pady=5)

        btn_search = ttk.Button(filter_frame, text="Search", command=self.load_reservations)
        btn_search.grid(row=0, column=4, padx=10, pady=5)

        btn_refresh = ttk.Button(filter_frame, text="Reset", command=self.reset_reservation_filters)
        btn_refresh.grid(row=0, column=5, padx=5, pady=5)

        # Table View (Treeview)
        table_frame = ttk.Frame(self.tab_reservations, padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("booking_id", "full_name", "phone", "room_id", "type_name", "check_in", "check_out", "total_price", "status")
        self.tree_reservations = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Table Headers Configuration
        headers = {
            "booking_id": "Booking ID",
            "full_name": "Guest Name",
            "phone": "Phone Number",
            "room_id": "Room",
            "type_name": "Room Type",
            "check_in": "Check-in Date",
            "check_out": "Check-out Date",
            "total_price": "Total (VND)",
            "status": "Status"
        }
        widths = [80, 150, 100, 70, 120, 100, 100, 110, 100]

        for col, width in zip(columns, widths):
            self.tree_reservations.heading(col, text=headers[col])
            self.tree_reservations.column(col, width=width, anchor=tk.CENTER if col in ["booking_id", "room_id", "status"] else tk.W)

        # Bind event on selection
        self.tree_reservations.bind("<<TreeviewSelect>>", self._on_reservation_selected)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_reservations.yview)
        self.tree_reservations.configure(yscroll=scrollbar.set)
        
        self.tree_reservations.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_reservations(self):
        """Fetch and display reservation records on the Treeview widget"""
        for item in self.tree_reservations.get_children():
            self.tree_reservations.delete(item)

        status = self.cbo_filter_status.get()
        filter_status = None if status == "All" else status
        guest_name = self.txt_filter_name.get().strip() or None

        reservations = self.service.view_reservations(filter_status=filter_status, guest_name=guest_name)

        for r in reservations:
            room_str = r['room_id'] if r['room_id'] else "Unassigned"
            formatted_price = f"{r['total_price']:,.0f}" if r['total_price'] else "0"
            self.tree_reservations.insert("", tk.END, values=(
                r['booking_id'], r['full_name'], r['phone'], room_str,
                r['type_name'], str(r['check_in']), str(r['check_out']),
                formatted_price, r['status']
            ))

    def reset_reservation_filters(self):
        """Reset search filters and refresh table"""
        self.cbo_filter_status.current(0)
        self.txt_filter_name.delete(0, tk.END)
        self.load_reservations()

    def _on_reservation_selected(self, event):
        """Auto fill Booking ID into Check-in/Check-out inputs when selected"""
        selected_item = self.tree_reservations.selection()
        if selected_item:
            values = self.tree_reservations.item(selected_item[0], "values")
            booking_id = values[0]
            
            # Fill into Check-in / Check-out entries
            self.txt_ci_booking_id.delete(0, tk.END)
            self.txt_ci_booking_id.insert(0, booking_id)

            self.txt_co_booking_id.delete(0, tk.END)
            self.txt_co_booking_id.insert(0, booking_id)

    # ==========================================
    # TAB 2: WALK-IN BOOKING
    # ==========================================
    def _build_walkin_tab(self):
        container = ttk.Frame(self.tab_walkin, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Guest Details Section
        guest_frame = ttk.LabelFrame(container, text=" Guest Details ", padding=15, style="SubHeader.TLabelframe")
        guest_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(guest_frame, text="Full Name (*):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_w_fullname = ttk.Entry(guest_frame, width=30)
        self.txt_w_fullname.grid(row=0, column=1, pady=5)

        ttk.Label(guest_frame, text="Email (*):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.txt_w_email = ttk.Entry(guest_frame, width=30)
        self.txt_w_email.grid(row=1, column=1, pady=5)

        ttk.Label(guest_frame, text="Phone Number (*):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_w_phone = ttk.Entry(guest_frame, width=30)
        self.txt_w_phone.grid(row=2, column=1, pady=5)

        ttk.Label(guest_frame, text="Gender:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cbo_w_gender = ttk.Combobox(guest_frame, values=["Male", "Female", "Other"], state="readonly", width=28)
        self.cbo_w_gender.current(0)
        self.cbo_w_gender.grid(row=3, column=1, pady=5)

        ttk.Label(guest_frame, text="Year of Birth (*):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.txt_w_yob = ttk.Entry(guest_frame, width=30)
        self.txt_w_yob.grid(row=4, column=1, pady=5)

        # Booking & Payment Details Section
        booking_frame = ttk.LabelFrame(container, text=" Room & Payment Details ", padding=15, style="SubHeader.TLabelframe")
        booking_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(booking_frame, text="Room Type (*):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cbo_w_roomtype = ttk.Combobox(booking_frame, state="readonly", width=28)
        self.cbo_w_roomtype.grid(row=0, column=1, pady=5)

        ttk.Label(booking_frame, text="Room Number (Optional):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.txt_w_roomid = ttk.Entry(booking_frame, width=30)
        self.txt_w_roomid.grid(row=1, column=1, pady=5)

        ttk.Label(booking_frame, text="Check-in Date (YYYY-MM-DD) (*):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_w_checkin = ttk.Entry(booking_frame, width=30)
        self.txt_w_checkin.grid(row=2, column=1, pady=5)

        ttk.Label(booking_frame, text="Check-out Date (YYYY-MM-DD) (*):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.txt_w_checkout = ttk.Entry(booking_frame, width=30)
        self.txt_w_checkout.grid(row=3, column=1, pady=5)

        ttk.Label(booking_frame, text="Total Price (Optional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.txt_w_price = ttk.Entry(booking_frame, width=30)
        self.txt_w_price.grid(row=4, column=1, pady=5)

        ttk.Label(booking_frame, text="Payment Method:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.cbo_w_payment = ttk.Combobox(booking_frame, values=["Cash", "Card", "Transfer"], state="readonly", width=28)
        self.cbo_w_payment.current(0)
        self.cbo_w_payment.grid(row=5, column=1, pady=5)

        # Submit Button
        btn_submit = ttk.Button(container, text="Create Walk-in Booking", command=self.handle_walkin_booking)
        btn_submit.grid(row=1, column=0, columnspan=2, pady=20, ipadx=20, ipady=5)

    def handle_walkin_booking(self):
        """Handle submission for Walk-in guest booking creation with strict input validation"""
        full_name = self.txt_w_fullname.get().strip()
        email = self.txt_w_email.get().strip()
        phone = self.txt_w_phone.get().strip()
        raw_yob = self.txt_w_yob.get().strip()
        selected_rt_text = self.cbo_w_roomtype.get()
        check_in = self.txt_w_checkin.get().strip()
        check_out = self.txt_w_checkout.get().strip()
        raw_price = self.txt_w_price.get().strip()

        if not all([full_name, email, phone, raw_yob, selected_rt_text, check_in, check_out]):
            messagebox.showwarning("Validation Warning", "Please fill in all mandatory fields (*).")
            return

        try:
            d_checkin = datetime.strptime(check_in, "%Y-%m-%d").date()
            d_checkout = datetime.strptime(check_out, "%Y-%m-%d").date()

            if d_checkout <= d_checkin:
                messagebox.showwarning("Validation Warning", "Check-out date must be after Check-in date.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Dates must follow the YYYY-MM-DD format (e.g., 2026-09-08).")
            return

        try:
            year_of_birth = int(raw_yob)
            room_type_id = self.room_types_map.get(selected_rt_text)
            total_price = float(raw_price) if raw_price else None
            gender = self.cbo_w_gender.get()
            room_id = self.txt_w_roomid.get().strip() or None
            payment_method = self.cbo_w_payment.get()

            # Call Service layer
            success, message = self.service.create_walkin_booking(
                full_name, email, phone, gender, year_of_birth,
                room_type_id, room_id, check_in, check_out, total_price, payment_method
            )

            if success:
                messagebox.showinfo("Success", message)
                self.load_reservations()
                self._clear_walkin_inputs()
                self.notebook.select(self.tab_reservations)
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Input Error", "Year of Birth and Total Price must be valid numeric values!")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {e}")

    def _clear_walkin_inputs(self):
        """Reset walk-in form input fields"""
        self.txt_w_fullname.delete(0, tk.END)
        self.txt_w_email.delete(0, tk.END)
        self.txt_w_phone.delete(0, tk.END)
        self.txt_w_yob.delete(0, tk.END)
        self.txt_w_roomid.delete(0, tk.END)
        self.txt_w_checkin.delete(0, tk.END)
        self.txt_w_checkout.delete(0, tk.END)
        self.txt_w_price.delete(0, tk.END)

    # ==========================================
    # TAB 3: CHECK-IN & CHECK-OUT
    # ==========================================
    def _build_checkin_checkout_tab(self):
        container = ttk.Frame(self.tab_checkin_checkout, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # --- Check-in Operations Frame ---
        ci_frame = ttk.LabelFrame(container, text=" Process Check-in ", padding=20, style="SubHeader.TLabelframe")
        ci_frame.pack(fill=tk.X, pady=10)

        ttk.Label(ci_frame, text="Booking ID (*):").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.txt_ci_booking_id = ttk.Entry(ci_frame, width=20)
        self.txt_ci_booking_id.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(ci_frame, text="Room Number (Leave blank to keep pre-assigned room):").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.txt_ci_room_number = ttk.Entry(ci_frame, width=20)
        self.txt_ci_room_number.grid(row=1, column=1, pady=5, padx=5)

        btn_ci = ttk.Button(ci_frame, text="Process Check-in", command=self.handle_check_in)
        btn_ci.grid(row=2, column=0, columnspan=2, pady=15)

        # --- Check-out Operations Frame ---
        co_frame = ttk.LabelFrame(container, text=" Process Check-out ", padding=20, style="SubHeader.TLabelframe")
        co_frame.pack(fill=tk.X, pady=10)

        ttk.Label(co_frame, text="Booking ID (*):").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.txt_co_booking_id = ttk.Entry(co_frame, width=20)
        self.txt_co_booking_id.grid(row=0, column=1, pady=5, padx=5)

        btn_co = ttk.Button(co_frame, text="Process Check-out", command=self.handle_check_out)
        btn_co.grid(row=1, column=0, columnspan=2, pady=15)

    def handle_check_in(self):
        """Process check-in operation"""
        try:
            booking_id_str = self.txt_ci_booking_id.get().strip()
            if not booking_id_str:
                messagebox.showwarning("Validation Warning", "Please enter a Booking ID.")
                return

            booking_id = int(booking_id_str)
            room_number = self.txt_ci_room_number.get().strip() or None

            success, message = self.service.process_check_in(booking_id, room_number)
            if success:
                messagebox.showinfo("Success", message)
                self.txt_ci_booking_id.delete(0, tk.END)
                self.txt_ci_room_number.delete(0, tk.END)
                self.load_reservations()
                self.notebook.select(self.tab_reservations)
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Input Error", "Booking ID must be a valid integer!")

    def handle_check_out(self):
        """Process check-out operation"""
        try:
            booking_id_str = self.txt_co_booking_id.get().strip()
            if not booking_id_str:
                messagebox.showwarning("Validation Warning", "Please enter a Booking ID.")
                return

            booking_id = int(booking_id_str)

            if messagebox.askyesno("Confirmation", f"Are you sure you want to check out Booking #{booking_id}?"):
                success, message = self.service.process_check_out(booking_id)
                if success:
                    messagebox.showinfo("Success", message)
                    self.txt_co_booking_id.delete(0, tk.END)
                    self.load_reservations()
                    self.notebook.select(self.tab_reservations)
                else:
                    messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Input Error", "Booking ID must be a valid integer!")

    def run(self):
        """Start the Tkinter GUI main event loop"""
        self.mainloop()

# Standalone execution for GUI testing
if __name__ == "__main__":
    app = ReceptionistView()
    app.run()
