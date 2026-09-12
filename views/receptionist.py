# views/receptionist.py
# User interface module for Receptionist operations with Pastel Purple Theme

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.receptionist_service import ReceptionistService
from config.database import db

# ==========================================
# CONSTANTS: COLOR PALETTE & TYPOGRAPHY
# ==========================================
COLOR_MAIN_BG = "#F5EFFF"   # Nền chính
COLOR_SIDEBAR = "#E5D9F2"   # Nền card / panel
COLOR_BUTTON  = "#CDC1FF"   # Nút phụ
COLOR_ACCENT  = "#A594F9"   # Nút chính / Header
COLOR_TEXT    = "#3B2F63"   # Chữ tối
COLOR_WHITE   = "#FFFFFF"

FONT_TITLE  = ("Arial", 16, "bold")
FONT_HEADER = ("Arial", 11, "bold")
FONT_BOLD   = ("Arial", 9, "bold")
FONT_NORMAL = ("Arial", 9)


class ReceptionistView(tk.Tk):
    def __init__(self, on_logout=None):
        super().__init__()
        self.on_logout = on_logout

        self.title("HOTEL MANAGEMENT SYSTEM - RECEPTIONIST PANEL")
        self.geometry("1100x750")
        self.minsize(1000, 680)

        self.configure(bg=COLOR_MAIN_BG)

        # Initialize service instance
        self.service = ReceptionistService()
        self.room_types_map = {}
        self.room_type_prices = {}
        self.cio_search_results = []  # Lưu kết quả tìm kiếm cho Checkin/Checkout

        # Configure Theme and Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # --- Top Header Banner ---
        self._build_header_banner()

        # Create Notebook container for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))

        # Initialize Tabs
        self.tab_reservations = ttk.Frame(self.notebook, style="MainTab.TFrame")
        self.tab_walkin = ttk.Frame(self.notebook, style="MainTab.TFrame")
        self.tab_checkin_checkout = ttk.Frame(self.notebook, style="MainTab.TFrame")

        self.notebook.add(self.tab_reservations, text=" 📋 Reservations ")
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
        """Cấu hình style giao diện theo bộ màu Pastel Lavender"""
        # Form Container Styles
        self.style.configure("MainTab.TFrame", background=COLOR_MAIN_BG)
        self.style.configure("Card.TFrame", background=COLOR_SIDEBAR, relief="flat")
        
        # Notebook Tab Style
        self.style.configure(
            "TNotebook", 
            background=COLOR_MAIN_BG, 
            borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab", 
            font=FONT_HEADER, 
            padding=[16, 8], 
            background=COLOR_SIDEBAR, 
            foreground=COLOR_TEXT
        )
        self.style.map(
            "TNotebook.Tab", 
            background=[("selected", COLOR_ACCENT)], 
            foreground=[("selected", COLOR_WHITE)]
        )

        # LabelFrame Style
        self.style.configure(
            "TLabelframe", 
            background=COLOR_SIDEBAR, 
            borderwidth=1, 
            relief="solid",
            darkcolor=COLOR_ACCENT,
            lightcolor=COLOR_ACCENT
        )
        self.style.configure(
            "TLabelframe.Label", 
            font=FONT_HEADER, 
            foreground=COLOR_TEXT, 
            background=COLOR_SIDEBAR
        )

        # Labels & Inputs
        self.style.configure("TLabel", background=COLOR_SIDEBAR, font=FONT_NORMAL, foreground=COLOR_TEXT)
        self.style.configure("TEntry", padding=5, font=FONT_NORMAL)
        self.style.configure("TCombobox", padding=4, font=FONT_NORMAL)

        # Treeview (Table) Style
        self.style.configure(
            "Treeview.Heading", 
            font=FONT_HEADER, 
            background=COLOR_SIDEBAR, 
            foreground=COLOR_TEXT, 
            relief="flat"
        )
        self.style.configure(
            "Treeview", 
            font=FONT_NORMAL, 
            rowheight=32, 
            background=COLOR_WHITE, 
            fieldbackground=COLOR_WHITE, 
            borderwidth=0
        )
        self.style.map("Treeview", background=[("selected", COLOR_ACCENT)], foreground=[("selected", COLOR_WHITE)])

        # Custom Buttons
        self.style.configure(
            "Primary.TButton", 
            font=FONT_BOLD, 
            background=COLOR_ACCENT, 
            foreground=COLOR_WHITE,
            borderwidth=0
        )
        self.style.map("Primary.TButton", background=[("active", "#8B77E8")])

        self.style.configure(
            "Secondary.TButton", 
            font=FONT_BOLD, 
            background=COLOR_BUTTON, 
            foreground=COLOR_TEXT,
            borderwidth=0
        )
        self.style.map("Secondary.TButton", background=[("active", "#B7A8F5")])

    def _build_header_banner(self):
        """Header Banner với tông màu Accent tím pastel"""
        header_frame = tk.Frame(self, bg=COLOR_ACCENT, height=65)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        lbl_title = tk.Label(
            header_frame, 
            text="HOTEL MANAGEMENT SYSTEM — RECEPTIONIST DESK", 
            font=FONT_TITLE, 
            fg=COLOR_WHITE, 
            bg=COLOR_ACCENT
        )
        lbl_title.pack(side=tk.LEFT, padx=20, pady=16)

        btn_logout = tk.Button(
            header_frame,
            text="Log Out",
            command=self._logout,
            bg=COLOR_BUTTON,
            fg=COLOR_TEXT,
            font=FONT_BOLD,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5,
        )
        btn_logout.pack(side=tk.RIGHT, padx=20, pady=15)

    def _logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?", parent=self):
            self.destroy()
            if self.on_logout:
                self.on_logout()

    def load_room_types(self):
        """Fetch available room types to populate the room type dropdown list"""
        connection = db.get_connection()
        if not connection:
            return

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT room_type_id, type_name, price_per_night, capacity FROM room_types")
            room_types = cursor.fetchall()
            
            self.room_types_map.clear()
            self.room_type_prices.clear()
            combobox_values = []
            
            for rt in room_types:
                display_str = f"ID {rt['room_type_id']} - {rt['type_name']} ({rt['price_per_night']:,.0f} VND)"
                self.room_types_map[display_str] = rt['room_type_id']
                self.room_type_prices[display_str] = float(rt['price_per_night'])
                combobox_values.append(display_str)

            self.cbo_w_roomtype['values'] = combobox_values
            if combobox_values:
                self.cbo_w_roomtype.current(0)
                self._refresh_walkin_rooms()
        except Exception as e:
            print(f"Error loading room types: {e}")
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # TAB 1: RESERVATIONS LIST
    # ==========================================
    def _build_reservations_tab(self):
        filter_frame = ttk.LabelFrame(self.tab_reservations, text=" Search & Filter ", padding=12)
        filter_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(filter_frame, text="Status:").grid(row=0, column=0, padx=(5, 2), pady=5, sticky=tk.W)
        self.cbo_filter_status = ttk.Combobox(
            filter_frame, 
            values=["All", "Pending Payment", "Confirmed", "Checked-in", "Completed", "Cancelled"],
            state="readonly", width=16
        )
        self.cbo_filter_status.current(0)
        self.cbo_filter_status.grid(row=0, column=1, padx=(0, 15), pady=5)

        ttk.Label(filter_frame, text="Guest Name:").grid(row=0, column=2, padx=(5, 2), pady=5, sticky=tk.W)
        self.txt_filter_name = ttk.Entry(filter_frame, width=22)
        self.txt_filter_name.grid(row=0, column=3, padx=(0, 15), pady=5)

        btn_search = ttk.Button(filter_frame, text="🔍 Search", style="Primary.TButton", command=self.load_reservations)
        btn_search.grid(row=0, column=4, padx=5, pady=5)

        btn_refresh = ttk.Button(filter_frame, text="🔄 Reset", style="Secondary.TButton", command=self.reset_reservation_filters)
        btn_refresh.grid(row=0, column=5, padx=5, pady=5)

        # Table View (Treeview)
        table_frame = ttk.Frame(self.tab_reservations, padding=10, style="MainTab.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("booking_id", "full_name", "phone", "room_id", "type_name", "check_in", "check_out", "total_price", "status")
        self.tree_reservations = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Dynamic Status Highlight Colors
        self.tree_reservations.tag_configure("Pending Payment", background="#FEF08A", foreground="#713F12")
        self.tree_reservations.tag_configure("Confirmed", background="#BBF7D0", foreground="#14532D")
        self.tree_reservations.tag_configure("Checked-in", background="#BFDBFE", foreground="#1E3A8A")
        self.tree_reservations.tag_configure("Completed", background="#E2E8F0", foreground="#334155")
        self.tree_reservations.tag_configure("Cancelled", background="#FECDD3", foreground="#881337")

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
        widths = [90, 160, 110, 80, 130, 110, 110, 120, 120]

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
            status_val = r['status']

            self.tree_reservations.insert(
                "", tk.END, 
                values=(
                    r['booking_id'], r['full_name'], r['phone'], room_str,
                    r['type_name'], str(r['check_in']), str(r['check_out']),
                    formatted_price, status_val
                ),
                tags=(status_val,)
            )

    def reset_reservation_filters(self):
        """Reset search filters and refresh table"""
        self.cbo_filter_status.current(0)
        self.txt_filter_name.delete(0, tk.END)
        self.load_reservations()

    def _on_reservation_selected(self, event):
        """Tự động điền thông tin sang tab Check-in/Check-out khi chọn dòng trong bảng"""
        selected_item = self.tree_reservations.selection()
        if selected_item:
            values = self.tree_reservations.item(selected_item[0], "values")
            guest_name = values[1]
            phone = values[2]
            
            # Điền tên/sđt vào ô tra cứu ở Tab 3 và tự động tra cứu
            self.txt_cio_keyword.delete(0, tk.END)
            self.txt_cio_keyword.insert(0, phone if phone else guest_name)
            self.search_cio_booking()

    # ==========================================
    # TAB 2: WALK-IN BOOKING
    # ==========================================
    def _build_walkin_tab(self):
        container = ttk.Frame(self.tab_walkin, padding=15, style="MainTab.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        guest_frame = ttk.LabelFrame(container, text=" Guest Details ", padding=15)
        guest_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(guest_frame, text="Full Name (*):").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.txt_w_fullname = ttk.Entry(guest_frame, width=28)
        self.txt_w_fullname.grid(row=0, column=1, pady=8, padx=(10, 0))

        ttk.Label(guest_frame, text="Email (*):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.txt_w_email = ttk.Entry(guest_frame, width=28)
        self.txt_w_email.grid(row=1, column=1, pady=8, padx=(10, 0))

        ttk.Label(guest_frame, text="Phone Number (*):").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.txt_w_phone = ttk.Entry(guest_frame, width=28)
        self.txt_w_phone.grid(row=2, column=1, pady=8, padx=(10, 0))

        ttk.Label(guest_frame, text="Gender:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.cbo_w_gender = ttk.Combobox(guest_frame, values=["Male", "Female", "Other"], state="readonly", width=26)
        self.cbo_w_gender.current(0)
        self.cbo_w_gender.grid(row=3, column=1, pady=8, padx=(10, 0))

        ttk.Label(guest_frame, text="Year of Birth (*):").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.txt_w_yob = ttk.Entry(guest_frame, width=28)
        self.txt_w_yob.grid(row=4, column=1, pady=8, padx=(10, 0))

        booking_frame = ttk.LabelFrame(container, text=" Room & Payment Details ", padding=15)
        booking_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(booking_frame, text="Room Type (*):").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.cbo_w_roomtype = ttk.Combobox(booking_frame, state="readonly", width=26)
        self.cbo_w_roomtype.grid(row=0, column=1, pady=8, padx=(10, 0))

        ttk.Label(booking_frame, text="Room Number (*):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.cbo_w_roomid = ttk.Combobox(booking_frame, state="readonly", width=26)
        self.cbo_w_roomid.grid(row=1, column=1, pady=8, padx=(10, 0))

        ttk.Label(booking_frame, text="Check-in Date (*):").grid(row=2, column=0, sticky=tk.W, pady=8)
        self._build_walkin_date_selector(booking_frame, "checkin", row=2, selected_date=date.today())

        ttk.Label(booking_frame, text="Check-out Date (*):").grid(row=3, column=0, sticky=tk.W, pady=8)
        self._build_walkin_date_selector(
            booking_frame, "checkout", row=3, selected_date=date.today() + timedelta(days=1)
        )

        ttk.Label(booking_frame, text="Total Price:").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.txt_w_price = ttk.Entry(booking_frame, width=28, state="readonly")
        self.txt_w_price.grid(row=4, column=1, pady=8, padx=(10, 0))

        ttk.Label(booking_frame, text="Payment Method:").grid(row=5, column=0, sticky=tk.W, pady=8)
        self.cbo_w_payment = ttk.Combobox(booking_frame, values=["Cash", "Card", "Transfer"], state="readonly", width=26)
        self.cbo_w_payment.current(0)
        self.cbo_w_payment.grid(row=5, column=1, pady=8, padx=(10, 0))

        self.cbo_w_roomtype.bind("<<ComboboxSelected>>", lambda _event: self._refresh_walkin_rooms())

        btn_submit = ttk.Button(container, text="➕ Create Walk-in Booking", style="Primary.TButton", command=self.handle_walkin_booking)
        btn_submit.grid(row=1, column=0, columnspan=2, pady=15, ipadx=25, ipady=6)

    def _build_walkin_date_selector(self, parent, prefix, row, selected_date):
        date_frame = ttk.Frame(parent)
        date_frame.grid(row=row, column=1, pady=8, padx=(10, 0), sticky=tk.W)

        year_values = [str(year) for year in range(date.today().year, date.today().year + 3)]
        selectors = {
            "day": ("Day", [f"{day:02d}" for day in range(1, 32)], f"{selected_date.day:02d}"),
            "month": ("Month", [f"{month:02d}" for month in range(1, 13)], f"{selected_date.month:02d}"),
            "year": ("Year", year_values, str(selected_date.year)),
        }
        self.walkin_date_selectors = getattr(self, "walkin_date_selectors", {})
        self.walkin_date_selectors[prefix] = {}

        for index, (part, (label, values, selected)) in enumerate(selectors.items()):
            ttk.Label(date_frame, text=label).grid(row=0, column=index * 2, padx=(0 if index == 0 else 5, 2))
            combo = ttk.Combobox(date_frame, values=values, state="readonly", width=5 if part != "year" else 7)
            combo.set(selected)
            combo.grid(row=0, column=index * 2 + 1)
            combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_walkin_rooms())
            self.walkin_date_selectors[prefix][part] = combo

    def _get_walkin_date(self, prefix):
        selectors = self.walkin_date_selectors[prefix]
        try:
            return date(
                int(selectors["year"].get()),
                int(selectors["month"].get()),
                int(selectors["day"].get()),
            ).isoformat()
        except (TypeError, ValueError):
            return ""

    def _update_walkin_total_price(self):
        """Calculate the walk-in total from selected room type and stay dates."""
        room_type_text = self.cbo_w_roomtype.get()
        price_per_night = self.room_type_prices.get(room_type_text)
        check_in = self._get_walkin_date("checkin")
        check_out = self._get_walkin_date("checkout")
        total = ""

        if price_per_night and check_in and check_out:
            try:
                nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
                if nights > 0:
                    total = f"{nights * price_per_night:,.0f}"
            except ValueError:
                pass

        self.txt_w_price.configure(state="normal")
        self.txt_w_price.delete(0, tk.END)
        self.txt_w_price.insert(0, total)
        self.txt_w_price.configure(state="readonly")

    def _refresh_walkin_rooms(self, show_message=False):
        """Refresh room choices and automatically select the first available room."""
        self._update_walkin_total_price()
        room_type_text = self.cbo_w_roomtype.get()
        check_in = self._get_walkin_date("checkin")
        check_out = self._get_walkin_date("checkout")
        room_values = []

        if room_type_text and check_in and check_out:
            try:
                d_checkin = datetime.strptime(check_in, "%Y-%m-%d").date()
                d_checkout = datetime.strptime(check_out, "%Y-%m-%d").date()
                if d_checkout > d_checkin:
                    room_type_id = self.room_types_map.get(room_type_text)
                    rooms = self.service.get_available_rooms(room_type_id, d_checkin, d_checkout)
                    room_values = [str(room["room_number"]) for room in rooms]
            except ValueError:
                pass

        self.cbo_w_roomid["values"] = room_values
        if room_values:
            self.cbo_w_roomid.current(0)
        else:
            self.cbo_w_roomid.set("")
            if show_message and room_type_text and check_in and check_out:
                messagebox.showwarning(
                    "No rooms available",
                    f"There are no available rooms for {room_type_text} in the selected dates.",
                    parent=self,
                )

    def handle_walkin_booking(self):
        """Handle submission for Walk-in guest booking creation with strict input validation"""
        full_name = self.txt_w_fullname.get().strip()
        email = self.txt_w_email.get().strip()
        phone = self.txt_w_phone.get().strip()
        raw_yob = self.txt_w_yob.get().strip()
        selected_rt_text = self.cbo_w_roomtype.get()
        check_in = self._get_walkin_date("checkin")
        check_out = self._get_walkin_date("checkout")
        raw_price = self.txt_w_price.get().strip()

        if not all([full_name, email, phone, raw_yob, selected_rt_text, check_in, check_out]):
            messagebox.showwarning("Warning", "Please fill in all required fields (*).")
            return

        try:
            d_checkin = datetime.strptime(check_in, "%Y-%m-%d").date()
            d_checkout = datetime.strptime(check_out, "%Y-%m-%d").date()

            if d_checkout <= d_checkin:
                messagebox.showwarning("Warning", "Check-out date must be after check-in date.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Dates must use the YYYY-MM-DD format (for example, 2026-09-08).")
            return

        try:
            year_of_birth = int(raw_yob)
            room_type_id = self.room_types_map.get(selected_rt_text)
            if room_type_id is None:
                messagebox.showwarning("Warning", "Please select a valid room type.")
                return
            total_price = float(raw_price.replace(",", "")) if raw_price else None
            gender = self.cbo_w_gender.get()
            room_id = self.cbo_w_roomid.get().strip() or None
            payment_method = self.cbo_w_payment.get()

            if not payment_method:
                messagebox.showwarning("Warning", "Please select a payment method.")
                return
            if not room_id:
                self._refresh_walkin_rooms(show_message=True)
                return

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
            messagebox.showerror("Input Error", "Year of birth and total price must be valid numbers!")
        except Exception as e:
            messagebox.showerror("System Error", f"An error occurred: {e}")

    def _clear_walkin_inputs(self):
        """Reset walk-in form input fields"""
        self.txt_w_fullname.delete(0, tk.END)
        self.txt_w_email.delete(0, tk.END)
        self.txt_w_phone.delete(0, tk.END)
        self.txt_w_yob.delete(0, tk.END)
        self.cbo_w_roomid.set("")
        self.cbo_w_roomid["values"] = []
        today = date.today()
        tomorrow = today + timedelta(days=1)
        for prefix, selected_date in (("checkin", today), ("checkout", tomorrow)):
            selectors = self.walkin_date_selectors[prefix]
            selectors["day"].set(f"{selected_date.day:02d}")
            selectors["month"].set(f"{selected_date.month:02d}")
            selectors["year"].set(str(selected_date.year))
        self.txt_w_price.configure(state="normal")
        self.txt_w_price.delete(0, tk.END)
        self.txt_w_price.configure(state="readonly")

    # ==========================================
    # TAB 3: CHECK-IN & CHECK-OUT (TRA CỨU TÊN/SĐỘ)
    # ==========================================
    def _build_checkin_checkout_tab(self):
        container = ttk.Frame(self.tab_checkin_checkout, padding=20, style="MainTab.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        # --- Section 1: Tìm kiếm Khách hàng (Search Frame) ---
        search_frame = ttk.LabelFrame(container, text=" 🔎 Find a Booking ", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_frame, text="Enter guest name or phone:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.txt_cio_keyword = ttk.Entry(search_frame, width=30)
        self.txt_cio_keyword.grid(row=0, column=1, padx=10, pady=5)
        self.txt_cio_keyword.bind("<Return>", lambda event: self.search_cio_booking())

        btn_search_cio = ttk.Button(search_frame, text="🔍 Find Booking", style="Primary.TButton", command=self.search_cio_booking)
        btn_search_cio.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(search_frame, text="Booking found:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cbo_cio_results = ttk.Combobox(search_frame, state="readonly", width=45)
        self.cbo_cio_results.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)
        self.cbo_cio_results.bind("<<ComboboxSelected>>", self._on_cio_booking_selected)

        # --- Section 2: Hiển thị Chi tiết phòng & Khách hàng (Info Display Frame) ---
        info_frame = ttk.LabelFrame(container, text=" 📋 Booking Details ", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)

        # Hàng 1: Mã Booking & Tên Khách hàng
        ttk.Label(info_frame, text="Booking ID:", font=FONT_BOLD).grid(row=0, column=0, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_booking_id = ttk.Label(info_frame, text="---", font=FONT_HEADER, foreground=COLOR_TEXT)
        self.lbl_cio_booking_id.grid(row=0, column=1, sticky=tk.W, pady=8)

        ttk.Label(info_frame, text="Guest Name:", font=FONT_BOLD).grid(row=0, column=2, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_guest_name = ttk.Label(info_frame, text="---", font=FONT_HEADER, foreground=COLOR_TEXT)
        self.lbl_cio_guest_name.grid(row=0, column=3, sticky=tk.W, pady=8)

        # Hàng 2: SĐT & Trạng thái hiện tại
        ttk.Label(info_frame, text="Phone Number:", font=FONT_BOLD).grid(row=1, column=0, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_phone = ttk.Label(info_frame, text="---", font=FONT_NORMAL)
        self.lbl_cio_phone.grid(row=1, column=1, sticky=tk.W, pady=8)

        ttk.Label(info_frame, text="Booking Status:", font=FONT_BOLD).grid(row=1, column=2, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_status = ttk.Label(info_frame, text="---", font=FONT_BOLD)
        self.lbl_cio_status.grid(row=1, column=3, sticky=tk.W, pady=8)

        # Hàng 3: Số ID Phòng / Số phòng & Loại phòng
        ttk.Label(info_frame, text="Room ID / Number:", font=FONT_BOLD).grid(row=2, column=0, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_room_id = ttk.Label(info_frame, text="---", font=FONT_HEADER, foreground="#1D4ED8")
        self.lbl_cio_room_id.grid(row=2, column=1, sticky=tk.W, pady=8)

        ttk.Label(info_frame, text="Room Type & Capacity:", font=FONT_BOLD).grid(row=2, column=2, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_room_type = ttk.Label(info_frame, text="---", font=FONT_NORMAL)
        self.lbl_cio_room_type.grid(row=2, column=3, sticky=tk.W, pady=8)

        # Hàng 4: Ngày Check-in & Check-out dự kiến
        ttk.Label(info_frame, text="Expected Check-in:", font=FONT_BOLD).grid(row=3, column=0, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_checkin_date = ttk.Label(info_frame, text="---", font=FONT_NORMAL)
        self.lbl_cio_checkin_date.grid(row=3, column=1, sticky=tk.W, pady=8)

        ttk.Label(info_frame, text="Expected Check-out:", font=FONT_BOLD).grid(row=3, column=2, sticky=tk.W, pady=8, padx=10)
        self.lbl_cio_checkout_date = ttk.Label(info_frame, text="---", font=FONT_NORMAL)
        self.lbl_cio_checkout_date.grid(row=3, column=3, sticky=tk.W, pady=8)

        # --- Section 3: Thao tác Check-in / Check-out (Action Frame) ---
        action_frame = ttk.LabelFrame(container, text=" ⚡ Confirm Action ", padding=15)
        action_frame.pack(fill=tk.X)

        ttk.Label(action_frame, text="Assign / change check-in room (optional):").pack(side=tk.LEFT, padx=10)
        self.txt_cio_custom_room = ttk.Entry(action_frame, width=15)
        self.txt_cio_custom_room.pack(side=tk.LEFT, padx=5)

        btn_confirm_checkin = ttk.Button(
            action_frame, text="📥 Confirm CHECK-IN", style="Primary.TButton", command=self.execute_check_in
        )
        btn_confirm_checkin.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=3)

        btn_confirm_checkout = ttk.Button(
            action_frame, text="📤 Confirm CHECK-OUT", style="Secondary.TButton", command=self.execute_check_out
        )
        btn_confirm_checkout.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=3)

    def search_cio_booking(self):
        """Tra cứu danh sách phòng dựa theo Tên hoặc SĐT"""
        keyword = self.txt_cio_keyword.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a guest name or phone number to search.")
            return

        # Lấy tất cả đơn từ Service
        all_reservations = self.service.view_reservations()
        
        # Lọc theo keyword (khớp tương đối Tên hoặc SĐT)
        self.cio_search_results = [
            r for r in all_reservations 
            if (keyword.lower() in (r['full_name'] or "").lower()) or (keyword in (r['phone'] or ""))
        ]

        if not self.cio_search_results:
            messagebox.showinfo("Notice", "No bookings match the information entered.")
            self._reset_cio_info_display()
            self.cbo_cio_results['values'] = []
            self.cbo_cio_results.set("")
            return

        # Đưa vào Combobox danh sách đơn tìm thấy
        combo_values = []
        for r in self.cio_search_results:
            room_str = r['room_id'] if r['room_id'] else "Unassigned"
            display_text = f"Booking #{r['booking_id']} - {r['full_name']} ({r['phone']}) | Room: {room_str} [{r['status']}]"
            combo_values.append(display_text)

        self.cbo_cio_results['values'] = combo_values
        self.cbo_cio_results.current(0)
        self._on_cio_booking_selected(None)

    def _on_cio_booking_selected(self, event):
        """Hiển thị chi tiết đơn được chọn từ Combobox"""
        idx = self.cbo_cio_results.current()
        if idx < 0 or idx >= len(self.cio_search_results):
            return

        booking = self.cio_search_results[idx]

        # Truy vấn bổ sung thông tin sức chứa phòng (số người) từ Database nếu có
        max_capacity = self._get_room_capacity(booking.get('type_name'))

        # Cập nhật thông tin lên UI
        self.lbl_cio_booking_id.config(text=str(booking['booking_id']))
        self.lbl_cio_guest_name.config(text=str(booking['full_name']))
        self.lbl_cio_phone.config(text=str(booking['phone']))
        self.lbl_cio_status.config(text=str(booking['status']))
        
        room_id_display = str(booking['room_id']) if booking['room_id'] else "No room assigned"
        self.lbl_cio_room_id.config(text=room_id_display)

        capacity_str = f" (Capacity: {max_capacity} guests)" if max_capacity else ""
        self.lbl_cio_room_type.config(text=f"{booking['type_name']}{capacity_str}")
        
        self.lbl_cio_checkin_date.config(text=str(booking['check_in']))
        self.lbl_cio_checkout_date.config(text=str(booking['check_out']))

        # Tự động điền số phòng sẵn vào ô tùy chỉnh phòng
        self.txt_cio_custom_room.delete(0, tk.END)
        if booking['room_id']:
            self.txt_cio_custom_room.insert(0, str(booking['room_id']))

    def _get_room_capacity(self, room_type_name):
        """Hàm phụ hỗ trợ lấy số người tối đa dựa vào tên loại phòng"""
        if not room_type_name:
            return None
        connection = db.get_connection()
        if not connection:
            return None
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT max_capacity FROM room_types WHERE type_name = %s", (room_type_name,))
            row = cursor.fetchone()
            return row['max_capacity'] if row else None
        except Exception:
            return None
        finally:
            cursor.close()
            connection.close()

    def _reset_cio_info_display(self):
        """Xóa trắng khu vực thông tin chi tiết phòng"""
        self.lbl_cio_booking_id.config(text="---")
        self.lbl_cio_guest_name.config(text="---")
        self.lbl_cio_phone.config(text="---")
        self.lbl_cio_status.config(text="---")
        self.lbl_cio_room_id.config(text="---")
        self.lbl_cio_room_type.config(text="---")
        self.lbl_cio_checkin_date.config(text="---")
        self.lbl_cio_checkout_date.config(text="---")
        self.txt_cio_custom_room.delete(0, tk.END)

    def execute_check_in(self):
        """Thực hiện Check-in cho phòng đang chọn"""
        booking_id_text = self.lbl_cio_booking_id.cget("text")
        if booking_id_text == "---":
            messagebox.showwarning("Warning", "Please find and select a booking to check in.")
            return

        try:
            booking_id = int(booking_id_text)
            room_number = self.txt_cio_custom_room.get().strip() or None

            success, message = self.service.process_check_in(booking_id, room_number)
            if success:
                messagebox.showinfo("Success", f"Check-in completed for booking #{booking_id}.\n{message}")
                self.load_reservations()
                self.search_cio_booking()  # Cập nhật lại thông tin mới lên giao diện
            else:
                messagebox.showerror("Failed", message)

        except ValueError:
            messagebox.showerror("Error", "Booking ID must be a valid integer.")

    def execute_check_out(self):
        """Thực hiện Check-out cho phòng đang chọn"""
        booking_id_text = self.lbl_cio_booking_id.cget("text")
        if booking_id_text == "---":
            messagebox.showwarning("Warning", "Please find and select a booking to check out.")
            return

        try:
            booking_id = int(booking_id_text)
            guest_name = self.lbl_cio_guest_name.cget("text")
            room_id = self.lbl_cio_room_id.cget("text")

            if messagebox.askyesno("Confirm Check-out", f"Confirm check-out for this guest:\n\n• Name: {guest_name}\n• Booking ID: #{booking_id}\n• Room: {room_id}"):
                success, message = self.service.process_check_out(booking_id)
                if success:
                    messagebox.showinfo("Success", f"Check-out completed for booking #{booking_id}.\n{message}")
                    self.load_reservations()
                    self.search_cio_booking()  # Cập nhật lại thông tin mới lên giao diện
                else:
                    messagebox.showerror("Failed", message)

        except ValueError:
            messagebox.showerror("Error", "Booking ID must be a valid integer.")

    def run(self):
        """Start the Tkinter GUI main event loop"""
        self.mainloop()

# Standalone execution for GUI testing
if __name__ == "__main__":
    app = ReceptionistView()
    app.run()
