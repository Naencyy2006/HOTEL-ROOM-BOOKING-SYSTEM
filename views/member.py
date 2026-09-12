import os
import sys
import datetime

# Tự động thêm đường dẫn gốc project để import các gói services/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Import các Backend Services
try:
    from services import (
        booking_service,
        payment_service,
        cancellation_service,
        user_service,
        room_service,
        review_service
    )
except ImportError:
    booking_service = None
    payment_service = None
    cancellation_service = None
    user_service = None
    room_service = None
    review_service = None

# ============================================================
# HỆ THỐNG MÀU SẮC & PHÔNG CHỮ PASTEL TÍM
# ============================================================
COLOR_MAIN_BG = "#F5EFFF"   # Nền chính
COLOR_SIDEBAR = "#E5D9F2"   # Nền sidebar
COLOR_BUTTON = "#CDC1FF"    # Nút bấm thường
COLOR_ACCENT = "#A594F9"    # Nút chính / Mục đang chọn (Primary Accent)
ACCENT2 = COLOR_ACCENT
COLOR_TEXT = "#3B2F63"      # Chữ tối tương phản cao trên nền tím nhạt
COLOR_WHITE = "#FFFFFF"     # Nền thẻ, popup & chữ nổi bật trên Accent

# Các màu bổ trợ cho Trạng thái / Cảnh báo (Đã đồng bộ với DB Status)
COLOR_SUCCESS = "#2E7D32"   # Completed / Paid
COLOR_SUCCESS_BG = "#E8F5E9"
COLOR_INFO = "#0288D1"      # Checked-in / Confirmed
COLOR_INFO_BG = "#E1F5FE"
COLOR_WARNING = "#D84315"   # Pending Payment / Pending
COLOR_WARNING_BG = "#FBE9E7"
COLOR_DANGER = "#C62828"    # Cancelled
COLOR_DANGER_BG = "#FFEBEE"
COLOR_STAR_ACTIVE = "#FFB300" # Vàng sao đánh giá

FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 15, "bold")


class MemberDashboard(tk.Frame):
    def __init__(self, master, conn, user, on_logout=None, **kwargs):
        super().__init__(master, bg=COLOR_MAIN_BG, **kwargs)
        self.conn = conn
        self.user = user or self._get_fallback_user()
        self.on_logout = on_logout
        self.current_tab = "dashboard"
        self._sidebar_buttons = {}

        # Khởi tạo Style đồng bộ cho các Widget TTK
        self._setup_ttk_styles()

        # Đồng bộ dữ liệu người dùng từ DB
        self._sync_user_profile_from_db()

        # Dựng giao diện chính
        self._build_top_navbar()
        self._build_main_layout()

        # Mặc định hiển thị Màn hình Dashboard
        self.show_dashboard()

    # ============================================================
    # 0. CẤU HÌNH STYLE & ĐỒNG BỘ DỮ LIỆU NỀN
    # ============================================================
    def _setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground=COLOR_WHITE,
            background=COLOR_SIDEBAR,
            foreground=COLOR_TEXT,
            bordercolor=COLOR_BUTTON,
            lightcolor=COLOR_BUTTON,
            darkcolor=COLOR_BUTTON,
            arrowcolor=COLOR_TEXT
        )
        style.map("TCombobox", fieldbackground=[("readonly", COLOR_WHITE)])

        style.configure(
            "Vertical.TScrollbar",
            background=COLOR_BUTTON,
            troughcolor=COLOR_MAIN_BG,
            bordercolor=COLOR_MAIN_BG,
            arrowcolor=COLOR_TEXT,
            relief="flat"
        )
        style.map("Vertical.TScrollbar", background=[("active", COLOR_ACCENT)])
        style.configure("TSeparator", background=COLOR_BUTTON)

    def _get_fallback_user(self):
        """Khớp chính xác cấu hình bảng `users` trong schema.sql"""
        return {
            "user_id": 9,
            "full_name": "Phạm Trần Bảo Ngọc",
            "email": "ngoc.pham@gmail.com",
            "phone": "0912998877",
            "gender": "Nữ",
            "year_of_birth": 1997,
            "role": "Member",
            "status": "Active"
        }

    def _sync_user_profile_from_db(self):
        if self.conn and user_service and hasattr(user_service, 'get_user_by_id'):
            try:
                db_user = user_service.get_user_by_id(self.conn, self.user.get("user_id"))
                if db_user:
                    self.user.update(db_user)
            except Exception as e:
                print(f"[Warning] Sync user profile error: {e}")

    def _refresh_top_navbar_user_label(self):
        user_name = self.user.get("full_name", "Member")
        role = self.user.get("role", "Member")
        self.user_lbl.configure(text=f"🔔  👤 {user_name} ({role})")

    def _get_all_member_bookings(self):
        """Khớp dữ liệu seed.sql cho user_id = 9"""
        if self.conn and booking_service and hasattr(booking_service, 'list_bookings_by_member'):
            try:
                res = booking_service.list_bookings_by_member(self.conn, self.user["user_id"])
                if res is not None:
                    return res
            except Exception as e:
                print(f"[Warning] Sync bookings from DB error: {e}")

        # Dữ liệu fallback chuẩn theo seed.sql
        return [
            {
                "booking_id": 2008,
                "user_id": 9,
                "room_id": "302",
                "room_type_id": 3,
                "type_name": "Deluxe Suite",
                "room_number": "302",
                "check_in": datetime.date(2026, 9, 11),
                "check_out": datetime.date(2026, 9, 14),
                "total_price": 4500000.00,
                "status": "Checked-in",
                "capacity": 2,
                "guest_name": self.user.get("full_name", "Phạm Trần Bảo Ngọc")
            },
            {
                "booking_id": 2012,
                "user_id": 9,
                "room_id": None,
                "room_type_id": 2,
                "type_name": "Standard Double",
                "room_number": "N/A",
                "check_in": datetime.date(2026, 9, 25),
                "check_out": datetime.date(2026, 9, 28),
                "total_price": 2400000.00,
                "status": "Confirmed",
                "capacity": 2,
                "guest_name": self.user.get("full_name", "Phạm Trần Bảo Ngọc")
            }
        ]

    # ============================================================
    # 1. TOP NAVBAR (THANH TIÊU ĐỀ TRÊN CÙNG)
    # ============================================================
    def _build_top_navbar(self):
        navbar = tk.Frame(self, bg=COLOR_ACCENT, height=55)
        navbar.pack(side="top", fill="x")
        navbar.pack_propagate(False)

        brand_lbl = tk.Label(
            navbar, text="🏨  HOTEL BOOKING SYSTEM", bg=COLOR_ACCENT, fg=COLOR_WHITE,
            font=FONT_TITLE, padx=20
        )
        brand_lbl.pack(side="left")

        user_info_frame = tk.Frame(navbar, bg=COLOR_ACCENT)
        user_info_frame.pack(side="right", padx=20)

        user_name = self.user.get("full_name", "Member")
        role = self.user.get("role", "Member")
        self.user_lbl = tk.Label(
            user_info_frame, text=f"🔔  👤 {user_name} ({role})",
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD
        )
        self.user_lbl.pack(side="left", padx=(0, 15))

        btn_logout = tk.Button(
            user_info_frame, text="Logout", command=self._logout,
            bg=COLOR_DANGER, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat",
            activebackground="#9A0007", activeforeground=COLOR_WHITE,
            padx=12, pady=4, cursor="hand2"
        )
        btn_logout.pack(side="right")

    # ============================================================
    # 2. MAIN LAYOUT & SIDEBAR NAVIGATION
    # ============================================================
    def _build_main_layout(self):
        body_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        body_frame.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(body_frame, bg=COLOR_SIDEBAR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="MEMBER MENU", bg=COLOR_SIDEBAR, fg=COLOR_TEXT,
            font=FONT_BOLD, pady=15, padx=20, anchor="w"
        ).pack(fill="x")

        menu_items = [
            ("dashboard", "📊   Dashboard", self.show_dashboard),
            ("search", "🔍   Search Rooms", self.show_search),
            ("my_bookings", "📅   My Bookings", self.show_my_bookings),
            ("history", "📖   Booking History", self.show_history),
            ("profile", "👤   My Profile", self.show_profile),
        ]

        for tab_id, text, cmd in menu_items:
            btn = tk.Button(
                sidebar, text=text, command=cmd, bg=COLOR_SIDEBAR,
                fg=COLOR_TEXT, font=FONT_BOLD, relief="flat",
                anchor="w", padx=20, pady=12, cursor="hand2",
                activebackground=COLOR_ACCENT,
                activeforeground=COLOR_WHITE
            )
            btn.pack(fill="x")
            self._sidebar_buttons[tab_id] = btn

        logout_btn = tk.Button(
            sidebar, text="🚪   Logout", command=self._logout,
            bg=COLOR_SIDEBAR, fg=COLOR_DANGER, font=FONT_BOLD, relief="flat",
            anchor="w", padx=20, pady=12, cursor="hand2",
            activebackground=COLOR_DANGER_BG, activeforeground=COLOR_DANGER
        )
        logout_btn.pack(side="bottom", fill="x", pady=10)

        self.content_container = tk.Frame(body_frame, bg=COLOR_MAIN_BG)
        self.content_container.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_container, bg=COLOR_MAIN_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_container, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=COLOR_MAIN_BG)

        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.bind("<Enter>", self._enable_mousewheel)
        self.canvas.bind("<Leave>", self._disable_mousewheel)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=30, pady=20)
        self.scrollbar.pack(side="right", fill="y")

    def _enable_mousewheel(self, _event=None):
        self.canvas.focus_set()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _disable_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        event_num = getattr(event, "num", None)
        if event_num == 4:
            direction = -1
        elif event_num == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")

    def _set_active_tab(self, active_tab_id):
        self.current_tab = active_tab_id
        for tab_id, btn in self._sidebar_buttons.items():
            if tab_id == active_tab_id:
                btn.configure(bg=COLOR_ACCENT, fg=COLOR_WHITE)
            else:
                btn.configure(bg=COLOR_SIDEBAR, fg=COLOR_TEXT)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _logout(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if confirm:
            if self.on_logout:
                self.on_logout()
            else:
                self.master.destroy()

    # ============================================================
    # MÀN HÌNH 1: DASHBOARD OVERVIEW
    # ============================================================
    def show_dashboard(self):
        self._set_active_tab("dashboard")
        self._clear_content()

        tk.Label(
            self.content, text=f"Welcome back, {self.user.get('full_name', 'Member')}! 👋",
            bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", pady=(0, 5))
        tk.Label(
            self.content, text="Manage and track your bookings here.",
            bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_NORMAL
        ).pack(anchor="w", pady=(0, 20))

        stats_frame = tk.Frame(self.content, bg=COLOR_MAIN_BG)
        stats_frame.pack(fill="x", pady=(0, 20))

        bookings = self._get_all_member_bookings()
        # Đã cập nhật bao gồm cả Checked-in và Pending Payment
        active_cnt = len([b for b in bookings if b["status"] in ("Confirmed", "Pending Payment", "Checked-in", "Pending")])
        completed_cnt = len([b for b in bookings if b["status"] == "Completed"])
        total_spent = sum([b["total_price"] for b in bookings if b["status"] in ("Confirmed", "Completed", "Checked-in")])

        self._render_stat_card(stats_frame, "📅 Active Bookings", str(active_cnt), COLOR_ACCENT)
        self._render_stat_card(stats_frame, "✅ Completed Stays", str(completed_cnt), COLOR_SUCCESS)
        self._render_stat_card(stats_frame, "💰 Total Spent", f"{total_spent:,.0f} VND", COLOR_WARNING)

        quick_card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=20)
        quick_card.pack(fill="x", pady=10)

        tk.Label(quick_card, text="Quick Actions", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 10))
        btn_box = tk.Frame(quick_card, bg=COLOR_WHITE)
        btn_box.pack(anchor="w")

        tk.Button(
            btn_box, text="🔍 Find a Room", command=self.show_search,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat", padx=15, pady=8, cursor="hand2",
            activebackground="#8B77E8", activeforeground=COLOR_WHITE
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_box, text="📅 View My Bookings", command=self.show_my_bookings,
            bg=COLOR_BUTTON, fg=COLOR_TEXT, font=FONT_BOLD, relief="flat", padx=15, pady=8, cursor="hand2",
            activebackground=COLOR_ACCENT, activeforeground=COLOR_WHITE
        ).pack(side="left")

    def _render_stat_card(self, parent, title, val, accent_color):
        card = tk.Frame(parent, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=15)
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(card, text=title, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack(anchor="w")
        tk.Label(card, text=val, bg=COLOR_WHITE, fg=accent_color, font=FONT_TITLE).pack(anchor="w", pady=(5, 0))

    # ============================================================
    # MÀN HÌNH 2: SEARCH ROOMS (Đồng bộ cột với room_types)
    # ============================================================
    def show_search(self):
        self._set_active_tab("search")
        self._clear_content()

        tk.Label(self.content, text="🔍 Search & Book Rooms", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 15))

        filter_card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=20)
        filter_card.pack(fill="x", pady=(0, 20))

        tk.Label(filter_card, text="FIND YOUR PERFECT ROOM", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 15))

        form_grid = tk.Frame(filter_card, bg=COLOR_WHITE)
        form_grid.pack(fill="x")

        tk.Label(form_grid, text="Check-in Date", bg=COLOR_WHITE, font=FONT_NORMAL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(form_grid, text="Check-out Date", bg=COLOR_WHITE, font=FONT_NORMAL, fg=COLOR_TEXT).grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(form_grid, text="Guests", bg=COLOR_WHITE, font=FONT_NORMAL, fg=COLOR_TEXT).grid(row=0, column=2, sticky="w", padx=5)
        tk.Label(form_grid, text="Min Price (VND)", bg=COLOR_WHITE, font=FONT_NORMAL, fg=COLOR_TEXT).grid(row=0, column=3, sticky="w", padx=5)
        tk.Label(form_grid, text="Max Price (VND)", bg=COLOR_WHITE, font=FONT_NORMAL, fg=COLOR_TEXT).grid(row=0, column=4, sticky="w", padx=5)

        self.entry_cin = tk.Entry(form_grid, font=FONT_NORMAL, width=13, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
        self.entry_cin.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.entry_cin.grid(row=1, column=0, padx=5, pady=5)

        self.entry_cout = tk.Entry(form_grid, font=FONT_NORMAL, width=13, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
        self.entry_cout.insert(0, (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
        self.entry_cout.grid(row=1, column=1, padx=5, pady=5)

        self.combo_guests = ttk.Combobox(form_grid, values=["1 Guest", "2 Guests", "3 Guests", "4+ Guests"], width=10, state="readonly")
        self.combo_guests.current(1)
        self.combo_guests.grid(row=1, column=2, padx=5, pady=5)

        self.entry_min_price = tk.Entry(form_grid, font=FONT_NORMAL, width=12, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
        self.entry_min_price.grid(row=1, column=3, padx=5, pady=5)

        self.entry_max_price = tk.Entry(form_grid, font=FONT_NORMAL, width=12, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
        self.entry_max_price.grid(row=1, column=4, padx=5, pady=5)

        btn_search = tk.Button(
            filter_card, text="SEARCH ROOMS", command=self._do_search_rooms,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat", padx=20, pady=8, cursor="hand2",
            activebackground="#8B77E8", activeforeground=COLOR_WHITE
        )
        btn_search.pack(anchor="e", pady=(15, 0))

        self.results_container = tk.Frame(self.content, bg=COLOR_MAIN_BG)
        self.results_container.pack(fill="x", pady=10)

        self._do_search_rooms()

    def _do_search_rooms(self):
        for w in self.results_container.winfo_children():
            w.destroy()

        tk.Label(self.results_container, text="Available Rooms", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 10))

        rooms = []
        if self.conn and room_service and hasattr(room_service, 'search_rooms'):
            try:
                cin = self.entry_cin.get()
                cout = self.entry_cout.get()
                rooms = room_service.search_rooms(self.conn, check_in=cin, check_out=cout)
            except Exception as e:
                print(f"[Warning] Room search DB error: {e}")

        # Fallback dữ liệu từ seed.sql (bảng room_types)
        if not rooms:
            rooms = [
                {"room_type_id": 1, "type_name": "Standard Single", "price_per_night": 500000.00, "capacity": 1, "description": "Cozy standard single room with essential amenities."},
                {"room_type_id": 2, "type_name": "Standard Double", "price_per_night": 800000.00, "capacity": 2, "description": "Standard double room suitable for two guests."},
                {"room_type_id": 3, "type_name": "Deluxe Suite", "price_per_night": 1500000.00, "capacity": 2, "description": "Premium suite with city views and modern amenities."},
                {"room_type_id": 4, "type_name": "Executive VIP", "price_per_night": 3000000.00, "capacity": 4, "description": "Spacious family VIP room with a living room and two bedrooms."}
            ]

        for room in rooms:
            self._render_room_search_card(room)

    def _render_room_search_card(self, room):
        card = tk.Frame(self.results_container, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=15, pady=15)
        card.pack(fill="x", pady=6)

        left = tk.Frame(card, bg=COLOR_WHITE)
        left.pack(side="left", fill="both", expand=True)

        # Đã đồng bộ trường với DB room_types (type_name, price_per_night)
        room_name = room.get("type_name") or room.get("name", "Standard Room")
        capacity = room.get("capacity", 2)
        price = room.get("price_per_night") or room.get("price", 1000000)
        desc = room.get("description") or room.get("desc", "Room equipped with complete amenities.")

        tk.Label(left, text=room_name, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w")
        tk.Label(left, text=f"Capacity: {capacity} Guests", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack(anchor="w", pady=(2, 5))
        tk.Label(left, text=desc, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack(anchor="w")

        right = tk.Frame(card, bg=COLOR_WHITE)
        right.pack(side="right", fill="y", padx=(15, 0))

        tk.Label(right, text=f"{price:,.0f} VND / night", bg=COLOR_WHITE, fg=COLOR_SUCCESS, font=FONT_BOLD).pack(anchor="e", pady=(0, 10))
        tk.Button(
            right, text="Book Now", bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat", padx=15, pady=6, cursor="hand2",
            activebackground="#8B77E8", activeforeground=COLOR_WHITE,
            command=lambda: self._trigger_book_room(room)
        ).pack(anchor="e")

    def _trigger_book_room(self, room):
        room_name = room.get("type_name") or room.get("name", "Room")
        price = room.get("price_per_night") or room.get("price", 1000000)
        confirm = messagebox.askyesno("Confirm Booking", f"Would you like to book {room_name} for {price:,.0f} VND/night?")
        
        if confirm:
            if self.conn and booking_service and hasattr(booking_service, 'create_booking'):
                try:
                    booking_service.create_booking(
                        self.conn,
                        user_id=self.user["user_id"],
                        room_type_id=room.get("room_type_id", room.get("id")),
                        check_in=self.entry_cin.get(),
                        check_out=self.entry_cout.get()
                    )
                except Exception as e:
                    print(f"[Warning] Booking DB Insert error: {e}")

            messagebox.showinfo(
                "Booking Created",
                "Your booking has been created (Status: Pending Payment).\nPlease open 'My Bookings' to complete payment."
            )
            self.show_my_bookings()

    # ============================================================
    # MÀN HÌNH 3: MY ACTIVE BOOKINGS (Đã bổ sung Checked-in)
    # ============================================================
    def show_my_bookings(self):
        self._set_active_tab("my_bookings")
        self._clear_content()

        tk.Label(self.content, text="📅 My Active Bookings", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 15))

        # Đã cập nhật lọc bao gồm Checked-in và Pending
        bookings = [
            b for b in self._get_all_member_bookings()
            if b["status"] in ("Confirmed", "Pending Payment", "Checked-in", "Pending")
        ]

        if not bookings:
            empty_card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=30)
            empty_card.pack(fill="x")
            tk.Label(empty_card, text="You have no active bookings.", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack()
            return

        for b in bookings:
            self._render_active_booking_card(b)

    def _render_active_booking_card(self, b):
        card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=18)
        card.pack(fill="x", pady=8)

        top = tk.Frame(card, bg=COLOR_WHITE)
        top.pack(fill="x")

        booking_code = b.get("booking_code", f"#BK-{b['booking_id']}")
        tk.Label(top, text=f"BOOKING ID: {booking_code}", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD).pack(side="left")

        # Cấu hình Badge đồng bộ trạng thái từ DB
        if b["status"] == "Checked-in":
            badge_bg = COLOR_INFO_BG
            badge_fg = COLOR_INFO
            status_text = "● CHECKED-IN"
        elif b["status"] == "Confirmed":
            badge_bg = COLOR_SUCCESS_BG
            badge_fg = COLOR_SUCCESS
            status_text = "● CONFIRMED"
        else:
            badge_bg = COLOR_WARNING_BG
            badge_fg = COLOR_WARNING
            status_text = f"● {b['status'].upper()}"

        badge = tk.Label(top, text=status_text, bg=badge_bg, fg=badge_fg, font=FONT_BOLD, padx=10, pady=3)
        badge.pack(side="right")

        room_name = b.get("type_name", b.get("room_type_name", f"Room Type #{b['room_type_id']}"))
        room_num = b.get("room_number", b.get("room_id", "N/A"))
        title_text = f"{room_name} (Room {room_num})" if room_num and room_num != "N/A" else room_name

        tk.Label(card, text=title_text, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(8, 4))

        cin_str = b['check_in'].strftime("%d %b %Y") if isinstance(b['check_in'], (datetime.date, datetime.datetime)) else str(b['check_in'])
        cout_str = b['check_out'].strftime("%d %b %Y") if isinstance(b['check_out'], (datetime.date, datetime.datetime)) else str(b['check_out'])

        tk.Label(
            card, text=f"📅 Check-in: {cin_str} (14:00)   →   Check-out: {cout_str} (12:00)",
            bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL
        ).pack(anchor="w", pady=(0, 4))

        guest_name = b.get("guest_name", self.user.get("full_name", "Member"))
        tk.Label(
            card, text=f"👤 Guest: {guest_name}      💰 Total: {b['total_price']:,.0f} VND",
            bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL
        ).pack(anchor="w", pady=(0, 8))

        actions = tk.Frame(card, bg=COLOR_WHITE)
        actions.pack(fill="x", pady=(10, 0))

        if b["status"] == "Pending Payment":
            tk.Button(
                actions, text="Pay Now", bg=COLOR_SUCCESS, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat",
                padx=18, pady=6, cursor="hand2", activebackground="#1B5E20", activeforeground=COLOR_WHITE,
                command=lambda: self._pay_now(b)
            ).pack(side="right", padx=(5, 0))

            tk.Button(
                actions, text="Cancel Request", bg=COLOR_BUTTON, fg=COLOR_TEXT, font=FONT_NORMAL, relief="flat",
                padx=15, pady=6, cursor="hand2", activebackground=COLOR_SIDEBAR, activeforeground=COLOR_TEXT,
                command=lambda: self._cancel_booking(b)
            ).pack(side="right", padx=5)
        elif b["status"] == "Confirmed":
            tk.Button(
                actions, text="Cancel Booking", bg=COLOR_DANGER, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat",
                padx=18, pady=6, cursor="hand2", activebackground="#9A0007", activeforeground=COLOR_WHITE,
                command=lambda: self._cancel_booking(b)
            ).pack(side="right")
        elif b["status"] == "Checked-in":
            tk.Label(actions, text="ℹ️ You are currently checked in to this room", bg=COLOR_WHITE, fg=COLOR_INFO, font=FONT_BOLD).pack(side="right")

    # ============================================================
    # MÀN HÌNH 4: BOOKING HISTORY & REVIEWS
    # ============================================================
    def show_history(self):
        self._set_active_tab("history")
        self._clear_content()

        tk.Label(self.content, text="📖 Booking History", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 15))

        history = self._get_all_member_bookings()

        if not history:
            empty_card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=30)
            empty_card.pack(fill="x")
            tk.Label(empty_card, text="There is no booking history.", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack()
            return

        for b in history:
            self._render_history_card(b)

        self.content.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _render_history_card(self, b):
        card = tk.Frame(self.content, bg=COLOR_WHITE, highlightbackground=COLOR_BUTTON, highlightthickness=1, padx=20, pady=15)
        card.pack(fill="x", pady=6)

        top = tk.Frame(card, bg=COLOR_WHITE)
        top.pack(fill="x")

        room_name = b.get("type_name", b.get("room_type_name", f"Room Type #{b['room_type_id']}"))
        tk.Label(top, text=room_name, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(side="left")

        right_info = tk.Frame(top, bg=COLOR_WHITE)
        right_info.pack(side="right")

        status_styles = {
            "Completed": ("● Completed", COLOR_SUCCESS_BG, COLOR_SUCCESS),
            "Cancelled": ("● Cancelled", COLOR_DANGER_BG, COLOR_DANGER),
            "Confirmed": ("● Confirmed", COLOR_INFO_BG, COLOR_INFO),
            "Checked-in": ("● Checked-in", COLOR_INFO_BG, COLOR_INFO),
            "Pending Payment": ("● Pending Payment", COLOR_WARNING_BG, COLOR_WARNING),
            "Pending": ("● Pending", COLOR_WARNING_BG, COLOR_WARNING),
        }
        status_text, status_bg, status_fg = status_styles.get(
            b["status"], (f"● {b['status']}", COLOR_BUTTON, COLOR_TEXT)
        )
        badge_lbl = tk.Label(right_info, text=status_text, bg=status_bg, fg=status_fg, font=FONT_BOLD, padx=8, pady=2)
        badge_lbl.pack(side="right", padx=(10, 0))

        tk.Label(right_info, text=f"{b['total_price']:,.0f} VND", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD).pack(side="right")

        cin_str = b['check_in'].strftime("%d %b %Y") if isinstance(b['check_in'], (datetime.date, datetime.datetime)) else str(b['check_in'])
        cout_str = b['check_out'].strftime("%d %b %Y") if isinstance(b['check_out'], (datetime.date, datetime.datetime)) else str(b['check_out'])
        tk.Label(card, text=f"Dates: {cin_str} - {cout_str}", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack(anchor="w", pady=(4, 0))

        if b["status"] == "Completed":
            tk.Button(
                card, text="⭐ Write Review", bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat",
                padx=15, pady=5, cursor="hand2", activebackground="#8B77E8", activeforeground=COLOR_WHITE,
                command=lambda: self._open_review_dialog(b)
            ).pack(anchor="e", pady=(8, 0))

    def _open_review_dialog(self, booking):
        """
        TODO: gọi review_service (nếu có) để INSERT vào bảng reviews.
        Ở đây chỉ dựng dialog nhập rating + comment theo đúng use-case
        "Write review" (mục 4.4.9).
        """
        win = tk.Toplevel(self)
        win.title("Write Review")
        win.configure(bg="white")

        tk.Label(win, text="Rating (1-5):", bg="white").pack(pady=(10, 0))
        rating_var = tk.IntVar(value=5)
        tk.Spinbox(win, from_=1, to=5, textvariable=rating_var).pack()

        tk.Label(win, text="Comment:", bg="white").pack(pady=(10, 0))
        comment_box = tk.Text(win, width=40, height=5)
        comment_box.pack(padx=10)

        def submit():
            # TODO: review_service.create_review(conn, user_id, booking, rating, comment)
            messagebox.showinfo("Cảm ơn!", "Đánh giá của bạn đã được ghi nhận.")
            win.destroy()

        tk.Button(win, text="Submit", bg=ACCENT2, fg="white", command=submit).pack(pady=10)

    # ============================================================
    # MÀN HÌNH 5: MY PROFILE (Đồng bộ chuẩn schema.sql)
    # ============================================================
    def show_profile(self):
        self._set_active_tab("profile")

        self._clear_content()

        card = tk.Frame(
            self.content,
            bg=COLOR_WHITE,
            highlightbackground=COLOR_BUTTON,
            highlightthickness=1,
            padx=25,
            pady=25,
        )
        card.pack(fill="x")

        top_profile = tk.Frame(card, bg=COLOR_WHITE)
        top_profile.pack(fill="x", pady=(0, 20))

        avatar_lbl = tk.Label(top_profile, text="👤", font=("Segoe UI", 36), bg=COLOR_SIDEBAR, fg=COLOR_TEXT, width=3, height=1)
        avatar_lbl.pack(side="left", padx=(0, 15))

        info_sub = tk.Frame(top_profile, bg=COLOR_WHITE)
        info_sub.pack(side="left")

        self.lbl_profile_name = tk.Label(info_sub, text=self.user.get("full_name", "Member Name"), bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE)
        self.lbl_profile_name.pack(anchor="w")

        self.lbl_profile_email = tk.Label(info_sub, text=self.user.get("email", "email@example.com"), bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL)
        self.lbl_profile_email.pack(anchor="w")

        role_tag = tk.Label(info_sub, text=self.user.get("role", "MEMBER").upper(), bg=COLOR_BUTTON, fg=COLOR_TEXT, font=FONT_BOLD, padx=8, pady=2)
        role_tag.pack(anchor="w", pady=(4, 0))

        self.is_profile_editing = False
        self.btn_edit_profile = tk.Button(
            top_profile, text="✏️ Edit Info", bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat",
            padx=15, pady=6, cursor="hand2", activebackground="#8B77E8", activeforeground=COLOR_WHITE,
            command=self._toggle_edit_profile
        )
        self.btn_edit_profile.pack(side="right")

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=(0, 20))

        tk.Label(card, text="Account Details", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(0, 15))

        details_grid = tk.Frame(card, bg=COLOR_WHITE)
        details_grid.pack(fill="x")

        # Đã đồng bộ loại bỏ trường address và chỉnh year_of_birth thành INT
        fields = [
            ("FULL NAME", "full_name", self.user.get("full_name", "")),
            ("EMAIL ADDRESS", "email", self.user.get("email", "")),
            ("PHONE NUMBER", "phone", self.user.get("phone", "")),
            ("GENDER", "gender", self.user.get("gender", "Male")),
            ("YEAR OF BIRTH", "year_of_birth", self.user.get("year_of_birth", 1997)),
        ]

        self._profile_labels = {}
        self._profile_entries = {}

        for idx, (label_title, key, val) in enumerate(fields):
            row = idx
            lbl_title = tk.Label(details_grid, text=label_title, bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD)
            lbl_title.grid(row=row*2, column=0, sticky="w", pady=(8, 2))

            lbl_val = tk.Label(details_grid, text=str(val), bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL)
            lbl_val.grid(row=row*2+1, column=0, sticky="w", pady=(0, 8))
            self._profile_labels[key] = lbl_val

            entry = tk.Entry(details_grid, font=FONT_NORMAL, width=45, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
            entry.insert(0, str(val))
            self._profile_entries[key] = entry

    def _toggle_edit_profile(self):
        if not self.is_profile_editing:
            self.is_profile_editing = True
            self.btn_edit_profile.configure(text="💾 Save Changes", bg=COLOR_SUCCESS, activebackground="#1B5E20")

            for key, lbl in self._profile_labels.items():
                row = lbl.grid_info()["row"]
                lbl.grid_remove()
                entry = self._profile_entries[key]
                entry.grid(row=row, column=0, sticky="w", pady=(0, 8))
        else:
            self._save_profile()

    def _save_profile(self):
        updated_data = {}

        for key, entry in self._profile_entries.items():
            val = entry.get().strip()
            if key == "year_of_birth":
                if not val.isdigit():
                    messagebox.showerror("Error", "Year of birth must contain numbers only.")
                    entry.focus_set()
                    return
                val = int(val)
                current_year = datetime.date.today().year
                if not 1900 <= val <= current_year:
                    messagebox.showerror(
                        "Error",
                        f"Year of birth must be between 1900 and {current_year}.",
                    )
                    entry.focus_set()
                    return
            updated_data[key] = val

        for key, entry in self._profile_entries.items():
            val = updated_data[key]
            self.user[key] = val
            lbl = self._profile_labels[key]
            lbl.configure(text=str(val))
            entry.grid_remove()
            lbl.grid()

        if self.conn and user_service and hasattr(user_service, 'update_user'):
            try:
                user_service.update_user(self.conn, self.user["user_id"], updated_data)
            except Exception as e:
                print(f"[Warning] Save user profile to DB error: {e}")

        self._refresh_top_navbar_user_label()
        self.lbl_profile_name.configure(text=self.user.get("full_name"))
        self.lbl_profile_email.configure(text=self.user.get("email"))

        self.is_profile_editing = False
        self.btn_edit_profile.configure(text="✏️ Edit Info", bg=COLOR_ACCENT, activebackground="#8B77E8")
        messagebox.showinfo("Success", "Account information was synchronized and updated successfully!")

    # ============================================================
    # POPUP DIALOGS (ĐỒNG BỘ CẢ PHẦN THÊM REVIEWS VỚI ROOM_ID)
    # ============================================================
    def _pay_now(self, booking):
        pay_win = tk.Toplevel(self)
        pay_win.title("Online Payment Gateway")
        pay_win.geometry("420x350")
        pay_win.configure(bg=COLOR_WHITE)
        pay_win.grab_set()

        tk.Label(pay_win, text="💳 PAYMENT GATEWAY", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(pady=(20, 10))

        b_code = booking.get("booking_code", f"#BK-{booking['booking_id']}")
        tk.Label(pay_win, text=f"Booking ID: {b_code}", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack()
        tk.Label(pay_win, text=f"Total Amount: {booking['total_price']:,.0f} VND", bg=COLOR_WHITE, fg=COLOR_SUCCESS, font=FONT_TITLE).pack(pady=10)

        tk.Label(pay_win, text="Choose a payment method:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD).pack(anchor="w", padx=40, pady=(10, 5))

        method_var = tk.StringVar(value="MoMo")
        methods = [("MoMo Wallet", "MoMo"), ("Bank Transfer", "Bank Transfer"), ("Credit Card (Visa/Master)", "Credit Card")]

        for txt, val in methods:
            rb = tk.Radiobutton(
                pay_win, text=txt, value=val, variable=method_var, bg=COLOR_WHITE, fg=COLOR_TEXT,
                activebackground=COLOR_WHITE, selectcolor=COLOR_WHITE, font=FONT_NORMAL
            )
            rb.pack(anchor="w", padx=50, pady=2)

        def confirm_payment():
            selected_method = method_var.get()
            tx_code = f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

            if self.conn and payment_service and hasattr(payment_service, 'process_payment'):
                try:
                    res = payment_service.process_payment(self.conn, booking["booking_id"], selected_method)
                    if isinstance(res, dict) and "transaction_code" in res:
                        tx_code = res["transaction_code"]
                except Exception as e:
                    print(f"[Warning] Payment DB Sync error: {e}")

            booking["status"] = "Confirmed"
            pay_win.destroy()

            messagebox.showinfo(
                "Payment Successful",
                f"✅ Payment completed successfully!\n\n"
                f"Transaction code: {tx_code}\n"
                f"Method: {selected_method}\n"
                f"Amount: {booking['total_price']:,.0f} VND\n"
                f"Booking status: CONFIRMED\n\n"
                f"The electronic receipt has been saved."
            )
            self.show_my_bookings()

        tk.Button(
            pay_win, text="Confirm Payment", command=confirm_payment,
            bg=COLOR_SUCCESS, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat", padx=20, pady=8, cursor="hand2",
            activebackground="#1B5E20", activeforeground=COLOR_WHITE
        ).pack(pady=20)

    def _cancel_booking(self, booking):
        now = datetime.datetime.now()
        cin = booking['check_in']
        if isinstance(cin, datetime.date) and not isinstance(cin, datetime.datetime):
            cin = datetime.datetime.combine(cin, datetime.time(14, 0))

        hours_left = (cin - now).total_seconds() / 3600.0

        if hours_left > 48:
            refund_rate = 1.0
            policy_msg = "Cancel more than 48 hours before check-in: 100% refund."
        elif 24 <= hours_left <= 48:
            refund_rate = 0.5
            policy_msg = "Cancel 24 to 48 hours before check-in: 50% refund (50% cancellation fee)."
        else:
            refund_rate = 0.0
            policy_msg = "Cancel within 24 hours of check-in: 100% fee (no refund)."

        refund_amount = booking['total_price'] * refund_rate

        confirm = messagebox.askyesno(
            "Confirm Booking Cancellation",
            f"Applicable policy:\n{policy_msg}\n\n"
            f"• Booking total: {booking['total_price']:,.0f} VND\n"
            f"• Refund amount: {refund_amount:,.0f} VND\n\n"
            f"Are you sure you want to cancel this booking?"
        )

        if confirm:
            if self.conn and cancellation_service and hasattr(cancellation_service, 'cancel_booking'):
                try:
                    cancellation_service.cancel_booking(self.conn, booking["booking_id"])
                except Exception as e:
                    print(f"[Warning] Cancel booking DB Sync error: {e}")

            booking["status"] = "Cancelled"
            messagebox.showinfo("Booking Cancelled", f"Booking cancelled successfully.\nRefund amount: {refund_amount:,.0f} VND.")
            self.show_my_bookings()

    def _open_review_dialog(self, booking):
        review_win = tk.Toplevel(self)
        review_win.title("Write Review")
        review_win.geometry("400x380")
        review_win.configure(bg=COLOR_WHITE)
        review_win.grab_set()

        room_name = booking.get("type_name", booking.get("room_type_name", f"Room Type #{booking['room_type_id']}"))
        tk.Label(review_win, text="⭐ WRITE A REVIEW", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_TITLE).pack(pady=(15, 5))
        tk.Label(review_win, text=f"Room: {room_name}", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_NORMAL).pack()

        rating_var = tk.IntVar(value=5)

        tk.Label(review_win, text="Your review:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD).pack(pady=(15, 5))
        stars_frame = tk.Frame(review_win, bg=COLOR_WHITE)
        stars_frame.pack()

        star_btns = []

        def update_stars(val):
            rating_var.set(val)
            for idx, btn in enumerate(star_btns):
                if idx < val:
                    btn.configure(fg=COLOR_STAR_ACTIVE, text="★")
                else:
                    btn.configure(fg=COLOR_BUTTON, text="★")

        for i in range(1, 6):
            btn = tk.Button(
                stars_frame, text="★", font=("Segoe UI", 20), bg=COLOR_WHITE, fg=COLOR_STAR_ACTIVE,
                activebackground=COLOR_WHITE, relief="flat", bd=0, cursor="hand2", command=lambda v=i: update_stars(v)
            )
            btn.pack(side="left", padx=2)
            star_btns.append(btn)

        tk.Label(review_win, text="Detailed comments:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=FONT_BOLD).pack(anchor="w", padx=30, pady=(15, 5))
        comment_box = tk.Text(review_win, width=40, height=4, font=FONT_NORMAL, bg=COLOR_WHITE, fg=COLOR_TEXT, relief="solid", bd=1)
        comment_box.pack(padx=30)

        def submit_review():
            comment = comment_box.get("1.0", "end-1c").strip()
            if not comment:
                messagebox.showwarning("Notice", "Please enter your review.")
                return

            if not self.conn:
                messagebox.showerror("Review Error", "Database connection is unavailable.", parent=review_win)
                return
            if not review_service or not hasattr(review_service, "add_review"):
                messagebox.showerror("Review Error", "Review service is unavailable.", parent=review_win)
                return

            try:
                review_service.add_review(
                    self.conn,
                    user_id=self.user["user_id"],
                    room_id=booking.get("room_id") or booking.get("room_number"),
                    booking_id=booking["booking_id"],
                    rating=rating_var.get(),
                    comment=comment,
                )
            except Exception as error:
                messagebox.showerror("Review Error", f"Could not save your review: {error}", parent=review_win)
                return

            messagebox.showinfo("Thank You!", f"Thank you for rating your stay {rating_var.get()} ⭐!")
            review_win.destroy()

        tk.Button(
            review_win, text="Submit Review", command=submit_review,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, relief="flat", padx=20, pady=8, cursor="hand2",
            activebackground="#8B77E8", activeforeground=COLOR_WHITE
        ).pack(pady=15)


def open_member_dashboard(root, conn, user):
    """Hàm public để main.py / views/login.py gọi sau khi Member đăng nhập."""
    for w in root.winfo_children():
        w.destroy()
    root.title("Hotel Booking System - Member Portal")
    root.geometry("1100x700")
    root.minsize(950, 600)
    dashboard = MemberDashboard(root, conn, user)
    dashboard.pack(fill="both", expand=True)
    return dashboard


if __name__ == "__main__":
    root = tk.Tk()
    fake_user = {
        "user_id": 9,
        "full_name": "Phạm Trần Bảo Ngọc",
        "email": "ngoc.pham@gmail.com",
        "phone": "0912998877",
        "gender": "Nữ",
        "year_of_birth": 1997,
        "role": "Member",
        "status": "Active"
    }
    open_member_dashboard(root, None, fake_user)
    root.mainloop()