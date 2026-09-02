import tkinter as tk
from tkinter import ttk, messagebox

class ModernHotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Room Booking System - Receptionist Panel")
        self.geometry("1200x750")
        self.minsize(1050, 680)

        # ---------------------------------------------------------
        # COLOR PALETTE
        # ---------------------------------------------------------
        self.COLOR_HEADER_BG = "#0A3963"  # Màu Xanh Navy của thanh Heading
        self.COLOR_BG_MAIN   = "#F1F5F9"  # Nền tổng thể (Xám trắng nhạt)
        self.COLOR_BG_CARD   = "#FFFFFF"  # Nền Card / Khung chứa (Trắng tinh)
        self.COLOR_BG_INPUT  = "#F8FAFC"  # Nền ô nhập liệu
        self.COLOR_BORDER    = "#E2E8F0"  # Màu đường viền nhẹ
        self.COLOR_ACCENT    = "#2563EB"  # Xanh Dương chủ đạo (Royal Blue)
        self.COLOR_TEXT_MAIN = "#1E293B"  # Chữ chính (Đen xám đậm)
        self.COLOR_TEXT_MUTED= "#64748B"  # Chữ phụ (Xám)
        self.COLOR_RED_BTN   = "#E53935"  # Đỏ nút Logout
        self.COLOR_GREEN     = "#059669"  # Xanh lá cây (Giá tiền / Status)
        self.COLOR_ORANGE    = "#D97706"  # Cam Status

        self.configure(bg=self.COLOR_BG_MAIN)

        # Mock Data
        self.room_types = [
            {"id": 101, "name": "Standard", "price": 1200000},
            {"id": 102, "name": "Standard", "price": 1200000},
            {"id": 201, "name": "Deluxe", "price": 2400000},
            {"id": 202, "name": "Ocean Suite", "price": 3500000},
        ]

        self.bookings = [
            {
                "id": "BK-2026-001",
                "guest": "Daniel Vance",
                "guests_count": "2A 0C",
                "contact": "Daniel@daniel.com\n7808032007",
                "room": "Standard\n#101",
                "dates": "2026-10-24\nto 2026-10-26",
                "total": 2400000,
                "nights": 2,
                "notes": "Honeymoon",
                "status": "Reserved",
                "payment": "Pending"
            },
            {
                "id": "BK-2026-002",
                "guest": "Sophia Chen",
                "guests_count": "1A 1C",
                "contact": "sophia@example.com\n0912345678",
                "room": "Deluxe\n#201",
                "dates": "2026-10-25\nto 2026-10-28",
                "total": 7200000,
                "nights": 3,
                "notes": "Late check-in",
                "status": "Checked In",
                "payment": "Paid"
            }
        ]

        self.current_status_filter = "All"
        self.active_tab = "Reservations"
        self._setup_custom_styles()
        self._build_header_and_nav()
        
        # Container cho các màn hình (Views)
        self.view_container = tk.Frame(self, bg=self.COLOR_BG_MAIN)
        self.view_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        self.views = {}
        self._init_views()
        self.switch_tab("Reservations")

    def _setup_custom_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        # Style cho Treeview (Bảng danh sách)
        style.configure("Light.Treeview",
                        background=self.COLOR_BG_CARD,
                        foreground=self.COLOR_TEXT_MAIN,
                        fieldbackground=self.COLOR_BG_CARD,
                        borderwidth=0,
                        rowheight=42,
                        font=("Helvetica", 10))
        
        style.configure("Light.Treeview.Heading",
                        background="#E2E8F0",
                        foreground=self.COLOR_TEXT_MAIN,
                        font=("Helvetica", 10, "bold"),
                        borderwidth=0)
        
        style.map("Light.Treeview", background=[('selected', "#DBEAFE")])

    # ---------------------------------------------------------
    # HEADER & NAVIGATION BAR (Đã xóa Dashboard, Guests, Settings)
    # ---------------------------------------------------------
    def _build_header_and_nav(self):
        # 1. Heading Top Bar Tràn Viền (Màu Xanh Navy)
        header_bar = tk.Frame(self, bg=self.COLOR_HEADER_BG, height=55)
        header_bar.pack(fill=tk.X, side=tk.TOP)
        header_bar.pack_propagate(False)

        # Left: Icon & Title
        left_frame = tk.Frame(header_bar, bg=self.COLOR_HEADER_BG)
        left_frame.pack(side=tk.LEFT, padx=20)

        lbl_icon = tk.Label(left_frame, text="🏨", font=("Segoe UI Emoji", 13), bg=self.COLOR_HEADER_BG, fg="white")
        lbl_icon.pack(side=tk.LEFT, padx=(0, 10))

        lbl_title = tk.Label(left_frame, text="Hotel Booking System", font=("Helvetica", 13, "bold"), fg="white", bg=self.COLOR_HEADER_BG)
        lbl_title.pack(side=tk.LEFT)

        # Right: Chuông Thông báo, Tên "Ngọc ▼", Nút Logout
        right_frame = tk.Frame(header_bar, bg=self.COLOR_HEADER_BG)
        right_frame.pack(side=tk.RIGHT, padx=20)

        lbl_bell = tk.Label(right_frame, text="🔔", font=("Segoe UI Emoji", 11), fg="white", bg=self.COLOR_HEADER_BG, cursor="hand2")
        lbl_bell.pack(side=tk.LEFT, padx=(0, 20))

        lbl_user = tk.Label(right_frame, text="Ngọc ▼", font=("Helvetica", 10, "bold"), fg="white", bg=self.COLOR_HEADER_BG, cursor="hand2")
        lbl_user.pack(side=tk.LEFT, padx=(0, 15))

        btn_logout = tk.Button(right_frame, text="Logout", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_RED_BTN,
                               activebackground="#C62828", activeforeground="white", bd=0, padx=14, pady=5, cursor="hand2")
        btn_logout.pack(side=tk.LEFT)

        # 2. Navigation Bar (Đã chỉ giữ 4 tab chính)
        nav_frame = tk.Frame(self, bg=self.COLOR_BG_MAIN)
        nav_frame.pack(fill=tk.X, padx=25, pady=(15, 5))

        self.nav_buttons = {}
        tabs = [
            ("Reservations", "📅 Reservations"),
            ("Calendar", "🗓️ Calendar"),
            ("Rooms", "🛏️ Rooms"),
            ("New Booking", "➕ New Booking")
        ]

        for tab_key, tab_label in tabs:
            btn = tk.Button(
                nav_frame, text=tab_label, font=("Helvetica", 10, "bold"),
                fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_MAIN,
                activebackground=self.COLOR_BG_CARD, activeforeground=self.COLOR_TEXT_MAIN,
                bd=0, padx=16, pady=8, cursor="hand2",
                command=lambda k=tab_key: self.switch_tab(k)
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.nav_buttons[tab_key] = btn

    def switch_tab(self, tab_key):
        self.active_tab = tab_key
        for key, btn in self.nav_buttons.items():
            if key == tab_key:
                btn.config(bg=self.COLOR_ACCENT, fg="white")
            else:
                btn.config(bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT_MUTED)

        for view in self.views.values():
            view.pack_forget()

        if tab_key in self.views:
            self.views[tab_key].pack(fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------
    # INITIALIZE VIEWS
    # ---------------------------------------------------------
    def _init_views(self):
        self.views["Reservations"] = self._build_reservations_view()
        self.views["Calendar"] = self._build_calendar_view()
        self.views["Rooms"] = self._build_rooms_view()
        self.views["New Booking"] = self._build_new_booking_view()

    # ---------------------------------------------------------
    # VIEW 1: RESERVATIONS MANAGEMENT (Có Search & Sửa Status)
    # ---------------------------------------------------------
    def _build_reservations_view(self):
        main_frame = tk.Frame(self.view_container, bg=self.COLOR_BG_MAIN)

        card = tk.Frame(main_frame, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.pack(fill=tk.BOTH, expand=True)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=25, pady=20)

        lbl_head = tk.Label(top_sec, text="Reservations Management", font=("Helvetica", 18, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
        lbl_head.pack(side=tk.LEFT)

        # Thanh Tìm Kiếm Khách Hàng (Search Bar)
        search_frame = tk.Frame(top_sec, bg=self.COLOR_BG_CARD)
        search_frame.pack(side=tk.RIGHT)

        tk.Label(search_frame, text="🔍", font=("Segoe UI Emoji", 11), bg=self.COLOR_BG_CARD, fg=self.COLOR_TEXT_MUTED).pack(side=tk.LEFT, padx=(0, 5))
        
        self.ent_search = tk.Entry(search_frame, font=("Helvetica", 10), bg=self.COLOR_BG_INPUT, fg=self.COLOR_TEXT_MAIN, bd=1, relief=tk.SOLID, width=28)
        self.ent_search.insert(0, "")
        self.ent_search.pack(side=tk.LEFT, ipady=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self._update_reservations_table())

        # Thanh Lọc Status (Filter Pills)
        filter_bar = tk.Frame(card, bg=self.COLOR_BG_INPUT, pady=4)
        filter_bar.pack(fill=tk.X, padx=25, pady=(0, 15))

        self.filter_buttons = {}
        for filter_name in ["All", "Active", "Cancelled", "Completed"]:
            btn = tk.Button(
                filter_bar, text=filter_name, font=("Helvetica", 9, "bold"),
                fg=self.COLOR_TEXT_MAIN if filter_name == "All" else self.COLOR_TEXT_MUTED,
                bg=self.COLOR_BG_CARD if filter_name == "All" else self.COLOR_BG_INPUT,
                bd=0, padx=20, pady=4, cursor="hand2",
                command=lambda f=filter_name: self._set_status_filter(f)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.filter_buttons[filter_name] = btn

        # Bảng Dữ Liệu
        table_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        columns = ("Guest", "Contact", "Room", "Dates", "Total", "Notes", "Status", "Payment", "Actions")
        self.tree_res = ttk.Treeview(table_frame, columns=columns, show="headings", style="Light.Treeview")

        headings = {
            "Guest": "Guest", "Contact": "Contact", "Room": "Room", 
            "Dates": "Dates", "Total": "Total", "Notes": "Notes", 
            "Status": "Status (Nhấp đúp đổi)", "Payment": "Payment", "Actions": "Actions"
        }

        for col, head in headings.items():
            self.tree_res.heading(col, text=head, anchor=tk.W if col != "Actions" else tk.CENTER)
            self.tree_res.column(col, width=120, anchor=tk.W if col != "Actions" else tk.CENTER)

        self.tree_res.column("Guest", width=130)
        self.tree_res.column("Contact", width=160)
        self.tree_res.column("Dates", width=130)
        self.tree_res.pack(fill=tk.BOTH, expand=True)

        # Bắt sự kiện Nhấp Đúp chuột vào dòng để sửa Status
        self.tree_res.bind("<Double-1>", self._on_reservation_double_click)

        # Load dữ liệu vào bảng
        self._update_reservations_table()

        # Toast Thông báo
        toast = tk.Frame(main_frame, bg="#EFF6FF", highlightthickness=1, highlightbackground=self.COLOR_ACCENT)
        toast.pack(fill=tk.X, pady=(15, 0), side=tk.BOTTOM)
        
        lbl_toast_title = tk.Label(toast, text="💡 Mẹo nhanh", font=("Helvetica", 9, "bold"), fg=self.COLOR_ACCENT, bg="#EFF6FF")
        lbl_toast_title.pack(anchor="w", padx=15, pady=(6, 0))
        lbl_toast_msg = tk.Label(toast, text="Nhấp đôi (Double-click) vào hàng bất kỳ trong bảng để đổi trạng thái Booking.", font=("Helvetica", 9), fg=self.COLOR_TEXT_MAIN, bg="#EFF6FF")
        lbl_toast_msg.pack(anchor="w", padx=15, pady=(0, 6))

        return main_frame

    def _set_status_filter(self, filter_name):
        self.current_status_filter = filter_name
        for name, btn in self.filter_buttons.items():
            if name == filter_name:
                btn.config(bg=self.COLOR_BG_CARD, fg=self.COLOR_TEXT_MAIN)
            else:
                btn.config(bg=self.COLOR_BG_INPUT, fg=self.COLOR_TEXT_MUTED)
        self._update_reservations_table()

    def _update_reservations_table(self):
        # Xóa dữ liệu cũ
        for item in self.tree_res.get_children():
            self.tree_res.delete(item)

        query = self.ent_search.get().lower().strip()

        for b in self.bookings:
            # 1. Lọc theo Filter Button
            if self.current_status_filter != "All":
                if self.current_status_filter == "Active" and b["status"] not in ["Reserved", "Checked In"]:
                    continue
                elif self.current_status_filter == "Cancelled" and b["status"] != "Cancelled":
                    continue
                elif self.current_status_filter == "Completed" and b["status"] != "Checked Out":
                    continue

            # 2. Lọc theo thanh Tìm kiếm
            match_search = (
                query in b["guest"].lower() or
                query in b["contact"].lower() or
                query in b["room"].lower() or
                query in b["id"].lower()
            )
            if query and not match_search:
                continue

            formatted_price = f"{b['total']:,} VND\n{b['nights']} nights"
            self.tree_res.insert("", tk.END, iid=b["id"], values=(
                f"{b['guest']}\n{b['guests_count']}",
                b['contact'],
                b['room'],
                b['dates'],
                formatted_price,
                b['notes'],
                f"  {b['status']}  ",
                f"  {b['payment']}  ",
                "✏️ Đổi Status"
            ))

    def _on_reservation_double_click(self, event):
        selected_id = self.tree_res.focus()
        if not selected_id:
            return
        
        booking = next((b for b in self.bookings if b["id"] == selected_id), None)
        if booking:
            self._open_change_status_popup(booking)

    # cửa sổ Popup Đổi Trạng Thái
    def _open_change_status_popup(self, booking):
        win = tk.Toplevel(self)
        win.title("Cập nhật Trạng thái")
        win.geometry("340x200")
        win.configure(bg=self.COLOR_BG_CARD)
        win.resizable(False, False)
        win.grab_set()  # Khóa tương tác màn hình chính khi popup mở

        tk.Label(win, text=f"Cập nhật Trạng Thái Booking", font=("Helvetica", 11, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(pady=(15, 5))
        tk.Label(win, text=f"Khách hàng: {booking['guest']} ({booking['id']})", font=("Helvetica", 9), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_CARD).pack(pady=(0, 12))

        cbo_status = ttk.Combobox(win, values=["Reserved", "Checked In", "Checked Out", "Cancelled"], state="readonly", font=("Helvetica", 10))
        cbo_status.set(booking["status"])
        cbo_status.pack(pady=5, ipady=4, padx=30, fill=tk.X)

        def save_changes():
            new_status = cbo_status.get()
            booking["status"] = new_status
            self._update_reservations_table()
            messagebox.showinfo("Thành công", f"Đã đổi trạng thái sang: '{new_status}'")
            win.destroy()

        btn_save = tk.Button(win, text="Lưu Thay Đổi", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_ACCENT,
                             activebackground="#1D4ED8", bd=0, padx=20, pady=6, cursor="hand2", command=save_changes)
        btn_save.pack(pady=15)

    # ---------------------------------------------------------
    # VIEW 2: NEW BOOKING
    # ---------------------------------------------------------
    def _build_new_booking_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        lbl_head = tk.Label(card, text="New Booking", font=("Helvetica", 18, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
        lbl_head.pack(anchor="w", padx=25, pady=(20, 15))

        form_grid = tk.Frame(card, bg=self.COLOR_BG_CARD)
        form_grid.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        form_grid.columnconfigure(0, weight=1)
        form_grid.columnconfigure(1, weight=1)

        def create_field(parent, label_text, row, col, default_val=""):
            frame = tk.Frame(parent, bg=self.COLOR_BG_CARD)
            frame.grid(row=row, column=col, sticky="ew", padx=15, pady=8)
            
            lbl = tk.Label(frame, text=label_text, font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
            lbl.pack(anchor="w", pady=(0, 4))
            
            ent = tk.Entry(frame, font=("Helvetica", 10), bg=self.COLOR_BG_INPUT, fg=self.COLOR_TEXT_MAIN, bd=1, relief=tk.SOLID)
            ent.insert(0, default_val)
            ent.pack(fill=tk.X, ipady=7, padx=1)
            return ent

        self.ent_guest_name = create_field(form_grid, "Guest Name *", 0, 0, "Daniel Vance")
        self.ent_email = create_field(form_grid, "Email *", 0, 1, "Daniel@daniel.com")
        self.ent_phone = create_field(form_grid, "Phone", 1, 0, "7808032007")

        room_frame = tk.Frame(form_grid, bg=self.COLOR_BG_CARD)
        room_frame.grid(row=1, column=1, sticky="ew", padx=15, pady=8)
        
        tk.Label(room_frame, text="Room *", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(anchor="w", pady=(0, 2))
        tk.Label(room_frame, text="1 Standard room available | 1 Deluxe room available", font=("Helvetica", 8), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_CARD).pack(anchor="w", pady=(0, 4))
        
        self.cbo_room = ttk.Combobox(room_frame, values=["#101 - Standard (1,200,000 VND/night)", "#201 - Deluxe (2,400,000 VND/night)"], state="readonly")
        self.cbo_room.current(0)
        self.cbo_room.pack(fill=tk.X, ipady=4)

        self.ent_checkin = create_field(form_grid, "Check-In Date *", 2, 0, "2026-10-24")
        self.ent_checkout = create_field(form_grid, "Check-Out Date *", 2, 1, "2026-10-26")
        self.ent_adults = create_field(form_grid, "Adults *", 3, 0, "2")
        self.ent_children = create_field(form_grid, "Children", 3, 1, "0")

        req_frame = tk.Frame(form_grid, bg=self.COLOR_BG_CARD)
        req_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        
        tk.Label(req_frame, text="Special Requests", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(anchor="w", pady=(0, 4))
        self.txt_requests = tk.Text(req_frame, height=3, font=("Helvetica", 10), bg=self.COLOR_BG_INPUT, fg=self.COLOR_TEXT_MAIN, bd=1, relief=tk.SOLID)
        self.txt_requests.insert("1.0", "Honeymoon setup required...")
        self.txt_requests.pack(fill=tk.X)

        btn_submit = tk.Button(card, text="Submit Reservation", font=("Helvetica", 10, "bold"), fg="white", bg=self.COLOR_ACCENT,
                               activebackground="#1D4ED8", bd=0, pady=10, padx=25, cursor="hand2", command=self._handle_create_booking)
        btn_submit.pack(anchor="e", padx=40, pady=(10, 25))

        return card

    def _handle_create_booking(self):
        messagebox.showinfo("Success", "Reservation created successfully!")
        self.switch_tab("Reservations")

    # ---------------------------------------------------------
    # VIEW 3: CALENDAR
    # ---------------------------------------------------------
    def _build_calendar_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=25, pady=20)

        lbl_month = tk.Label(top_sec, text="November 2026", font=("Helvetica", 18, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
        lbl_month.pack(side=tk.LEFT)

        nav_btn_frame = tk.Frame(top_sec, bg=self.COLOR_BG_CARD)
        nav_btn_frame.pack(side=tk.RIGHT)

        btn_prev = tk.Button(nav_btn_frame, text="◀", font=("Helvetica", 9), fg="white", bg=self.COLOR_ACCENT, bd=0, padx=10, pady=4, cursor="hand2")
        btn_prev.pack(side=tk.LEFT, padx=2)

        btn_next = tk.Button(nav_btn_frame, text="▶", font=("Helvetica", 9), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_INPUT, bd=0, padx=10, pady=4, cursor="hand2")
        btn_next.pack(side=tk.LEFT, padx=2)

        grid_frame = tk.Frame(card, bg=self.COLOR_BORDER)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        days = [("Room", "")] + [(f"{i}", ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"][(i-1)%7]) for i in range(1, 14)]
        
        for col_idx, (day_num, day_str) in enumerate(days):
            header_text = f"{day_num}\n{day_str}".strip()
            lbl = tk.Label(grid_frame, text=header_text, font=("Helvetica", 8, "bold"), fg=self.COLOR_TEXT_MAIN, bg="#F1F5F9", width=8, pady=8)
            lbl.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)

        rooms_list = [("101", "Standard"), ("201", "Deluxe")]
        for row_idx, (r_num, r_type) in enumerate(rooms_list, start=1):
            lbl_room = tk.Label(grid_frame, text=f"{r_num}\n{r_type}", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD, width=10, pady=12)
            lbl_room.grid(row=row_idx, column=0, sticky="nsew", padx=1, pady=1)

            for col_idx in range(1, 14):
                cell_bg = self.COLOR_BG_CARD
                if row_idx == 1 and 3 <= col_idx <= 5:
                    cell_bg = self.COLOR_ACCENT
                elif row_idx == 2 and 7 <= col_idx <= 9:
                    cell_bg = self.COLOR_ORANGE

                cell = tk.Frame(grid_frame, bg=cell_bg)
                cell.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

        legend_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        legend_frame.pack(fill=tk.X, padx=25, pady=15)

        legends = [
            ("Reserved", self.COLOR_ORANGE),
            ("Confirmed", self.COLOR_GREEN),
            ("Checked In", self.COLOR_ACCENT)
        ]

        for text, color in legends:
            box = tk.Frame(legend_frame, bg=color, width=12, height=12)
            box.pack(side=tk.LEFT, padx=(0, 6))
            lbl = tk.Label(legend_frame, text=text, font=("Helvetica", 9), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
            lbl.pack(side=tk.LEFT, padx=(0, 20))

        return card

    # ---------------------------------------------------------
    # VIEW 4: ROOMS
    # ---------------------------------------------------------
    def _build_rooms_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        lbl_head = tk.Label(card, text="Room Inventory", font=("Helvetica", 18, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
        lbl_head.pack(anchor="w", padx=25, pady=20)

        rooms_grid = tk.Frame(card, bg=self.COLOR_BG_CARD)
        rooms_grid.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        for idx, room in enumerate(self.room_types):
            r_card = tk.Frame(rooms_grid, bg=self.COLOR_BG_INPUT, highlightthickness=1, highlightbackground=self.COLOR_BORDER, width=220, height=130)
            r_card.grid(row=idx//2, column=idx%2, padx=15, pady=15, sticky="nsew")
            r_card.grid_propagate(False)

            tk.Label(r_card, text=f"Room #{room['id']}", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_INPUT).pack(anchor="w", padx=12, pady=(12, 2))
            tk.Label(r_card, text=f"Type: {room['name']}", font=("Helvetica", 9), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_INPUT).pack(anchor="w", padx=12)
            tk.Label(r_card, text=f"Rate: {room['price']:,} VND/night", font=("Helvetica", 10, "bold"), fg=self.COLOR_GREEN, bg=self.COLOR_BG_INPUT).pack(anchor="w", padx=12, pady=(8, 0))

        return card

if __name__ == "__main__":
    app = ModernHotelApp()
    app.mainloop()