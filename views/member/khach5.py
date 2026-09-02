import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class HotelManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Booking System")
        window_width, window_height = 1180, 750
        center_x = int((self.winfo_screenwidth() - window_width) / 2)
        center_y = int((self.winfo_screenheight() - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(1080, 700)
        self.configure(fg_color="#f4f6f9")

        # 1. TOP HEADER BAR
        self.create_header()

        # 2. MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.sidebar_buttons = {}
        self.frames = {}

        # 3. SIDEBAR NAVIGATION
        self.create_sidebar()

        # 4. CONTENT AREA CONTAINER
        self.content_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=25, pady=20)

        # 5. KHỞI TẠO TẤT CẢ MÀN HÌNH
        self.init_all_screens()

        # Mặc định mở màn hình Dashboard khi khởi chạy
        self.show_screen("dashboard")

    # ================= 1. HEADER =================
    def create_header(self):
        header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#0b3b60")
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        lbl_logo = ctk.CTkLabel(
            header, text="🏨 Hotel Booking System",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="white"
        )
        lbl_logo.pack(side="left", padx=25)

        nav_right = ctk.CTkFrame(header, fg_color="transparent")
        nav_right.pack(side="right", padx=25)

        btn_notif = ctk.CTkButton(
            nav_right, text="🔔", fg_color="transparent", hover_color="#082b47",
            width=35, text_color="white", font=ctk.CTkFont(size=14),
            command=lambda: messagebox.showinfo("Thông báo", "Bạn có 1 lịch nhận phòng sắp tới!")
        )
        btn_notif.pack(side="left", padx=(0, 5))

        lbl_user = ctk.CTkLabel(
            nav_right, text="Ngọc ▼",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="white"
        )
        lbl_user.pack(side="left", padx=(5, 12))

        btn_logout = ctk.CTkButton(
            nav_right, text="Logout", width=70, height=30,
            fg_color="#e74c3c", hover_color="#c0392b",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.logout
        )
        btn_logout.pack(side="left")

    def logout(self):
        if messagebox.askyesno("Logout", "Bạn có chắc chắn muốn đăng xuất?"):
            self.destroy()

    # ================= 2. SIDEBAR =================
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_container, width=190, corner_radius=0, fg_color="#ffffff", border_width=1, border_color="#e5e5e5")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("🔍 Search", "search"),
            ("📅 My Booking", "booking"),
            ("📜 History", "history"),
            ("👤 Profile", "profile")
        ]

        top_menu = ctk.CTkFrame(sidebar, fg_color="transparent")
        top_menu.pack(fill="x", pady=(15, 0))

        for label, key in menu_items:
            btn = ctk.CTkButton(
                top_menu, text=label, anchor="w", height=42,
                fg_color="transparent", text_color="#555555",
                hover_color="#e2e8f0", font=ctk.CTkFont(size=13),
                command=lambda k=key: self.show_screen(k)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.sidebar_buttons[key] = btn

        btn_sidebar_logout = ctk.CTkButton(
            sidebar, text="🚪 Logout", anchor="w", height=42,
            fg_color="transparent", text_color="#e74c3c",
            hover_color="#fdeded", font=ctk.CTkFont(size=13, weight="bold"),
            command=self.logout
        )
        btn_sidebar_logout.pack(side="bottom", fill="x", padx=10, pady=20)

    # ================= 3. ĐIỀU HƯỚNG MÀN HÌNH =================
    def init_all_screens(self):
        self.frames["dashboard"] = self.build_dashboard_screen()
        self.frames["search"] = self.build_search_screen()
        self.frames["booking"] = self.build_booking_screen()
        self.frames["history"] = self.build_history_screen()
        self.frames["profile"] = self.build_profile_screen()

    def show_screen(self, screen_key):
        for frame in self.frames.values():
            frame.pack_forget()

        self.frames[screen_key].pack(fill="both", expand=True)

        for key, btn in self.sidebar_buttons.items():
            if key == screen_key:
                btn.configure(fg_color="#eef2f7", text_color="#0b3b60", font=ctk.CTkFont(size=13, weight="bold"))
            else:
                btn.configure(fg_color="transparent", text_color="#555555", font=ctk.CTkFont(size=13, weight="normal"))

    # ================= MÀN HÌNH 1: DASHBOARD =================
    def build_dashboard_screen(self):
        scroll_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")

        lbl_welcome = ctk.CTkLabel(scroll_frame, text="Welcome back, Ngọc 👋", font=ctk.CTkFont(size=24, weight="bold"), text_color="#0b3b60")
        lbl_welcome.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(scroll_frame, text="Here's what's happening with your hotel bookings.", font=ctk.CTkFont(size=13), text_color="gray")
        lbl_sub.pack(anchor="w", pady=(2, 20))

        # Card Thống kê
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 25))

        cards_data = [
            {"count": "1", "label": "Upcoming\nBookings", "color": "#27ae60"},
            {"count": "3", "label": "Completed\nBookings", "color": "#2980b9"},
            {"count": "1", "label": "Cancelled\nBookings", "color": "#e74c3c"}
        ]
        for data in cards_data:
            card = ctk.CTkFrame(stats_frame, width=220, height=95, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
            card.pack(side="left", padx=(0, 20))
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=data["count"], font=ctk.CTkFont(size=34, weight="bold"), text_color=data["color"]).pack(side="left", padx=(20, 15))
            ctk.CTkLabel(card, text=data["label"], font=ctk.CTkFont(size=13, weight="bold"), text_color="#333333", justify="left").pack(side="left")

        # Đặt phòng sắp tới
        ctk.CTkLabel(scroll_frame, text="Upcoming Booking", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 10))
        booking_card = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        booking_card.pack(fill="x", pady=(0, 25))

        r1 = ctk.CTkFrame(booking_card, fg_color="transparent")
        r1.pack(fill="x", padx=20, pady=(15, 8))
        ctk.CTkLabel(r1, text="Deluxe Ocean View (Room 203)", font=ctk.CTkFont(size=17, weight="bold"), text_color="#0b3b60").pack(side="left")
        ctk.CTkLabel(r1, text="● Confirmed", font=ctk.CTkFont(size=13, weight="bold"), text_color="#27ae60").pack(side="right")

        r2 = ctk.CTkFrame(booking_card, fg_color="transparent")
        r2.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(r2, text="📅 Check-in: 12 Sep 2026 → Check-out: 15 Sep 2026", font=ctk.CTkFont(size=13), text_color="#444444").pack(side="left")

        r3 = ctk.CTkFrame(booking_card, fg_color="transparent")
        r3.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(r3, text="👤 Guest: Ngọc • 2 Guests • 3 Nights", font=ctk.CTkFont(size=13), text_color="#666666").pack(side="left")

        ctk.CTkFrame(booking_card, height=1, fg_color="#eeeeee").pack(fill="x", padx=20, pady=12)

        r4 = ctk.CTkFrame(booking_card, fg_color="transparent")
        r4.pack(fill="x", padx=20, pady=(0, 15))
        ctk.CTkLabel(r4, text="Tổng cộng: 9.000.000 VNĐ", font=ctk.CTkFont(size=18, weight="bold"), text_color="#d35400").pack(side="left")
        ctk.CTkButton(r4, text="View Details", width=120, height=36, fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.show_screen("booking")).pack(side="right")

        # Nút truy cập nhanh
        ctk.CTkLabel(scroll_frame, text="Quick Actions", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 12))
        actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        actions_frame.pack(fill="x")

        quick_btns = [
            ("🔍 Search Available Rooms", "search"),
            ("📅 Manage My Bookings", "booking"),
            ("📜 View Booking History", "history"),
            ("👤 Update My Profile", "profile")
        ]
        for idx, (label, key) in enumerate(quick_btns):
            btn = ctk.CTkButton(
                actions_frame, text=label, width=260, height=45, fg_color="white", text_color="#0b3b60",
                hover_color="#eef2f7", border_width=1, border_color="#d0d7de", font=ctk.CTkFont(size=14, weight="bold"),
                corner_radius=8, command=lambda k=key: self.show_screen(k)
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=(0, 15), pady=(0, 15), sticky="w")

        return scroll_frame

    # ================= MÀN HÌNH 2: SEARCH (TÌM KIẾM PHÒNG) =================
    def build_search_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="🔍 Search Available Rooms", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        filter_box = ctk.CTkFrame(frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        filter_box.pack(fill="x", pady=(0, 20), padx=2)

        inner = ctk.CTkFrame(filter_box, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=15)

        entry_keyword = ctk.CTkEntry(inner, placeholder_text="Nhập tên phòng hoặc khu vực...", width=260, height=40)
        entry_keyword.pack(side="left", padx=(0, 10))

        combo_type = ctk.CTkOptionMenu(inner, values=["Tất cả loại phòng", "Deluxe Room", "Standard Room", "VIP Suite", "Beach Villa"], height=40, width=160)
        combo_type.pack(side="left", padx=(0, 10))

        combo_price = ctk.CTkOptionMenu(inner, values=["Mọi mức giá", "< 2.500.000 VNĐ / đêm", "2.500.000 - 6.000.000 VNĐ / đêm", "> 6.000.000 VNĐ / đêm"], height=40, width=210)
        combo_price.pack(side="left", padx=(0, 10))

        btn_search = ctk.CTkButton(inner, text="Search", height=40, width=90, fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(weight="bold"),
                                   command=lambda: messagebox.showinfo("Search Result", "Đã cập nhật danh sách các phòng khả dụng!"))
        btn_search.pack(side="left")

        rooms_data = [
            ("Deluxe Ocean View", "3.000.000 VNĐ / đêm", "🛏 1 King Bed  •  👥 2 Guests  •  📶 Free WiFi  •  🌅 Sea View", "Trải nghiệm phòng hướng biển tuyệt đẹp với ban công rộng rãi thoáng mát."),
            ("Executive VIP Suite", "6.250.000 VNĐ / đêm", "🛏 2 Queen Beds  •  👥 4 Guests  •  🛁 Jacuzzi  •  🍳 Free Breakfast", "Phòng VIP cao cấp với bồn tắm massage Jacuzzi và phục vụ điểm tâm tận phòng."),
            ("Standard Twin Room", "2.000.000 VNĐ / đêm", "🛏 2 Single Beds  •  👥 2 Guests  •  ❄ Air Conditioner  •  🏙 City View", "Lựa chọn tiết kiệm, không gian sạch sẽ hiện đại ngay trung tâm thành phố."),
            ("Luxury Beach Villa", "11.250.000 VNĐ / đêm", "🛏 3 King Beds  •  👥 6 Guests  •  🏊 Private Pool  •  🍹 Private Bar", "Biệt thự sát biển có hồ bơi riêng thích hợp cho nghỉ dưỡng gia đình.")
        ]

        for title, price, tags, desc in rooms_data:
            card = ctk.CTkFrame(frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
            card.pack(fill="x", pady=8)

            inner_card = ctk.CTkFrame(card, fg_color="transparent")
            inner_card.pack(fill="x", padx=20, pady=15)

            info_col = ctk.CTkFrame(inner_card, fg_color="transparent")
            info_col.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(info_col, text=title, font=ctk.CTkFont(size=17, weight="bold"), text_color="#0b3b60").pack(anchor="w")
            ctk.CTkLabel(info_col, text=tags, font=ctk.CTkFont(size=12, weight="bold"), text_color="#2c7a7b").pack(anchor="w", pady=(3, 3))
            ctk.CTkLabel(info_col, text=desc, font=ctk.CTkFont(size=12), text_color="#666666").pack(anchor="w")

            action_col = ctk.CTkFrame(inner_card, fg_color="transparent")
            action_col.pack(side="right", padx=(15, 0))

            ctk.CTkLabel(action_col, text=price, font=ctk.CTkFont(size=16, weight="bold"), text_color="#d35400").pack(anchor="e")
            btn_book = ctk.CTkButton(action_col, text="Book Now", width=110, height=36, fg_color="#27ae60", hover_color="#219150",
                                     font=ctk.CTkFont(weight="bold"), command=lambda t=title: messagebox.showinfo("Booking Request", f"Xác nhận đặt: {t}"))
            btn_book.pack(anchor="e", pady=(8, 0))

        return frame

    # ================= MÀN HÌNH 3: MY BOOKING (ĐẶT PHÒNG HIỆN TẠI) =================
    def build_booking_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="📅 My Bookings", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        # Booking 1: Confirmed
        card1 = ctk.CTkFrame(frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        card1.pack(fill="x", pady=(0, 15))

        inner1 = ctk.CTkFrame(card1, fg_color="transparent")
        inner1.pack(fill="x", padx=20, pady=20)

        h1 = ctk.CTkFrame(inner1, fg_color="transparent")
        h1.pack(fill="x")
        ctk.CTkLabel(h1, text="BOOKING ID: #BK-2026-8891", font=ctk.CTkFont(size=13, weight="bold"), text_color="gray").pack(side="left")
        ctk.CTkLabel(h1, text="● CONFIRMED", font=ctk.CTkFont(size=13, weight="bold"), text_color="#27ae60").pack(side="right")

        ctk.CTkLabel(inner1, text="Deluxe Ocean View (Room 203)", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(6, 2))
        ctk.CTkLabel(inner1, text="📅 Check-in: 12 Sep 2026 (14:00)  →  Check-out: 15 Sep 2026 (12:00)", font=ctk.CTkFont(size=13), text_color="#444444").pack(anchor="w", pady=2)
        ctk.CTkLabel(inner1, text="👤 Guest Name: Ngọc  •  2 Adults  •  Total Amount: 9.000.000 VNĐ", font=ctk.CTkFont(size=13, weight="bold"), text_color="#d35400").pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(inner1, height=1, fg_color="#eeeeee").pack(fill="x", pady=15)

        btn_row1 = ctk.CTkFrame(inner1, fg_color="transparent")
        btn_row1.pack(fill="x")
        ctk.CTkButton(btn_row1, text="Cancel Booking", fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(weight="bold"), width=130, height=36,
                       command=lambda: messagebox.showwarning("Cancel", "Xác nhận gửi yêu cầu hủy đơn #BK-2026-8891?")).pack(side="right")
        ctk.CTkButton(btn_row1, text="Modify Booking", fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(weight="bold"), width=130, height=36,
                       command=lambda: messagebox.showinfo("Modify", "Mở khung thay đổi lịch đặt phòng.")).pack(side="right", padx=10)

        # Booking 2: Pending Payment
        card2 = ctk.CTkFrame(frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        card2.pack(fill="x", pady=5)

        inner2 = ctk.CTkFrame(card2, fg_color="transparent")
        inner2.pack(fill="x", padx=20, pady=20)

        h2 = ctk.CTkFrame(inner2, fg_color="transparent")
        h2.pack(fill="x")
        ctk.CTkLabel(h2, text="BOOKING ID: #BK-2026-9012", font=ctk.CTkFont(size=13, weight="bold"), text_color="gray").pack(side="left")
        ctk.CTkLabel(h2, text="● PENDING PAYMENT", font=ctk.CTkFont(size=13, weight="bold"), text_color="#e67e22").pack(side="right")

        ctk.CTkLabel(inner2, text="Executive VIP Suite (Room 501)", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(6, 2))
        ctk.CTkLabel(inner2, text="📅 Check-in: 01 Oct 2026 (14:00)  →  Check-out: 03 Oct 2026 (12:00)", font=ctk.CTkFont(size=13), text_color="#444444").pack(anchor="w", pady=2)
        ctk.CTkLabel(inner2, text="👤 Guest Name: Ngọc  •  4 Adults  •  Total Amount: 12.500.000 VNĐ", font=ctk.CTkFont(size=13, weight="bold"), text_color="#d35400").pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(inner2, height=1, fg_color="#eeeeee").pack(fill="x", pady=15)

        btn_row2 = ctk.CTkFrame(inner2, fg_color="transparent")
        btn_row2.pack(fill="x")
        ctk.CTkButton(btn_row2, text="Pay Now", fg_color="#27ae60", hover_color="#219150", font=ctk.CTkFont(weight="bold"), width=130, height=36,
                       command=lambda: messagebox.showinfo("Payment", "Chuyển sang màn hình thanh toán.")).pack(side="right")
        ctk.CTkButton(btn_row2, text="Cancel Request", fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(weight="bold"), width=130, height=36,
                       command=lambda: messagebox.showinfo("Cancel", "Đã hủy đơn chờ thanh toán.")).pack(side="right", padx=10)

        return frame

    # ================= MÀN HÌNH 4: HISTORY (LỊCH SỬ ĐẶT PHÒNG) =================
    def build_history_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="📜 Booking History", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        history_items = [
            ("Standard Twin Room", "01 Jun 2026 - 03 Jun 2026", "4.000.000 VNĐ", "Completed", "#27ae60"),
            ("Executive VIP Suite", "10 May 2026 - 12 May 2026", "12.500.000 VNĐ", "Completed", "#27ae60"),
            ("Single Deluxe Room", "15 Feb 2026 - 16 Feb 2026", "2.250.000 VNĐ", "Cancelled", "#e74c3c"),
            ("Luxury Beach Villa", "20 Dec 2025 - 25 Dec 2025", "21.250.000 VNĐ", "Completed", "#27ae60")
        ]

        for item, dates, price, status, status_color in history_items:
            card = ctk.CTkFrame(frame, fg_color="white", corner_radius=8, border_width=1, border_color="#e0e0e0")
            card.pack(fill="x", pady=6)

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=15)

            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left")
            ctk.CTkLabel(left, text=item, font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(anchor="w")
            ctk.CTkLabel(left, text=f"📅 Dates: {dates}", font=ctk.CTkFont(size=13), text_color="gray").pack(anchor="w", pady=(3, 0))

            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right")

            ctk.CTkLabel(right, text=f"● {status}", font=ctk.CTkFont(size=13, weight="bold"), text_color=status_color).pack(anchor="e")
            ctk.CTkLabel(right, text=price, font=ctk.CTkFont(size=14, weight="bold"), text_color="#333333").pack(anchor="e", pady=(2, 5))

            if status == "Completed":
                btn_act = ctk.CTkButton(right, text="⭐ Write Review", width=110, height=28, fg_color="#f39c12", hover_color="#d68910",
                                         font=ctk.CTkFont(size=11, weight="bold"), command=lambda t=item: messagebox.showinfo("Review", f"Đánh giá cho phòng: {t}"))
                btn_act.pack(anchor="e")
            else:
                ctk.CTkLabel(right, text="Refunded", font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="e")

        return frame

    # ================= MÀN HÌNH 5: PROFILE (HỒ SƠ CÁ NHÂN NGỌC) =================
    def build_profile_screen(self):
        scroll_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")

        card = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#e2e8f0")
        card.pack(fill="x", padx=5, pady=5)

        # Header card
        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=30, pady=(25, 15))

        lbl_title = ctk.CTkLabel(header_row, text="MY PROFILE", font=ctk.CTkFont(size=16, weight="bold"), text_color="#2c7a7b")
        lbl_title.pack(side="left")

        btn_edit = ctk.CTkButton(
            header_row, text="✏  Edit Info", width=105, height=34,
            fg_color="#2c7a7b", hover_color="#205d5e",
            text_color="white", font=ctk.CTkFont(size=12, weight="bold"), corner_radius=8,
            command=lambda: messagebox.showinfo("Edit Profile", "Mở chế độ chỉnh sửa thông tin cá nhân")
        )
        btn_edit.pack(side="right")

        divider = ctk.CTkFrame(card, height=1, fg_color="#e2e8f0")
        divider.pack(fill="x", padx=30, pady=(0, 25))

        # Body Layout
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=(0, 35))

        # --- CỘT TRÁI (Avatar tròn + Tên Ngọc) ---
        left_col = ctk.CTkFrame(body, fg_color="transparent")
        left_col.pack(side="left", anchor="n", padx=(10, 50))

        avatar_box = ctk.CTkFrame(left_col, width=90, height=90, corner_radius=45, fg_color="#38b2ac")
        avatar_box.pack_propagate(False)
        avatar_box.pack(pady=(0, 15))

        lbl_avatar_icon = ctk.CTkLabel(avatar_box, text="👩‍🎓", font=ctk.CTkFont(size=42))
        lbl_avatar_icon.place(relx=0.5, rely=0.5, anchor="center")

        lbl_name = ctk.CTkLabel(left_col, text="Ngọc", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2d3748")
        lbl_name.pack(anchor="w")

        lbl_email_sub = ctk.CTkLabel(left_col, text="ngoc@test.com", font=ctk.CTkFont(size=13, weight="bold"), text_color="#319795")
        lbl_email_sub.pack(anchor="w", pady=(2, 12))

        badges_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        badges_frame.pack(anchor="w")

        badge1 = ctk.CTkFrame(badges_frame, fg_color="#edf2f7", corner_radius=12)
        badge1.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(badge1, text="STUDENT", font=ctk.CTkFont(size=10, weight="bold"), text_color="#718096", padx=10, pady=3).pack()

        badge2 = ctk.CTkFrame(badges_frame, fg_color="#ebf8ff", corner_radius=12)
        badge2.pack(side="left")
        ctk.CTkLabel(badge2, text="S001", font=ctk.CTkFont(size=10, weight="bold"), text_color="#3182ce", padx=10, pady=3).pack()

        # --- CỘT PHẢI (Thông tin liên hệ) ---
        right_col = ctk.CTkFrame(body, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(20, 10))

        ctk.CTkLabel(right_col, text="Contact Details", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2d3748").pack(anchor="w")
        ctk.CTkFrame(right_col, height=1, fg_color="#cbd5e0").pack(fill="x", pady=(5, 18))

        fields_data = [
            ("DATE OF BIRTH", "2002-05-15"),
            ("EMAIL ADDRESS", "ngoc@test.com"),
            ("PHONE NUMBER", "0901234567"),
            ("ADDRESS", "123 ABC Street, District 1, HCMC")
        ]

        for label_text, val in fields_data:
            field_box = ctk.CTkFrame(right_col, fg_color="transparent")
            field_box.pack(fill="x", pady=(0, 14))

            ctk.CTkLabel(field_box, text=label_text, font=ctk.CTkFont(size=10, weight="bold"), text_color="#718096").pack(anchor="w", pady=(0, 4))

            entry_field = ctk.CTkEntry(
                field_box, height=42,
                fg_color="#f7fafc", border_color="#e2e8f0", border_width=1,
                text_color="#2d3748", font=ctk.CTkFont(size=13, weight="bold"),
                corner_radius=8
            )
            entry_field.insert(0, val)
            entry_field.configure(state="readonly")
            entry_field.pack(fill="x")

        return scroll_frame


if __name__ == "__main__":
    app = HotelManagementApp()
    app.mainloop()