import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class HotelManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Booking System - Payment Integrated")
        window_width, window_height = 1180, 750
        center_x = int((self.winfo_screenwidth() - window_width) / 2)
        center_y = int((self.winfo_screenheight() - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(1080, 700)
        self.configure(fg_color="#f4f6f9")

        # CƠ SỞ DỮ LIỆU ĐÁNH GIÁ MẪU
        self.reviews_db = {
            "Deluxe Ocean View": [
                {"user": "Minh Anh", "rating": "⭐ 5", "date": "10/08/2026", "comment": "Phòng rất đẹp, view biển đỉnh cao, sạch sẽ tiện nghi!"},
                {"user": "Hoàng Nam", "rating": "⭐ 4", "date": "25/07/2026", "comment": "Nhân viên nhiệt tình, đồ ăn sáng ngon."}
            ],
            "Executive VIP Suite": [
                {"user": "Trần Bình", "rating": "⭐ 5", "date": "12/08/2026", "comment": "Bồn tắm Jacuzzi cực kỳ thích, không gian vô cùng sang trọng."}
            ],
            "Standard Twin Room": [
                {"user": "Lê Hoa", "rating": "⭐ 4", "date": "02/08/2026", "comment": "Giá hợp lý, không gian sạch sẽ ngay trung tâm tiện đi lại."}
            ],
            "Luxury Beach Villa": [
                {"user": "Đặng Khoa", "rating": "⭐ 5", "date": "18/08/2026", "comment": "Hồ bơi riêng tư, gia đình mình rất hài lòng với chuyến đi."}
            ]
        }

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
        self.show_screen("dashboard")

    # ================= HEADER & SIDEBAR =================
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

    # ================= 💳 POPUP: MÀN HÌNH ĐẶT PHÒNG & THANH TOÁN =================
    def open_payment_dialog(self, room_name, price, booking_id=None):
        top = ctk.CTkToplevel(self)
        top.title(f"Thanh Toán Đặt Phòng - {room_name}")
        top.geometry("540x680")
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{self.winfo_x() + 320}+{self.winfo_y() + 40}")

        # Header Title
        ctk.CTkLabel(top, text="💳 XÁC NHẬN & THANH TOÁN", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(pady=(18, 5))

        # Box Tóm tắt đơn hàng (Order Summary)
        summary_box = ctk.CTkFrame(top, fg_color="#f8fafc", corner_radius=10, border_width=1, border_color="#e2e8f0")
        summary_box.pack(fill="x", padx=25, pady=10)

        s_inner = ctk.CTkFrame(summary_box, fg_color="transparent")
        s_inner.pack(fill="x", padx=15, pady=12)

        code_text = booking_id if booking_id else "#BK-2026-NEW"
        ctk.CTkLabel(s_inner, text=f"Mã Đơn: {code_text}", font=ctk.CTkFont(size=11, weight="bold"), text_color="#718096").pack(anchor="w")
        ctk.CTkLabel(s_inner, text=room_name, font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(2, 4))
        ctk.CTkLabel(s_inner, text="📅 Nhận phòng: 15/09/2026  →  Trả phòng: 17/09/2026 (2 Đêm)", font=ctk.CTkFont(size=12), text_color="#4a5568").pack(anchor="w")
        
        div = ctk.CTkFrame(s_inner, height=1, fg_color="#e2e8f0")
        div.pack(fill="x", pady=8)

        total_row = ctk.CTkFrame(s_inner, fg_color="transparent")
        total_row.pack(fill="x")
        ctk.CTkLabel(total_row, text="Tổng tiền thanh toán:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2d3748").pack(side="left")
        ctk.CTkLabel(total_row, text=price, font=ctk.CTkFont(size=17, weight="bold"), text_color="#d35400").pack(side="right")

        # Phương thức thanh toán
        ctk.CTkLabel(top, text="Chọn phương thức thanh toán:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#0b3b60").pack(anchor="w", padx=25, pady=(10, 5))

        payment_method = ctk.StringVar(value="card")

        card_frame = ctk.CTkFrame(top, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        card_frame.pack(fill="x", padx=25, pady=5)

        # Dynamic Content Container
        pay_content_container = ctk.CTkFrame(top, fg_color="transparent")
        pay_content_container.pack(fill="both", expand=True, padx=25, pady=10)

        def switch_payment_view():
            for child in pay_content_container.winfo_children():
                child.destroy()

            method = payment_method.get()
            if method == "card":
                # Form Thẻ Tín Dụng
                ctk.CTkLabel(pay_content_container, text="Số thẻ (Card Number):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4a5568").pack(anchor="w", pady=(0, 2))
                entry_card_num = ctk.CTkEntry(pay_content_container, placeholder_text="4111 2222 3333 4444", height=38)
                entry_card_num.pack(fill="x", pady=(0, 8))

                row2 = ctk.CTkFrame(pay_content_container, fg_color="transparent")
                row2.pack(fill="x", pady=(0, 8))

                col1 = ctk.CTkFrame(row2, fg_color="transparent")
                col1.pack(side="left", fill="x", expand=True, padx=(0, 5))
                ctk.CTkLabel(col1, text="Tên chủ thẻ:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4a5568").pack(anchor="w", pady=(0, 2))
                entry_name = ctk.CTkEntry(col1, placeholder_text="NGUYEN VAN A", height=38)
                entry_name.pack(fill="x")

                col2 = ctk.CTkFrame(row2, fg_color="transparent")
                col2.pack(side="right", width=120, padx=(5, 0))
                ctk.CTkLabel(col2, text="Hạn (MM/YY):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4a5568").pack(anchor="w", pady=(0, 2))
                entry_exp = ctk.CTkEntry(col2, placeholder_text="12/28", height=38)
                entry_exp.pack(fill="x")

            elif method == "qr":
                # Khung hiển thị Mã QR
                qr_box = ctk.CTkFrame(pay_content_container, fg_color="white", corner_radius=8, border_width=1, border_color="#cbd5e0")
                qr_box.pack(fill="both", expand=True, pady=5)

                ctk.CTkLabel(qr_box, text="📲 Quét mã VietQR để thanh toán", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2b6cb0").pack(pady=(12, 4))
                
                # Biểu tượng QR mô phỏng
                qr_icon_frame = ctk.CTkFrame(qr_box, width=110, height=110, fg_color="#edf2f7", corner_radius=6)
                qr_icon_frame.pack(pady=4)
                qr_icon_frame.pack_propagate(False)
                ctk.CTkLabel(qr_icon_frame, text="🔳\n[ VietQR ]", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4a5568").place(relx=0.5, rely=0.5, anchor="center")

                ctk.CTkLabel(qr_box, text="Ngân hàng: MBBank | STK: 0901234567\nChủ tài khoản: HOTEL BOOKING SYSTEM", font=ctk.CTkFont(size=11), text_color="#4a5568", justify="center").pack(pady=(4, 10))

            elif method == "cash":
                # Khung Tiền Mặt
                cash_box = ctk.CTkFrame(pay_content_container, fg_color="#fffaf0", corner_radius=8, border_width=1, border_color="#feebc8")
                cash_box.pack(fill="both", expand=True, pady=5)
                
                ctk.CTkLabel(cash_box, text="🏨 Thanh toán trực tiếp tại Lễ Tân", font=ctk.CTkFont(size=13, weight="bold"), text_color="#c05621").pack(pady=(15, 5))
                ctk.CTkLabel(cash_box, text="• Khách sạn sẽ giữ phòng cho bạn đến 18:00 ngày nhận phòng.\n• Vui lòng chuẩn bị tiền mặt hoặc thẻ để thanh toán khi Check-in.", font=ctk.CTkFont(size=11), text_color="#7b341e", justify="left").pack(padx=15, pady=5)

        segmented = ctk.CTkSegmentedButton(
            top, values=["Thẻ Tín Dụng", "Chuyển Khoản QR", "Tiền Mặt"],
            command=lambda v: [payment_method.set("card" if v == "Thẻ Tín Dụng" else "qr" if v == "Chuyển Khoản QR" else "cash"), switch_payment_view()],
            selected_color="#0b3b60", selected_hover_color="#082b47"
        )
        segmented.set("Thẻ Tín Dụng")
        segmented.pack(fill="x", padx=25, pady=(0, 10))

        # Khởi tạo giao diện phương thức ban đầu
        switch_payment_view()

        # Nút xác nhận thanh toán
        def confirm_payment():
            m = payment_method.get()
            method_str = "Thẻ Tín Dụng" if m == "card" else "Chuyển Khoản QR" if m == "qr" else "Tiền Mặt khi Check-in"
            
            messagebox.showinfo(
                "Thành Công!", 
                f"🎉 ĐẶT PHÒNG THÀNH CÔNG!\n\n"
                f"• Phòng: {room_name}\n"
                f"• Tổng thanh toán: {price}\n"
                f"• Hình thức: {method_str}\n\n"
                f"Cảm ơn bạn đã lựa chọn dịch vụ của chúng tôi!",
                parent=top
            )
            top.destroy()
            self.show_screen("booking") # Chuyển về màn hình Booking để xem đơn

        btn_confirm = ctk.CTkButton(
            top, text="🔒 XÁC NHẬN THANH TOÁN", fg_color="#27ae60", hover_color="#219150",
            font=ctk.CTkFont(size=14, weight="bold"), height=45, corner_radius=8,
            command=confirm_payment
        )
        btn_confirm.pack(fill="x", padx=25, side="bottom", pady=20)

    # ================= ✍ POPUP: VIẾT ĐÁNH GIÁ =================
    def open_write_review_dialog(self, room_name):
        top = ctk.CTkToplevel(self)
        top.title(f"Viết đánh giá - {room_name}")
        top.geometry("450x430")
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{self.winfo_x() + 350}+{self.winfo_y() + 150}")

        ctk.CTkLabel(top, text="✍  VIẾT ĐÁNH GIÁ PHÒNG", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(pady=(18, 2))
        ctk.CTkLabel(top, text=room_name, font=ctk.CTkFont(size=13, weight="bold"), text_color="#2c7a7b").pack(pady=(0, 15))

        ctk.CTkLabel(top, text="Chọn mức độ hài lòng:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333").pack(anchor="w", padx=25, pady=(0, 5))
        star_option = ctk.CTkSegmentedButton(top, values=["⭐ 1", "⭐ 2", "⭐ 3", "⭐ 4", "⭐ 5"], selected_color="#f39c12", selected_hover_color="#d68910")
        star_option.set("⭐ 5")
        star_option.pack(fill="x", padx=25, pady=(0, 15))

        ctk.CTkLabel(top, text="Nội dung nhận xét / Đánh giá:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333").pack(anchor="w", padx=25, pady=(0, 5))
        txt_comment = ctk.CTkTextbox(top, height=120, border_width=1, border_color="#cccccc", corner_radius=8)
        txt_comment.pack(fill="x", padx=25, pady=(0, 20))

        def submit_review():
            comment = txt_comment.get("1.0", "end-1c").strip()
            if not comment:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung đánh giá!", parent=top)
                return

            rating = star_option.get()
            if room_name not in self.reviews_db:
                self.reviews_db[room_name] = []

            self.reviews_db[room_name].insert(0, {
                "user": "Ngọc",
                "rating": rating,
                "date": "Hôm nay",
                "comment": comment
            })

            messagebox.showinfo("Thành công", f"Cảm ơn bạn đã gửi đánh giá cho {room_name}!", parent=top)
            top.destroy()

        btn_submit = ctk.CTkButton(
            top, text="Gửi Đánh Giá", fg_color="#27ae60", hover_color="#219150",
            font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=8, command=submit_review
        )
        btn_submit.pack(fill="x", padx=25)

    # ================= 💬 POPUP: XEM ĐÁNH GIÁ =================
    def open_view_reviews_dialog(self, room_name):
        top = ctk.CTkToplevel(self)
        top.title(f"Đánh giá - {room_name}")
        top.geometry("520x550")
        top.grab_set()
        top.geometry(f"+{self.winfo_x() + 330}+{self.winfo_y() + 100}")

        ctk.CTkLabel(top, text="💬 ĐÁNH GIÁ TỪ KHÁCH HÀNG", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(pady=(18, 2))
        ctk.CTkLabel(top, text=room_name, font=ctk.CTkFont(size=13, weight="bold"), text_color="#2c7a7b").pack(pady=(0, 15))

        scroll = ctk.CTkScrollableFrame(top, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        reviews = self.reviews_db.get(room_name, [])

        if not reviews:
            ctk.CTkLabel(scroll, text="Chưa có đánh giá nào cho phòng này.", text_color="gray", font=ctk.CTkFont(size=13)).pack(pady=40)
        else:
            for r in reviews:
                card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=8, border_width=1, border_color="#e0e0e0")
                card.pack(fill="x", pady=6)

                h = ctk.CTkFrame(card, fg_color="transparent")
                h.pack(fill="x", padx=15, pady=(10, 2))

                ctk.CTkLabel(h, text=f"👤 {r['user']}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#0b3b60").pack(side="left")
                ctk.CTkLabel(h, text=r['rating'], font=ctk.CTkFont(size=12, weight="bold"), text_color="#f39c12").pack(side="right")

                ctk.CTkLabel(card, text=f"📅 {r['date']}", font=ctk.CTkFont(size=10), text_color="gray").pack(anchor="w", padx=15)
                ctk.CTkLabel(card, text=r['comment'], font=ctk.CTkFont(size=12), text_color="#333333", justify="left", wraplength=430).pack(anchor="w", padx=15, pady=(6, 12))

    # ================= MÀN HÌNH 1: DASHBOARD =================
    def build_dashboard_screen(self):
        scroll_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")

        lbl_welcome = ctk.CTkLabel(scroll_frame, text="Welcome back, Ngọc 👋", font=ctk.CTkFont(size=24, weight="bold"), text_color="#0b3b60")
        lbl_welcome.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(scroll_frame, text="Here's what's happening with your hotel bookings.", font=ctk.CTkFont(size=13), text_color="gray")
        lbl_sub.pack(anchor="w", pady=(2, 20))

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

        return scroll_frame

    # ================= MÀN HÌNH 2: SEARCH (KÍCH HOẠT THANH TOÁN KHI BOOK NOW) =================
    def build_search_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="🔍 Search Available Rooms", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

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

            btn_group = ctk.CTkFrame(action_col, fg_color="transparent")
            btn_group.pack(anchor="e", pady=(8, 0))

            btn_view_rev = ctk.CTkButton(
                btn_group, text="💬 Xem đánh giá", width=115, height=36, fg_color="#f39c12", hover_color="#d68910",
                font=ctk.CTkFont(size=12, weight="bold"), command=lambda t=title: self.open_view_reviews_dialog(t)
            )
            btn_view_rev.pack(side="left", padx=(0, 8))

            # NÚT BOOK NOW -> MỞ POPUP THANH TOÁN ĐẶT PHÒNG
            btn_book = ctk.CTkButton(
                btn_group, text="Book Now", width=100, height=36, fg_color="#27ae60", hover_color="#219150",
                font=ctk.CTkFont(weight="bold"), command=lambda t=title, p=price: self.open_payment_dialog(room_name=t, price=p)
            )
            btn_book.pack(side="left")

        return frame

    # ================= MÀN HÌNH 3: MY BOOKING (THANH TOÁN ĐƠN PENDING) =================
    def build_booking_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="📅 My Bookings", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        # Booking 1: Pending Payment -> Bấm "Pay Now" để mở Popup Thanh toán
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
        
        # NÚT PAY NOW MỞ POPUP THANH TOÁN
        ctk.CTkButton(
            btn_row2, text="Pay Now", fg_color="#27ae60", hover_color="#219150", font=ctk.CTkFont(weight="bold"), width=130, height=36,
            command=lambda: self.open_payment_dialog(room_name="Executive VIP Suite (Room 501)", price="12.500.000 VNĐ", booking_id="#BK-2026-9012")
        ).pack(side="right")
        
        ctk.CTkButton(btn_row2, text="Cancel Request", fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(weight="bold"), width=130, height=36,
                       command=lambda: messagebox.showinfo("Cancel", "Đã hủy đơn chờ thanh toán.")).pack(side="right", padx=10)

        return frame

    # ================= MÀN HÌNH 4: HISTORY =================
    def build_history_screen(self):
        frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(frame, text="📜 Booking History", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        history_items = [
            ("Standard Twin Room", "01 Jun 2026 - 03 Jun 2026", "4.000.000 VNĐ", "Completed", "#27ae60"),
            ("Executive VIP Suite", "10 May 2026 - 12 May 2026", "12.500.000 VNĐ", "Completed", "#27ae60"),
            ("Single Deluxe Room", "15 Feb 2026 - 16 Feb 2026", "2.250.000 VNĐ", "Cancelled", "#e74c3c")
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
                btn_act = ctk.CTkButton(
                    right, text="⭐ Write Review", width=115, height=28, fg_color="#f39c12", hover_color="#d68910",
                    font=ctk.CTkFont(size=11, weight="bold"), command=lambda t=item: self.open_write_review_dialog(t)
                )
                btn_act.pack(anchor="e")

        return frame

    # ================= MÀN HÌNH 5: PROFILE =================
    def build_profile_screen(self):
        scroll_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        card = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#e2e8f0")
        card.pack(fill="x", padx=5, pady=5)

        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header_row, text="MY PROFILE", font=ctk.CTkFont(size=16, weight="bold"), text_color="#2c7a7b").pack(side="left")

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=(0, 35))

        left_col = ctk.CTkFrame(body, fg_color="transparent")
        left_col.pack(side="left", anchor="n", padx=(10, 50))

        avatar_box = ctk.CTkFrame(left_col, width=90, height=90, corner_radius=45, fg_color="#38b2ac")
        avatar_box.pack_propagate(False)
        avatar_box.pack(pady=(0, 15))

        lbl_avatar_icon = ctk.CTkLabel(avatar_box, text="👩‍🎓", font=ctk.CTkFont(size=42))
        lbl_avatar_icon.place(relx=0.5, rely=0.5, anchor="center")

        lbl_name = ctk.CTkLabel(left_col, text="Ngọc", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2d3748")
        lbl_name.pack(anchor="w")

        return scroll_frame


if __name__ == "__main__":
    app = HotelManagementApp()
    app.mainloop()