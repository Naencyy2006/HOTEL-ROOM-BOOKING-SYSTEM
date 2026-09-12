# views/guest.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta, datetime

# Try to import tkcalendar for date selection; if not available, fallback to simple Entry widgets.
try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR = True
except ImportError:
    HAS_TKCALENDAR = False


COLOR_MAIN_BG = "#F5EFFF"   # Nền chính
COLOR_SIDEBAR = "#E5D9F2"   # Nền card / panel
COLOR_BUTTON  = "#CDC1FF"   # Nút phụ
COLOR_ACCENT  = "#A594F9"   # Nút chính / Header
COLOR_TEXT    = "#3B2F63"   # Chữ tối
COLOR_WHITE   = "#FFFFFF"

FONT_TITLE = ("Arial", 16, "bold")
FONT_HEADER = ("Arial", 11, "bold")
FONT_BOLD = ("Arial", 9, "bold")
FONT_NORMAL = ("Arial", 9)


class GuestView(tk.Frame):

    # Initialize the GuestView frame with parent, database connection, and authentication callback.
    def __init__(self, parent, db_conn=None, on_open_auth=None):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.parent = parent
        self.conn = db_conn
        self.on_open_auth = on_open_auth

        self._build_header()
        self._build_search_panel()
        self._build_room_display()

        self.search_rooms()

    # Build the header section of the guest view with title and authentication buttons.
    def _build_header(self):
        header = tk.Frame(self, bg=COLOR_ACCENT, pady=12, padx=25)
        header.pack(fill="x")

        tk.Label(
            header, text="HOTEL BOOKING SYSTEM",
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_TITLE
        ).pack(side="left")

        action_frame = tk.Frame(header, bg=COLOR_ACCENT)
        action_frame.pack(side="right")

        btn_login = tk.Button(
            action_frame, text="Login", command=lambda: self._goto_auth("login"),
            bg=COLOR_BUTTON, fg=COLOR_TEXT, font=FONT_BOLD,
            bd=0, padx=14, pady=4, cursor="hand2", activebackground=COLOR_SIDEBAR
        )
        btn_login.pack(side="left", padx=5)

        btn_register = tk.Button(
            action_frame, text="Register", command=lambda: self._goto_auth("register"),
            bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD,
            bd=0, padx=14, pady=4, cursor="hand2"
        )
        btn_register.pack(side="left", padx=5)

    # Build the search panel for filtering available rooms based on check-in/check-out dates, number of guests, and price range.
    def _build_search_panel(self):
        panel = tk.LabelFrame(
            self, text=" FIND YOUR PERFECT ROOM ", bg=COLOR_SIDEBAR,
            fg=COLOR_TEXT, font=FONT_HEADER, padx=15, pady=15, bd=0
        )
        panel.pack(fill="x", padx=25, pady=15)

        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Check-in Date Picker
        tk.Label(panel, text="Check-in", bg=COLOR_SIDEBAR, font=FONT_BOLD, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=5)
        if HAS_TKCALENDAR:
            self.txt_checkin = DateEntry(
                panel, font=FONT_NORMAL, width=11,
                background=COLOR_ACCENT, foreground=COLOR_WHITE,
                headersbackground=COLOR_ACCENT, headersforeground=COLOR_WHITE,
                selectbackground=COLOR_ACCENT, selectforeground=COLOR_WHITE,
                date_pattern='yyyy-mm-dd', mindate=today
            )
            self.txt_checkin.set_date(today)
            self.txt_checkin.bind("<<DateEntrySelected>>", self._on_checkin_change)
        else:
            self.txt_checkin = tk.Entry(panel, font=FONT_NORMAL, width=12)
            self.txt_checkin.insert(0, today.strftime("%Y-%m-%d"))
        self.txt_checkin.grid(row=1, column=0, padx=5, pady=(2, 10))

        # Check-out Date Picker
        tk.Label(panel, text="Check-out", bg=COLOR_SIDEBAR, font=FONT_BOLD, fg=COLOR_TEXT).grid(row=0, column=1, sticky="w", padx=5)
        if HAS_TKCALENDAR:
            self.txt_checkout = DateEntry(
                panel, font=FONT_NORMAL, width=11,
                background=COLOR_ACCENT, foreground=COLOR_WHITE,
                headersbackground=COLOR_ACCENT, headersforeground=COLOR_WHITE,
                selectbackground=COLOR_ACCENT, selectforeground=COLOR_WHITE,
                date_pattern='yyyy-mm-dd', mindate=tomorrow
            )
            self.txt_checkout.set_date(tomorrow)
        else:
            self.txt_checkout = tk.Entry(panel, font=FONT_NORMAL, width=12)
            self.txt_checkout.insert(0, tomorrow.strftime("%Y-%m-%d"))
        self.txt_checkout.grid(row=1, column=1, padx=5, pady=(2, 10))

        # Number of Guests Dropdown
        tk.Label(panel, text="Guests", bg=COLOR_SIDEBAR, font=FONT_BOLD, fg=COLOR_TEXT).grid(row=0, column=2, sticky="w", padx=5)
        self.cbo_guests = ttk.Combobox(panel, values=["1 Guest", "2 Guests", "3 Guests", "4+ Guests"], state="readonly", width=10)
        self.cbo_guests.current(0)
        self.cbo_guests.grid(row=1, column=2, padx=5, pady=(2, 10))

        # Min Price Entry
        tk.Label(panel, text="Min Price (VND)", bg=COLOR_SIDEBAR, font=FONT_BOLD, fg=COLOR_TEXT).grid(row=0, column=3, sticky="w", padx=5)
        self.txt_min_price = tk.Entry(panel, font=FONT_NORMAL, width=12)
        self.txt_min_price.grid(row=1, column=3, padx=5, pady=(2, 10))

        # Max Price Entry
        tk.Label(panel, text="Max Price (VND)", bg=COLOR_SIDEBAR, font=FONT_BOLD, fg=COLOR_TEXT).grid(row=0, column=4, sticky="w", padx=5)
        self.txt_max_price = tk.Entry(panel, font=FONT_NORMAL, width=12)
        self.txt_max_price.grid(row=1, column=4, padx=5, pady=(2, 10))

        # Search Button
        btn_search = tk.Button(
            panel, text="SEARCH ROOMS", command=self.search_rooms,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, bd=0, padx=15, pady=5, cursor="hand2"
        )
        btn_search.grid(row=1, column=5, padx=15, pady=(2, 10))

    # Automatically update the minimum check-out date when the check-in date changes, ensuring that check-out is always after check-in.
    def _on_checkin_change(self, event=None):
        # When the check-in date changes, update the minimum check-out date to be at least one day after the selected check-in date.
        if HAS_TKCALENDAR:
            checkin_date = self.txt_checkin.get_date()
            next_day = checkin_date + timedelta(days=1)
            self.txt_checkout.config(mindate=next_day)
            if self.txt_checkout.get_date() <= checkin_date:
                self.txt_checkout.set_date(next_day)

    # Build the room display section, showing available room types in a treeview with details like ID, name, capacity, price, and description.
    def _build_room_display(self):
        container = tk.Frame(self, bg=COLOR_MAIN_BG, padx=25)
        container.pack(fill="both", expand=True)

        tk.Label(
            container, text="Featured Room Types",
            bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", pady=(0, 10))

        columns = ("id", "name", "capacity", "price", "description")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=8)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Room Type")
        self.tree.heading("capacity", text="Capacity")
        self.tree.heading("price", text="Price / Night")
        self.tree.heading("description", text="Description & Amenities")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("capacity", width=100, anchor="center")
        self.tree.column("price", width=140, anchor="e")
        self.tree.column("description", width=400)

        self.tree.pack(fill="both", expand=True)

        btn_book = tk.Button(
            self, text="Book Now", command=self._handle_book_now,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_HEADER, bd=0, padx=25, pady=8, cursor="hand2"
        )
        btn_book.pack(pady=15)

    def search_rooms(self):
        # Validate the check-in and check-out dates to ensure that the check-out date is after the check-in date.
        try:
            if HAS_TKCALENDAR:
                checkin_dt = self.txt_checkin.get_date()
                checkout_dt = self.txt_checkout.get_date()
            else:
                checkin_dt = datetime.strptime(self.txt_checkin.get().strip(), "%Y-%m-%d").date()
                checkout_dt = datetime.strptime(self.txt_checkout.get().strip(), "%Y-%m-%d").date()

            if checkin_dt >= checkout_dt:
                messagebox.showerror(
                    "Invalid Date",
                    "Check-out date must be AFTER check-in date!"
                )
                for item in self.tree.get_children():
                    self.tree.delete(item)
                return
        except Exception:
            messagebox.showerror("Invalid Date Format", "Please enter valid dates (YYYY-MM-DD).")
            return

        # Clear the current room display before loading new search results.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load available room types from the database based on the search criteria, including number of guests and price range.
        if not self.conn:
            return

        # Load available room types from the database based on the search criteria, including number of guests and price range.
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT room_type_id, type_name, capacity, price_per_night, description FROM room_types WHERE 1=1"
            params = []

            guest_str = self.cbo_guests.get()
            guest_num = int(guest_str.split()[0].replace("+", ""))
            query += " AND capacity >= %s"
            params.append(guest_num)

            min_p = self.txt_min_price.get().strip()
            if min_p.isdigit():
                query += " AND price_per_night >= %s"
                params.append(float(min_p))

            max_p = self.txt_max_price.get().strip()
            if max_p.isdigit():
                query += " AND price_per_night <= %s"
                params.append(float(max_p))

            cursor.execute(query, tuple(params))
            rooms = cursor.fetchall()

            for r in rooms:
                self.tree.insert("", "end", values=(
                    r["room_type_id"],
                    r["type_name"],
                    f"{r['capacity']} Guests",
                    f"{float(r['price_per_night']):,.0f} VND",
                    r.get("description", "")
                ))
            cursor.close()
        except Exception as e:
            print(f"Error loading rooms: {e}")

    # Navigate to the authentication view (login or register) when the user clicks the corresponding button in the header.
    def _goto_auth(self, tab="login"):
        if self.on_open_auth:
            self.on_open_auth(tab)

    # Handle the "Book Now" button click event, prompting the user to log in or register if they are not authenticated before proceeding with the booking process.
    def _handle_book_now(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Notice", "Please select a room type to book.")
            return

        msg = messagebox.askyesno(
            "Authentication Required",
            "Only registered members can book rooms.\nWould you like to log in or register now?"
        )
        if msg and self.on_open_auth:
            self.on_open_auth("login")