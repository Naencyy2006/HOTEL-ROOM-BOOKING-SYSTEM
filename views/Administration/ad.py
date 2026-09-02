import tkinter as tk
from tkinter import ttk, messagebox

class AdminHotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Room Booking System - Administrator Panel")
        self.geometry("1280x800")
        self.minsize(1100, 700)

        # ---------------------------------------------------------
        # PALETTE MÀU CHUẨN
        # ---------------------------------------------------------
        self.COLOR_HEADER_BG = "#0A3963"  # Màu Xanh Navy đậm của Header
        self.COLOR_BG_MAIN   = "#F1F5F9"  # Nền tổng thể
        self.COLOR_BG_CARD   = "#FFFFFF"  # Nền Card / Khung chứa
        self.COLOR_BG_INPUT  = "#F8FAFC"  # Nền ô nhập liệu
        self.COLOR_BORDER    = "#E2E8F0"  # Viền nhẹ
        self.COLOR_ACCENT    = "#2563EB"  # Xanh Dương chủ đạo
        self.COLOR_TEXT_MAIN = "#1E293B"  # Chữ đen xám đậm
        self.COLOR_TEXT_MUTED= "#64748B"  # Chữ xám phụ
        self.COLOR_RED_BTN   = "#E53935"  # Đỏ nút Logout/Delete/Lock
        self.COLOR_GREEN     = "#059669"  # Xanh lá cây (Doanh thu / Active)
        self.COLOR_ORANGE    = "#D97706"  # Cam (Maintenance / Pending)

        self.configure(bg=self.COLOR_BG_MAIN)

        # ---------------------------------------------------------
        # MOCK DATA (Dữ liệu giả lập cho Admin)
        # ---------------------------------------------------------
        self.rooms_data = [
            {"number": "101", "type": "Standard", "price": 1200000, "capacity": 2, "status": "Available", "amenities": "Wifi, TV, Aircon"},
            {"number": "102", "type": "Standard", "price": 1200000, "capacity": 2, "status": "Occupied", "amenities": "Wifi, TV, Aircon"},
            {"number": "201", "type": "Deluxe", "price": 2400000, "capacity": 3, "status": "Available", "amenities": "Wifi, TV, MiniBar, Balcony"},
            {"number": "202", "type": "Ocean Suite", "price": 3500000, "capacity": 4, "status": "Maintenance", "amenities": "Wifi, TV, Jacuzzi, Ocean View"}
        ]

        self.users_data = [
            {"id": "USR-001", "name": "Daniel Vance", "email": "daniel@example.com", "role": "Member", "status": "Active", "bookings": 3},
            {"id": "USR-002", "name": "Sophia Chen", "email": "sophia@example.com", "role": "Member", "status": "Locked", "bookings": 1},
            {"id": "REC-001", "name": "Ngọc (Front Desk)", "email": "ngoc.reception@hotel.com", "role": "Receptionist", "status": "Active", "bookings": 0},
            {"id": "ADM-001", "name": "Minh Admin", "email": "admin.minh@hotel.com", "role": "Administrator", "status": "Active", "bookings": 0}
        ]

        self.all_bookings = [
            {"id": "BK-2026-001", "guest": "Daniel Vance", "room": "Standard #101", "dates": "2026-10-24 to 2026-10-26", "total": 2400000, "status": "Confirmed"},
            {"id": "BK-2026-002", "guest": "Sophia Chen", "room": "Deluxe #201", "dates": "2026-10-25 to 2026-10-28", "total": 7200000, "status": "Checked In"},
            {"id": "BK-2026-003", "guest": "Alex Mercer", "room": "Ocean Suite #202", "dates": "2026-11-01 to 2026-11-03", "total": 7000000, "status": "Cancelled"}
        ]

        self.reviews_data = [
            {"id": "REV-101", "guest": "Daniel Vance", "room": "Standard", "rating": "⭐⭐⭐⭐⭐ (5/5)", "comment": "Great room service and clean atmosphere!", "status": "Published"},
            {"id": "REV-102", "guest": "Anonymous Spam", "room": "Deluxe", "rating": "⭐ (1/5)", "comment": "Visit cheap-pills-online.com for discounts!", "status": "Spam Flagged"}
        ]

        self.active_tab = "Reports"
        self._setup_custom_styles()
        self._build_header_and_nav()
        
        self.view_container = tk.Frame(self, bg=self.COLOR_BG_MAIN)
        self.view_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        self.views = {}
        self._init_views()
        self.switch_tab("Reports")

    def _setup_custom_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Light.Treeview",
                        background=self.COLOR_BG_CARD,
                        foreground=self.COLOR_TEXT_MAIN,
                        fieldbackground=self.COLOR_BG_CARD,
                        borderwidth=0,
                        rowheight=38,
                        font=("Helvetica", 10))
        
        style.configure("Light.Treeview.Heading",
                        background="#E2E8F0",
                        foreground=self.COLOR_TEXT_MAIN,
                        font=("Helvetica", 10, "bold"),
                        borderwidth=0)
        
        style.map("Light.Treeview", background=[('selected', "#DBEAFE")])

    # ---------------------------------------------------------
    # HEADER & NAVIGATION BAR
    # ---------------------------------------------------------
    def _build_header_and_nav(self):
        # 1. Heading Top Bar Tràn Viền (Navy `#0A3963`)
        header_bar = tk.Frame(self, bg=self.COLOR_HEADER_BG, height=55)
        header_bar.pack(fill=tk.X, side=tk.TOP)
        header_bar.pack_propagate(False)

        left_frame = tk.Frame(header_bar, bg=self.COLOR_HEADER_BG)
        left_frame.pack(side=tk.LEFT, padx=20)

        lbl_icon = tk.Label(left_frame, text="🏨", font=("Segoe UI Emoji", 13), bg=self.COLOR_HEADER_BG, fg="white")
        lbl_icon.pack(side=tk.LEFT, padx=(0, 10))

        lbl_title = tk.Label(left_frame, text="Hotel Booking System - Admin Panel", font=("Helvetica", 13, "bold"), fg="white", bg=self.COLOR_HEADER_BG)
        lbl_title.pack(side=tk.LEFT)

        right_frame = tk.Frame(header_bar, bg=self.COLOR_HEADER_BG)
        right_frame.pack(side=tk.RIGHT, padx=20)

        lbl_bell = tk.Label(right_frame, text="🔔", font=("Segoe UI Emoji", 11), fg="white", bg=self.COLOR_HEADER_BG, cursor="hand2")
        lbl_bell.pack(side=tk.LEFT, padx=(0, 20))

        lbl_user = tk.Label(right_frame, text="Minh (Admin) ▼", font=("Helvetica", 10, "bold"), fg="white", bg=self.COLOR_HEADER_BG, cursor="hand2")
        lbl_user.pack(side=tk.LEFT, padx=(0, 15))

        btn_logout = tk.Button(right_frame, text="Logout", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_RED_BTN,
                               activebackground="#C62828", activeforeground="white", bd=0, padx=14, pady=5, cursor="hand2")
        btn_logout.pack(side=tk.LEFT)

        # 2. Navigation Bar (Tabs Admin)
        nav_frame = tk.Frame(self, bg=self.COLOR_BG_MAIN)
        nav_frame.pack(fill=tk.X, padx=25, pady=(15, 5))

        self.nav_buttons = {}
        tabs = [
            ("Reports", "📊 Reports & Statistics"),
            ("Manage Rooms", "🛏️ Manage Rooms"),
            ("Manage Users", "👥 Manage Users"),
            ("Manage Bookings", "📅 Manage Bookings"),
            ("Manage Reviews", "⭐ Manage Reviews")
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
    # INITIALIZE ALL ADMIN VIEWS
    # ---------------------------------------------------------
    def _init_views(self):
        self.views["Reports"] = self._build_reports_view()
        self.views["Manage Rooms"] = self._build_manage_rooms_view()
        self.views["Manage Users"] = self._build_manage_users_view()
        self.views["Manage Bookings"] = self._build_manage_bookings_view()
        self.views["Manage Reviews"] = self._build_manage_reviews_view()

    # ---------------------------------------------------------
    # TAB 1: REPORTS & STATISTICS (Báo cáo & Thống kê)
    # ---------------------------------------------------------
    def _build_reports_view(self):
        frame = tk.Frame(self.view_container, bg=self.COLOR_BG_MAIN)

        # Stat Cards Grid (4 Thẻ chỉ số tổng quan)
        stats_frame = tk.Frame(frame, bg=self.COLOR_BG_MAIN)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        cards_data = [
            ("Total Revenue (Month)", "16,600,000 VND", "▲ +12% vs last month", self.COLOR_GREEN),
            ("Occupancy Rate", "75.0%", "3 / 4 Rooms occupied", self.COLOR_ACCENT),
            ("Total Bookings", "18 Bookings", "Active this month", self.COLOR_TEXT_MAIN),
            ("Active Members", "142 Users", "2 Locked for policy", self.COLOR_ORANGE)
        ]

        for title, val, sub, col in cards_data:
            c = tk.Frame(stats_frame, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER, width=240, height=100)
            c.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
            c.pack_propagate(False)

            tk.Label(c, text=title, font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_CARD).pack(anchor="w", padx=15, pady=(12, 2))
            tk.Label(c, text=val, font=("Helvetica", 14, "bold"), fg=col, bg=self.COLOR_BG_CARD).pack(anchor="w", padx=15)
            tk.Label(c, text=sub, font=("Helvetica", 8), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_BG_CARD).pack(anchor="w", padx=15, pady=(2, 0))

        # Main Report Table Card
        card = tk.Frame(frame, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_title = tk.Label(card, text="Revenue Breakdown by Room Type", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD)
        lbl_title.pack(anchor="w", padx=20, pady=15)

        columns = ("Room Type", "Total Bookings", "Nights Booked", "Occupancy Rate", "Total Revenue")
        tree = ttk.Treeview(card, columns=columns, show="headings", style="Light.Treeview", height=6)

        for col in columns:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, width=150, anchor=tk.W)

        tree.insert("", tk.END, values=("Standard Room", "8 Bookings", "16 Nights", "80%", "9,600,000 VND"))
        tree.insert("", tk.END, values=("Deluxe Room", "6 Bookings", "12 Nights", "70%", "14,400,000 VND"))
        tree.insert("", tk.END, values=("Ocean Suite", "4 Bookings", "8 Nights", "65%", "14,000,000 VND"))

        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        return frame

    # ---------------------------------------------------------
    # TAB 2: MANAGE ROOMS (Quản lý Phòng - CRUD)
    # ---------------------------------------------------------
    def _build_manage_rooms_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(top_sec, text="Room Inventory & Status Control", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(side=tk.LEFT)

        btn_add = tk.Button(top_sec, text="➕ Add New Room", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_ACCENT, bd=0, padx=15, pady=6, cursor="hand2", command=self._open_add_room_dialog)
        btn_add.pack(side=tk.RIGHT)

        # Table
        table_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("Room No", "Room Type", "Price/Night", "Capacity", "Status", "Amenities", "Actions")
        self.tree_rooms = ttk.Treeview(table_frame, columns=columns, show="headings", style="Light.Treeview")

        for col in columns:
            self.tree_rooms.heading(col, text=col, anchor=tk.W if col != "Actions" else tk.CENTER)
            self.tree_rooms.column(col, width=110, anchor=tk.W if col != "Actions" else tk.CENTER)

        self.tree_rooms.column("Amenities", width=220)
        self.tree_rooms.pack(fill=tk.BOTH, expand=True)

        self._refresh_rooms_table()
        return card

    def _refresh_rooms_table(self):
        for item in self.tree_rooms.get_children():
            self.tree_rooms.delete(item)
        for r in self.rooms_data:
            self.tree_rooms.insert("", tk.END, values=(
                f"#{r['number']}", r['type'], f"{r['price']:,} VND", f"{r['capacity']} Guests",
                r['status'], r['amenities'], "✏️ Edit / Status"
            ))

    def _open_add_room_dialog(self):
        win = tk.Toplevel(self)
        win.title("Add New Room")
        win.geometry("380x380")
        win.configure(bg=self.COLOR_BG_CARD)
        win.grab_set()

        tk.Label(win, text="Add New Room Record", font=("Helvetica", 11, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(pady=12)

        def make_field(lbl_text):
            f = tk.Frame(win, bg=self.COLOR_BG_CARD)
            f.pack(fill=tk.X, padx=25, pady=4)
            tk.Label(f, text=lbl_text, font=("Helvetica", 9, "bold"), bg=self.COLOR_BG_CARD).pack(anchor="w")
            e = tk.Entry(f, bg=self.COLOR_BG_INPUT, bd=1, relief=tk.SOLID)
            e.pack(fill=tk.X, ipady=4)
            return e

        e_num = make_field("Room Number (e.g. 301):")
        e_type = make_field("Room Type (Standard/Deluxe/Suite):")
        e_price = make_field("Price Per Night (VND):")
        e_cap = make_field("Capacity (Guests):")

        def save():
            try:
                self.rooms_data.append({
                    "number": e_num.get(), "type": e_type.get(),
                    "price": int(e_price.get()), "capacity": int(e_cap.get()),
                    "status": "Available", "amenities": "Wifi, TV, Aircon"
                })
                self._refresh_rooms_table()
                messagebox.showinfo("Success", "New room added successfully!")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric price and capacity.")

        tk.Button(win, text="Save Room", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_ACCENT, bd=0, pady=6, command=save).pack(pady=15, fill=tk.X, padx=25)

    # ---------------------------------------------------------
    # TAB 3: MANAGE USERS (Quản lý Người dùng & Khóa TK)
    # ---------------------------------------------------------
    def _build_manage_users_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(top_sec, text="User Accounts & Permissions", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(side=tk.LEFT)

        btn_add_rec = tk.Button(top_sec, text="➕ Add Receptionist Account", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_ACCENT, bd=0, padx=15, pady=6, cursor="hand2", command=self._open_add_receptionist_dialog)
        btn_add_rec.pack(side=tk.RIGHT)

        table_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("User ID", "Full Name", "Email", "Role", "Status", "Bookings", "Control Action")
        self.tree_users = ttk.Treeview(table_frame, columns=columns, show="headings", style="Light.Treeview")

        for col in columns:
            self.tree_users.heading(col, text=col, anchor=tk.W if col != "Control Action" else tk.CENTER)
            self.tree_users.column(col, width=120, anchor=tk.W if col != "Control Action" else tk.CENTER)

        self.tree_users.column("Email", width=180)
        self.tree_users.pack(fill=tk.BOTH, expand=True)

        self.tree_users.bind("<Double-1>", self._toggle_user_lock_status)
        self._refresh_users_table()

        return card

    def _refresh_users_table(self):
        for item in self.tree_users.get_children():
            self.tree_users.delete(item)
        for u in self.users_data:
            action_str = "🔒 Lock / 🔓 Unlock" if u['role'] == "Member" else "Protected Session"
            self.tree_users.insert("", tk.END, iid=u["id"], values=(
                u['id'], u['name'], u['email'], u['role'], u['status'], f"{u['bookings']} History", action_str
            ))

    def _toggle_user_lock_status(self, event):
        uid = self.tree_users.focus()
        user = next((u for u in self.users_data if u["id"] == uid), None)
        if user and user["role"] == "Member":
            user["status"] = "Locked" if user["status"] == "Active" else "Active"
            self._refresh_users_table()
            messagebox.showinfo("Status Updated", f"Account '{user['name']}' is now {user['status']}.")

    def _open_add_receptionist_dialog(self):
        win = tk.Toplevel(self)
        win.title("Create Receptionist Account")
        win.geometry("360x300")
        win.configure(bg=self.COLOR_BG_CARD)
        win.grab_set()

        tk.Label(win, text="Create Receptionist Account", font=("Helvetica", 11, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(pady=12)

        def make_field(lbl_text):
            f = tk.Frame(win, bg=self.COLOR_BG_CARD)
            f.pack(fill=tk.X, padx=25, pady=4)
            tk.Label(f, text=lbl_text, font=("Helvetica", 9, "bold"), bg=self.COLOR_BG_CARD).pack(anchor="w")
            e = tk.Entry(f, bg=self.COLOR_BG_INPUT, bd=1, relief=tk.SOLID)
            e.pack(fill=tk.X, ipady=4)
            return e

        e_name = make_field("Full Name:")
        e_email = make_field("Email Address:")
        e_pass = make_field("Password:")

        def save():
            new_id = f"REC-00{len(self.users_data)+1}"
            self.users_data.append({"id": new_id, "name": e_name.get(), "email": e_email.get(), "role": "Receptionist", "status": "Active", "bookings": 0})
            self._refresh_users_table()
            messagebox.showinfo("Success", f"Receptionist Account '{e_name.get()}' Created!")
            win.destroy()

        tk.Button(win, text="Create Account", font=("Helvetica", 9, "bold"), fg="white", bg=self.COLOR_ACCENT, bd=0, pady=6, command=save).pack(pady=15, fill=tk.X, padx=25)

    # ---------------------------------------------------------
    # TAB 4: MANAGE BOOKINGS (Quản lý Đặt phòng & Hủy khẩn cấp)
    # ---------------------------------------------------------
    def _build_manage_bookings_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(top_sec, text="All Reservations Overview & Emergency Controls", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(side=tk.LEFT)

        table_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("Booking ID", "Guest Name", "Assigned Room", "Dates", "Total Paid", "Status", "Emergency Override")
        self.tree_all_bk = ttk.Treeview(table_frame, columns=columns, show="headings", style="Light.Treeview")

        for col in columns:
            self.tree_all_bk.heading(col, text=col, anchor=tk.W if col != "Emergency Override" else tk.CENTER)
            self.tree_all_bk.column(col, width=120, anchor=tk.W if col != "Emergency Override" else tk.CENTER)

        self.tree_all_bk.column("Dates", width=180)
        self.tree_all_bk.pack(fill=tk.BOTH, expand=True)

        self.tree_all_bk.bind("<Double-1>", self._emergency_cancel_booking)
        self._refresh_bookings_table()

        return card

    def _refresh_bookings_table(self):
        for item in self.tree_all_bk.get_children():
            self.tree_all_bk.delete(item)
        for b in self.all_bookings:
            self.tree_all_bk.insert("", tk.END, iid=b["id"], values=(
                b['id'], b['guest'], b['room'], b['dates'], f"{b['total']:,} VND", b['status'], "🚨 Emergency Cancel & Refund"
            ))

    def _emergency_cancel_booking(self, event):
        bid = self.tree_all_bk.focus()
        b = next((x for x in self.all_bookings if x["id"] == bid), None)
        if b:
            if messagebox.askyesno("Emergency Override", f"Cancel booking '{bid}' and trigger 100% full refund due to special reasons (Disaster/Emergency)?"):
                b["status"] = "Cancelled & Refunded"
                self._refresh_bookings_table()

    # ---------------------------------------------------------
    # TAB 5: MANAGE REVIEWS (Quản lý Đánh giá & Spam)
    # ---------------------------------------------------------
    def _build_manage_reviews_view(self):
        card = tk.Frame(self.view_container, bg=self.COLOR_BG_CARD, highlightthickness=1, highlightbackground=self.COLOR_BORDER)

        top_sec = tk.Frame(card, bg=self.COLOR_BG_CARD)
        top_sec.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(top_sec, text="Customer Reviews Moderation", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg=self.COLOR_BG_CARD).pack(side=tk.LEFT)

        table_frame = tk.Frame(card, bg=self.COLOR_BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("Review ID", "Guest", "Room", "Rating", "Comment", "Status", "Action")
        self.tree_reviews = ttk.Treeview(table_frame, columns=columns, show="headings", style="Light.Treeview")

        for col in columns:
            self.tree_reviews.heading(col, text=col, anchor=tk.W if col != "Action" else tk.CENTER)
            self.tree_reviews.column(col, width=110, anchor=tk.W if col != "Action" else tk.CENTER)

        self.tree_reviews.column("Comment", width=250)
        self.tree_reviews.pack(fill=tk.BOTH, expand=True)

        self.tree_reviews.bind("<Double-1>", self._moderate_review)
        self._refresh_reviews_table()

        return card

    def _refresh_reviews_table(self):
        for item in self.tree_reviews.get_children():
            self.tree_reviews.delete(item)
        for r in self.reviews_data:
            self.tree_reviews.insert("", tk.END, iid=r["id"], values=(
                r['id'], r['guest'], r['room'], r['rating'], r['comment'], r['status'], "🗑️ Delete Spam / Hide"
            ))

    def _moderate_review(self, event):
        rid = self.tree_reviews.focus()
        r = next((x for x in self.reviews_data if x["id"] == rid), None)
        if r:
            if messagebox.askyesno("Review Moderation", f"Permanently delete/hide review '{rid}' as inappropriate/spam?"):
                self.reviews_data.remove(r)
                self._refresh_reviews_table()

if __name__ == "__main__":
    app = AdminHotelApp()
    app.mainloop()