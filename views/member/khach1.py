import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class RegisterFrame(ctk.CTkFrame):
    """Màn hình Đăng ký tài khoản thành viên"""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Card màu trắng căn giữa màn hình
        card = ctk.CTkFrame(self, width=540, fg_color="white", corner_radius=8, border_width=1, border_color="#e0e0e0")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề
        ctk.CTkLabel(
            card, text="Dang ky tai khoan thanh vien", 
            font=ctk.CTkFont(size=22, weight="bold"), 
            text_color="#0b3b60"
        ).pack(pady=(25, 20))

        # Form bố cục Grid (2 cột)
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Hàng 1: Ho va ten * | Ngay sinh (dd/mm/yyyy)
        lbl_fullname = ctk.CTkLabel(form_frame, text="Full name *", text_color="#555555", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_fullname.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 2))
        self.entry_fullname = ctk.CTkEntry(form_frame, width=225, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_fullname.grid(row=1, column=0, padx=5, pady=(0, 10))

        lbl_dob = ctk.CTkLabel(form_frame, text="Date of birth (dd/mm/yyyy)", text_color="#555555", font=ctk.CTkFont(size=12))
        lbl_dob.grid(row=0, column=1, sticky="w", padx=5, pady=(5, 2))
        self.entry_dob = ctk.CTkEntry(form_frame, width=225, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_dob.grid(row=1, column=1, padx=5, pady=(0, 10))

        # Hàng 2: So dien thoại | Gioi tinh
        lbl_phone = ctk.CTkLabel(form_frame, text="Phone number", text_color="#555555", font=ctk.CTkFont(size=12))
        lbl_phone.grid(row=2, column=0, sticky="w", padx=5, pady=(5, 2))
        self.entry_phone = ctk.CTkEntry(form_frame, width=225, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_phone.grid(row=3, column=0, padx=5, pady=(0, 10))

        lbl_gender = ctk.CTkLabel(form_frame, text="Gender", text_color="#555555", font=ctk.CTkFont(size=12))
        lbl_gender.grid(row=2, column=1, sticky="w", padx=5, pady=(5, 2))
        self.combo_gender = ctk.CTkComboBox(form_frame, values=["Male", "Female", "Other"], width=225, height=36, corner_radius=4, border_color="#aaaaaa", fg_color="white", text_color="black")
        self.combo_gender.set("Male")
        self.combo_gender.grid(row=3, column=1, padx=5, pady=(0, 10))

        # Hàng 3: Email * (Full chiều ngang)
        lbl_email = ctk.CTkLabel(form_frame, text="Email *", text_color="#555555", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_email.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 2))
        self.entry_email = ctk.CTkEntry(form_frame, width=460, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_email.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 10))

        # Hàng 4: Mat khau * (toi thieu 6 ky tu) | Xac nhan mat khau *
        lbl_pass = ctk.CTkLabel(form_frame, text="Password * (minimum 6 characters)", text_color="#555555", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_pass.grid(row=6, column=0, sticky="w", padx=5, pady=(5, 2))
        self.entry_pass = ctk.CTkEntry(form_frame, show="*", width=225, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_pass.grid(row=7, column=0, padx=5, pady=(0, 15))

        lbl_confirm_pass = ctk.CTkLabel(form_frame, text="Confirm Password *", text_color="#555555", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_confirm_pass.grid(row=6, column=1, sticky="w", padx=5, pady=(5, 2))
        self.entry_confirm_pass = ctk.CTkEntry(form_frame, show="*", width=225, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_confirm_pass.grid(row=7, column=1, padx=5, pady=(0, 15))

        # Nút Dang ky
        btn_register = ctk.CTkButton(
            card, text="Register", width=460, height=40, 
            fg_color="#0b3b60", hover_color="#082b47",
            font=ctk.CTkFont(size=14, weight="bold"), 
            corner_radius=4,
            command=self.handle_register
        )
        btn_register.pack(pady=(5, 15))

        # Link chuyển sang Dang nhap
        bottom_frame = ctk.CTkFrame(card, fg_color="transparent")
        bottom_frame.pack(pady=(0, 25))

        ctk.CTkLabel(bottom_frame, text="Already have an account? ", font=ctk.CTkFont(size=13), text_color="#555555").pack(side="left")
        btn_to_login = ctk.CTkButton(
            bottom_frame, text="Login", fg_color="transparent", text_color="#0b3b60",
            hover=False, font=ctk.CTkFont(size=13, weight="bold"), width=70,
            command=lambda: controller.show_frame("LoginFrame")
        )
        btn_to_login.pack(side="left")

    def handle_register(self):
        fullname = self.entry_fullname.get().strip()
        email = self.entry_email.get().strip()
        pwd = self.entry_pass.get().strip()
        confirm_pwd = self.entry_confirm_pass.get().strip()

        # Kiểm tra bắt buộc nhập các trường có dấu *
        if not fullname or not email or not pwd or not confirm_pwd:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ các trường bắt buộc (*)! ")
            return

        if len(pwd) < 6:
            messagebox.showwarning("Thông báo", "Mật khẩu phải chứa tối thiểu 6 ký tự!")
            return

        if pwd != confirm_pwd:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không trùng khớp!")
            return

        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        self.controller.show_frame("LoginFrame")


class LoginFrame(ctk.CTkFrame):
    """Màn hình Đăng nhập"""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Card màu trắng căn giữa màn hình
        card = ctk.CTkFrame(self, width=420, fg_color="white", corner_radius=8, border_width=1, border_color="#e0e0e0")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề
        ctk.CTkLabel(
            card, text="Login", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            text_color="#0b3b60"
        ).pack(pady=(25, 4))

        # Dòng phụ đề tài khoản demo
        ctk.CTkLabel(
            card, text="", 
            font=ctk.CTkFont(size=12), 
            text_color="gray"
        ).pack(pady=(0, 20))

        # Khung chứa Form
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(padx=35, fill="x")

        # Email
        lbl_email = ctk.CTkLabel(form_frame, text="Email", text_color="#555555", font=ctk.CTkFont(size=12))
        lbl_email.pack(anchor="w", pady=(0, 2))
        self.entry_email = ctk.CTkEntry(form_frame, width=350, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_email.pack(pady=(0, 15))

        # Mat khau
        lbl_pass = ctk.CTkLabel(form_frame, text="Password", text_color="#555555", font=ctk.CTkFont(size=12))
        lbl_pass.pack(anchor="w", pady=(0, 2))
        self.entry_pass = ctk.CTkEntry(form_frame, show="*", width=350, height=36, corner_radius=4, border_color="#aaaaaa")
        self.entry_pass.pack(pady=(0, 20))

        # Nút Dang nhap
        btn_login = ctk.CTkButton(
            card, text="Login", width=350, height=40, 
            fg_color="#0b3b60", hover_color="#082b47",
            font=ctk.CTkFont(size=14, weight="bold"), 
            corner_radius=4,
            command=self.handle_login
        )
        btn_login.pack(pady=(0, 20))

        # Các liên kết phía dưới
        bottom_frame = ctk.CTkFrame(card, fg_color="transparent", width=350)
        bottom_frame.pack(pady=(0, 25), fill="x", padx=35)

        btn_forgot = ctk.CTkButton(
            bottom_frame, text="Forgot Password?", fg_color="transparent", text_color="#0b3b60",
            hover=False, font=ctk.CTkFont(size=12), width=100, anchor="w",
            command=lambda: messagebox.showinfo("Thông báo", "Vui lòng liên hệ Admin để khôi phục mật khẩu.")
        )
        btn_forgot.pack(side="left")

        btn_to_reg = ctk.CTkButton(
            bottom_frame, text="Register", fg_color="transparent", text_color="#0b3b60",
            hover=False, font=ctk.CTkFont(size=12), width=130, anchor="e",
            command=lambda: controller.show_frame("RegisterFrame")
        )
        btn_to_reg.pack(side="right")

    def handle_login(self):
        email = self.entry_email.get().strip()
        pwd = self.entry_pass.get().strip()

        if not email or not pwd:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ Email và Mật khẩu!")
            return

        messagebox.showinfo("Thành công", f"Đăng nhập thành công với email: {email}")


class HotelBookingApp(ctk.CTk):
    """Cửa sổ chính ứng dụng kết nối 2 màn hình"""
    def __init__(self):
        super().__init__()

        self.title("Hotel Booking System")
        window_width, window_height = 1100, 680
        center_x = int((self.winfo_screenwidth() - window_width) / 2)
        center_y = int((self.winfo_screenheight() - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(950, 600)

        # Màu nền xám nhạt đằng sau Card
        self.configure(fg_color="#f3f5f8")

        # 1. TOP HEADER BAR (Thanh tiêu đề màu xanh đậm)
        self.top_header = ctk.CTkFrame(self, height=55, corner_radius=0, fg_color="#0b3b60")
        self.top_header.pack(fill="x", side="top")

        self.lbl_system_title = ctk.CTkLabel(
            self.top_header, text="Hotel Booking System",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="white"
        )
        self.lbl_system_title.pack(side="left", padx=30, pady=12)

        # Điều hướng góc phải: Tim phong | Dang nhap | Dang ky
        self.nav_box = ctk.CTkFrame(self.top_header, fg_color="transparent")
        self.nav_box.pack(side="right", padx=30)

        btn_nav_search = ctk.CTkButton(
            self.nav_box, text="", width=90, height=32, fg_color="transparent",
            hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold"), text_color="white",
            command=lambda: messagebox.showinfo("Thông báo", "Chuyển đến trang Tìm phòng")
        )
        btn_nav_search.pack(side="left", padx=5)

        btn_nav_login = ctk.CTkButton(
            self.nav_box, text="Login", width=90, height=32, fg_color="transparent",
            hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold"), text_color="white",
            command=lambda: self.show_frame("LoginFrame")
        )
        btn_nav_login.pack(side="left", padx=5)

        btn_nav_register = ctk.CTkButton(
            self.nav_box, text="Register", width=90, height=32, fg_color="transparent",
            hover_color="#082b47", font=ctk.CTkFont(size=13, weight="bold"), text_color="white",
            command=lambda: self.show_frame("RegisterFrame")
        )
        btn_nav_register.pack(side="left", padx=5)

        # 2. KHUNG CHÍNH CHỨA MÀN HÌNH
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Khởi tạo các View
        self.frames = {}
        for F in (LoginFrame, RegisterFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mặc định mở màn hình Đăng ký (như trong ảnh mẫu 1)
        self.show_frame("RegisterFrame")

    def show_frame(self, page_name):
        """Hàm thực hiện chuyển đổi giữa các màn hình"""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = HotelBookingApp()
    app.mainloop()