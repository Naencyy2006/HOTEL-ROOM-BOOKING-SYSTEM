import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class MemberDashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Booking System")
        window_width, window_height = 1180, 720
        center_x = int((self.winfo_screenwidth() - window_width) / 2)
        center_y = int((self.winfo_screenheight() - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(1050, 680)
        self.configure(fg_color="#f4f6f9")

        # 1. TOP HEADER BAR (Đã loại bỏ các nút menu giữa)
        self.create_header()

        # 2. MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # Sidebar bên trái (Nơi chứa menu chính)
        self.create_sidebar()

        # Content Area bên phải
        self.content_area = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)

        # Các thành phần giao diện chính
        self.create_greeting()
        self.create_stats_cards()
        self.create_upcoming_booking()
        self.create_quick_actions()

    # ================= 1. HEADER (ĐÃ XÓA MENU ĐIỀU HƯỚNG GIỮA) =================
    def create_header(self):
        header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#0b3b60")
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo bên trái
        lbl_logo = ctk.CTkLabel(
            header, text="🏨 Hotel Booking System",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="white"
        )
        lbl_logo.pack(side="left", padx=25)

        # Cụm tài khoản bên phải (Chuông + Tên + Logout)
        nav_right = ctk.CTkFrame(header, fg_color="transparent")
        nav_right.pack(side="right", padx=25)

        # Nút Thông báo 🔔
        btn_notif = ctk.CTkButton(
            nav_right, text="🔔", fg_color="transparent", hover_color="#082b47",
            width=35, text_color="white", font=ctk.CTkFont(size=14),
            command=lambda: messagebox.showinfo("Notifications", "Không có thông báo mới.")
        )
        btn_notif.pack(side="left", padx=(0, 5))

        # Tên người dùng "Ngọc ▼"
        lbl_user = ctk.CTkLabel(
            nav_right, text="Ngọc ▼",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="white"
        )
        lbl_user.pack(side="left", padx=(5, 12))

        # Nút Đăng xuất
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

        items = [
            ("📊 Dashboard", True),
            ("🔍 Search", False),
            ("📅 My Booking", False),
            ("📜 History", False),
            ("👤 Profile", False)
        ]

        top_menu = ctk.CTkFrame(sidebar, fg_color="transparent")
        top_menu.pack(fill="x", pady=(15, 0))

        for label, active in items:
            btn = ctk.CTkButton(
                top_menu, text=label, anchor="w", height=42,
                fg_color="#eef2f7" if active else "transparent",
                text_color="#0b3b60" if active else "#555555",
                hover_color="#e2e8f0",
                font=ctk.CTkFont(size=13, weight="bold" if active else "normal")
            )
            btn.pack(fill="x", padx=10, pady=3)

        btn_sidebar_logout = ctk.CTkButton(
            sidebar, text="🚪 Logout", anchor="w", height=42,
            fg_color="transparent", text_color="#e74c3c",
            hover_color="#fdeded", font=ctk.CTkFont(size=13, weight="bold"),
            command=self.logout
        )
        btn_sidebar_logout.pack(side="bottom", fill="x", padx=10, pady=20)

    # ================= 3. GREETING =================
    def create_greeting(self):
        lbl_welcome = ctk.CTkLabel(
            self.content_area, text="Welcome back, Ngọc 👋",
            font=ctk.CTkFont(size=24, weight="bold"), text_color="#0b3b60"
        )
        lbl_welcome.pack(anchor="w")

        lbl_subtitle = ctk.CTkLabel(
            self.content_area, text="Here's what's happening with your bookings.",
            font=ctk.CTkFont(size=13), text_color="gray"
        )
        lbl_subtitle.pack(anchor="w", pady=(2, 20))

    # ================= 4. STAT CARDS =================
    def create_stats_cards(self):
        stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 25))

        cards_data = [
            {"count": "1", "label": "Upcoming\nBookings", "color": "#27ae60"},
            {"count": "2", "label": "Completed\nBookings", "color": "#2980b9"},
            {"count": "0", "label": "Cancelled\nBookings", "color": "#e74c3c"}
        ]

        for data in cards_data:
            card = ctk.CTkFrame(stats_frame, width=220, height=95, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
            card.pack(side="left", padx=(0, 20))
            card.pack_propagate(False)

            lbl_count = ctk.CTkLabel(
                card, text=data["count"],
                font=ctk.CTkFont(size=34, weight="bold"), text_color=data["color"]
            )
            lbl_count.pack(side="left", padx=(20, 15))

            lbl_text = ctk.CTkLabel(
                card, text=data["label"],
                font=ctk.CTkFont(size=13, weight="bold"), text_color="#333333",
                justify="left"
            )
            lbl_text.pack(side="left")

    # ================= 5. UPCOMING BOOKING =================
    def create_upcoming_booking(self):
        lbl_title = ctk.CTkLabel(
            self.content_area, text="Upcoming Booking",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60"
        )
        lbl_title.pack(anchor="w", pady=(0, 10))

        booking_card = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        booking_card.pack(fill="x", pady=(0, 25))

        row1 = ctk.CTkFrame(booking_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(15, 8))

        lbl_room_name = ctk.CTkLabel(
            row1, text="Deluxe Room",
            font=ctk.CTkFont(size=17, weight="bold"), text_color="#0b3b60"
        )
        lbl_room_name.pack(side="left")

        lbl_status = ctk.CTkLabel(
            row1, text="● Confirmed",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#27ae60"
        )
        lbl_status.pack(side="right")

        row2 = ctk.CTkFrame(booking_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=3)

        lbl_date = ctk.CTkLabel(
            row2, text="📅 12 Sep 2026 → 15 Sep 2026",
            font=ctk.CTkFont(size=13), text_color="#444444"
        )
        lbl_date.pack(side="left")

        row3 = ctk.CTkFrame(booking_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=3)

        lbl_info = ctk.CTkLabel(
            row3, text="👤 2 Guests        🛏 Room 203",
            font=ctk.CTkFont(size=13), text_color="#666666"
        )
        lbl_info.pack(side="left")

        divider = ctk.CTkFrame(booking_card, height=1, fg_color="#eeeeee")
        divider.pack(fill="x", padx=20, pady=12)

        row4 = ctk.CTkFrame(booking_card, fg_color="transparent")
        row4.pack(fill="x", padx=20, pady=(0, 15))

        lbl_price = ctk.CTkLabel(
            row4, text="$360",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#d35400"
        )
        lbl_price.pack(side="left")

        btn_details = ctk.CTkButton(
            row4, text="View Details", width=120, height=36,
            fg_color="#0b3b60", hover_color="#082b47",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: messagebox.showinfo("Booking Details", "Hiển thị thông tin chi tiết phòng 203")
        )
        btn_details.pack(side="right")

    # ================= 6. QUICK ACTIONS =================
    def create_quick_actions(self):
        lbl_title = ctk.CTkLabel(
            self.content_area, text="Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60"
        )
        lbl_title.pack(anchor="w", pady=(0, 12))

        actions_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        actions_frame.pack(fill="x")

        buttons = [
            ("🔍 Search Rooms", lambda: messagebox.showinfo("Action", "Mở trang Tìm phòng")),
            ("📅 My Bookings", lambda: messagebox.showinfo("Action", "Mở trang Đặt phòng")),
            ("⭐ Write Review", lambda: messagebox.showinfo("Action", "Mở trang Viết đánh giá")),
            ("👤 My Profile", lambda: messagebox.showinfo("Action", "Mở Trang cá nhân"))
        ]

        for i, (btn_text, cmd) in enumerate(buttons):
            row_idx = i // 2
            col_idx = i % 2

            btn = ctk.CTkButton(
                actions_frame, text=btn_text, width=260, height=45,
                fg_color="white", text_color="#0b3b60",
                hover_color="#eef2f7", border_width=1, border_color="#d0d7de",
                font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8,
                command=cmd
            )
            btn.grid(row=row_idx, column=col_idx, padx=(0, 15), pady=(0, 15), sticky="w")


if __name__ == "__main__":
    app = MemberDashboardApp()
    app.mainloop()