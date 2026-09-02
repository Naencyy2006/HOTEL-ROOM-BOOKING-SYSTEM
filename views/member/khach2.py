import customtkinter as ctk
from tkinter import messagebox, ttk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class MemberDashboard(ctk.CTk):
    def __init__(self, username="Nguyen Van A"):
        super().__init__()

        self.username = username
        self.title("Hotel Booking System - Member Portal")
        
        # Kích thước màn hình chuẩn Desktop
        window_width, window_height = 1150, 720
        center_x = int((self.winfo_screenwidth() - window_width) / 2)
        center_y = int((self.winfo_screenheight() - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(1000, 650)
        self.configure(fg_color="#f3f5f8")

        # 1. TOP HEADER BAR
        self.create_header()

        # 2. MAIN CONTENT AREA (Sử dụng TabView cho mượt mà)
        self.tabview = ctk.CTkTabview(self, fg_color="white", corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=15)

        # Tạo 3 Tab chính
        self.tab_search = self.tabview.add("🔍 Tìm & Đặt Phòng")
        self.tab_bookings = self.tabview.add("📋 Đặt Phòng Của Tôi")
        self.tab_profile = self.tabview.add("👤 Thông Tin Cá Nhân")

        # Khởi tạo nội dung từng Tab
        self.setup_search_tab()
        self.setup_bookings_tab()
        self.setup_profile_tab()

    # ================= HEADER =================
    def create_header(self):
        header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#0b3b60")
        header.pack(fill="x", side="top")

        # Title
        lbl_title = ctk.CTkLabel(
            header, text="🏨 Hotel Booking System", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="white"
        )
        lbl_title.pack(side="left", padx=25, pady=15)

        # Right side: User info & Logout
        user_box = ctk.CTkFrame(header, fg_color="transparent")
        user_box.pack(side="right", padx=25)

        lbl_user = ctk.CTkLabel(
            user_box, text=f"👋 Xin chào, {self.username}", 
            font=ctk.CTkFont(size=14, weight="bold"), text_color="white"
        )
        lbl_user.pack(side="left", padx=(0, 15))

        btn_logout = ctk.CTkButton(
            user_box, text="Đăng xuất", width=90, height=32,
            fg_color="#e74c3c", hover_color="#c0392b",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.logout
        )
        btn_logout.pack(side="left")

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.destroy()

    # ================= TAB 1: TÌM & ĐẶT PHÒNG =================
    def setup_search_tab(self):
        # 1. Thanh Lọc / Tìm Kiếm
        filter_frame = ctk.CTkFrame(self.tab_search, fg_color="#f8f9fa", corner_radius=8, border_width=1, border_color="#e0e0e0")
        filter_frame.pack(fill="x", padx=15, pady=15)

        # Hàng 1: Bộ lọc
        ctk.CTkLabel(filter_frame, text="Loại phòng:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        combo_type = ctk.CTkComboBox(filter_frame, values=["Tất cả", "Phòng Đơn (Single)", "Phòng Đôi (Double)", "Phòng VIP (Suite)"], width=180)
        combo_type.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(filter_frame, text="Ngày nhận:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        entry_checkin = ctk.CTkEntry(filter_frame, placeholder_text="dd/mm/yyyy", width=140)
        entry_checkin.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(filter_frame, text="Ngày trả:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=4, padx=10, pady=10, sticky="w")
        entry_checkout = ctk.CTkEntry(filter_frame, placeholder_text="dd/mm/yyyy", width=140)
        entry_checkout.grid(row=0, column=5, padx=10, pady=10)

        btn_search = ctk.CTkButton(
            filter_frame, text="🔎 Tìm Phòng", width=120, height=36, 
            fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold")
        )
        btn_search.grid(row=0, column=6, padx=15, pady=10)

        # 2. Danh Sách Phòng (Scrollable Frame)
        rooms_scroll = ctk.CTkScrollableFrame(self.tab_search, fg_color="transparent")
        rooms_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # Dữ liệu phòng mẫu
        rooms_data = [
            {"name": "Deluxe Ocean View", "type": "Phòng Đôi", "price": "1,500,000 VNĐ / đêm", "details": "Bed: 1 King Size | View: Biển | Điều hòa, Wifi, Ban công"},
            {"name": "Standard Single Room", "type": "Phòng Đơn", "price": "650,000 VNĐ / đêm", "details": "Bed: 1 Single | View: Thành phố | Điều hòa, Wifi, Tivi"},
            {"name": "Executive Suite VIP", "type": "Phòng VIP (Suite)", "price": "3,200,000 VNĐ / đêm", "details": "Bed: 1 Super King | View: Toàn cảnh | Bồn tắm, Minibar, Ăn sáng miễn phí"},
            {"name": "Family Superior", "type": "Phòng Đôi", "price": "2,100,000 VNĐ / đêm", "details": "Bed: 2 Queen Size | View: Hồ bơi | Thích hợp cho 4 người"},
        ]

        for room in rooms_data:
            card = ctk.CTkFrame(rooms_scroll, fg_color="#ffffff", corner_radius=8, border_width=1, border_color="#e0e0e0")
            card.pack(fill="x", pady=8, padx=5)

            # Khung thông tin phòng (Trái)
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=20, pady=15, fill="both", expand=True)

            ctk.CTkLabel(info_frame, text=room["name"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Loại: {room['type']}", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=(2, 5))
            ctk.CTkLabel(info_frame, text=f"✨ {room['details']}", font=ctk.CTkFont(size=12), text_color="#444444").pack(anchor="w")

            # Khung Giá & Nút Đặt (Phải)
            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side="right", padx=20, pady=15)

            ctk.CTkLabel(action_frame, text=room["price"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#d35400").pack(pady=(0, 8))
            
            btn_book = ctk.CTkButton(
                action_frame, text="Đặt phòng ngay", width=140, height=36,
                fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda r=room["name"]: self.book_room_action(r)
            )
            btn_book.pack()

    def book_room_action(self, room_name):
        messagebox.showinfo("Đặt phòng", f"Bạn đã chọn đặt phòng: {room_name}\nHệ thống sẽ chuyển sang bước xác nhận thanh toán.")

    # ================= TAB 2: ĐẶT PHÒNG CỦA TÔI =================
    def setup_bookings_tab(self):
        container = ctk.CTkFrame(self.tab_bookings, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(container, text="Danh sách các phòng bạn đã đặt", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0b3b60").pack(anchor="w", pady=(0, 15))

        # Sử dụng Treeview của tkinter để làm bảng lịch sử
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#0b3b60", foreground="white")
        style.map("Treeview", background=[("selected", "#1f538d")])

        tree_frame = ctk.CTkFrame(container, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True)

        columns = ("id", "room", "checkin", "checkout", "total", "status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        tree.heading("id", text="Mã Đặt")
        tree.heading("room", text="Tên Phòng")
        tree.heading("checkin", text="Ngày Nhận")
        tree.heading("checkout", text="Ngày Trả")
        tree.heading("total", text="Tổng Tiền")
        tree.heading("status", text="Trạng Thái")

        tree.column("id", width=90, anchor="center")
        tree.column("room", width=220, anchor="w")
        tree.column("checkin", width=120, anchor="center")
        tree.column("checkout", width=120, anchor="center")
        tree.column("total", width=140, anchor="center")
        tree.column("status", width=130, anchor="center")

        # Dữ liệu mẫu lịch sử
        history = [
            ("BK001", "Deluxe Ocean View", "10/10/2026", "12/10/2026", "3,000,000 VNĐ", "Đã xác nhận"),
            ("BK002", "Standard Single Room", "01/08/2026", "02/08/2026", "650,000 VNĐ", "Hoàn thành"),
            ("BK003", "Family Superior", "15/05/2026", "17/05/2026", "4,200,000 VNĐ", "Đã hủy"),
        ]

        for item in history:
            tree.insert("", "end", values=item)

        tree.pack(side="left", fill="both", expand=True)

        # Scrollbar cho bảng
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Nút chức năng phía dưới bảng
        btn_box = ctk.CTkFrame(container, fg_color="transparent")
        btn_box.pack(fill="x", pady=15)

        btn_cancel = ctk.CTkButton(
            btn_box, text="Hủy đặt phòng đã chọn", fg_color="#e74c3c", hover_color="#c0392b",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: messagebox.showwarning("Thông báo", "Vui lòng chọn mã đặt phòng cần hủy!")
        )
        btn_cancel.pack(side="right")

    # ================= TAB 3: THÔNG TIN CÁ NHÂN =================
    def setup_profile_tab(self):
        card = ctk.CTkFrame(self.tab_profile, width=550, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="CẬP NHẬT THÔNG TIN CÁ NHÂN", font=ctk.CTkFont(size=18, weight="bold"), text_color="#0b3b60").pack(pady=(25, 20))

        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(padx=40, fill="x")

        # Họ và tên
        ctk.CTkLabel(form_frame, text="Họ và tên:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=8)
        entry_name = ctk.CTkEntry(form_frame, width=320)
        entry_name.insert(0, self.username)
        entry_name.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Email
        ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, sticky="w", pady=8)
        entry_email = ctk.CTkEntry(form_frame, width=320)
        entry_email.insert(0, "demo@member.com")
        entry_email.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Số điện thoại
        ctk.CTkLabel(form_frame, text="Số điện thoại:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, sticky="w", pady=8)
        entry_phone = ctk.CTkEntry(form_frame, width=320)
        entry_phone.insert(0, "0901234567")
        entry_phone.grid(row=2, column=1, pady=8, padx=(10, 0))

        # Ngày sinh
        ctk.CTkLabel(form_frame, text="Ngày sinh:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=3, column=0, sticky="w", pady=8)
        entry_dob = ctk.CTkEntry(form_frame, width=320)
        entry_dob.insert(0, "01/01/1998")
        entry_dob.grid(row=3, column=1, pady=8, padx=(10, 0))

        # Giới tính
        ctk.CTkLabel(form_frame, text="Giới tính:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=4, column=0, sticky="w", pady=8)
        combo_gender = ctk.CTkComboBox(form_frame, values=["Nam", "Nữ", "Khác"], width=320)
        combo_gender.set("Nam")
        combo_gender.grid(row=4, column=1, pady=8, padx=(10, 0))

        # Nút Lưu thay đổi
        btn_save = ctk.CTkButton(
            card, text="Lưu Thay Đổi", width=200, height=40,
            fg_color="#0b3b60", hover_color="#082b47", font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: messagebox.showinfo("Thành công", "Đã cập nhật thông tin cá nhân thành công!")
        )
        btn_save.pack(pady=(20, 25))


if __name__ == "__main__":
    app = MemberDashboard(username="Nguyen Van A")
    app.mainloop()