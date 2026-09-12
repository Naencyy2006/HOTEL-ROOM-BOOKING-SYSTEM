# views/login.py
import tkinter as tk
from tkinter import ttk, messagebox

from config.database import db
from services.auth_service import AuthService

# Bộ màu Tím Pastel đồng bộ
COLOR_MAIN_BG = "#F5EFFF"
COLOR_SIDEBAR = "#E5D9F2"
COLOR_BUTTON  = "#CDC1FF"
COLOR_ACCENT  = "#A594F9"
COLOR_TEXT    = "#3B2F63"
COLOR_WHITE   = "#FFFFFF"

FONT_TITLE = ("Arial", 16, "bold")
FONT_HEADER = ("Arial", 11, "bold")
FONT_BOLD = ("Arial", 9, "bold")
FONT_NORMAL = ("Arial", 9)


class LoginRegisterView(tk.Frame):
    def __init__(self, parent, db_conn=None, initial_tab="login", on_login_success=None, on_back_guest=None):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.conn = db_conn
        self.on_login_success = on_login_success
        self.on_back_guest = on_back_guest
        self.auth_service = AuthService()

        self._build_header()

        # Tạo Card Form đặt ở giữa màn hình
        self.card = tk.Frame(self, bg=COLOR_WHITE, padx=30, pady=25)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

        self.container = tk.Frame(self.card, bg=COLOR_WHITE)
        self.container.pack(fill="both", expand=True)

        self.login_frame = tk.Frame(self.container, bg=COLOR_WHITE)
        self.register_frame = tk.Frame(self.container, bg=COLOR_WHITE)
        self.reset_frame = tk.Frame(self.container, bg=COLOR_WHITE)

        self._build_login_form()
        self._build_register_form()
        self._build_reset_form()

        if initial_tab == "register":
            self.show_register()
        else:
            self.show_login()

    def _build_header(self):
        header = tk.Frame(self, bg=COLOR_ACCENT, height=55)
        header.pack(fill="x")

        # Nút Quay lại màn hình Khách
        btn_back = tk.Button(
            header, text="← Back to Guest", command=self._back,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, bd=0, cursor="hand2"
        )
        btn_back.pack(side="left", padx=15, pady=10)

        tab_frame = tk.Frame(header, bg=COLOR_ACCENT)
        tab_frame.pack(side="right", padx=20)

        self.btn_tab_login = tk.Button(
            tab_frame, text="LOG IN", command=self.show_login,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_HEADER, bd=0, cursor="hand2", padx=10
        )
        self.btn_tab_login.pack(side="left")

        tk.Label(tab_frame, text="|", bg=COLOR_ACCENT, fg=COLOR_SIDEBAR, font=FONT_HEADER).pack(side="left", padx=2)

        self.btn_tab_register = tk.Button(
            tab_frame, text="REGISTER", command=self.show_register,
            bg=COLOR_ACCENT, fg=COLOR_SIDEBAR, font=FONT_HEADER, bd=0, cursor="hand2", padx=10
        )
        self.btn_tab_register.pack(side="left")

    def show_login(self):
        self.register_frame.pack_forget()
        self.reset_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
        self.btn_tab_login.config(fg=COLOR_WHITE, font=("Arial", 11, "bold"))
        self.btn_tab_register.config(fg=COLOR_SIDEBAR, font=("Arial", 11, "normal"))

    def show_register(self):
        self.login_frame.pack_forget()
        self.reset_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)
        self.btn_tab_register.config(fg=COLOR_WHITE, font=("Arial", 11, "bold"))
        self.btn_tab_login.config(fg=COLOR_SIDEBAR, font=("Arial", 11, "normal"))

    def show_reset(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.reset_frame.pack(fill="both", expand=True)
        self.btn_tab_login.config(fg=COLOR_SIDEBAR, font=("Arial", 11, "normal"))
        self.btn_tab_register.config(fg=COLOR_SIDEBAR, font=("Arial", 11, "normal"))

    def _back(self):
        if self.on_back_guest:
            self.on_back_guest()

    def _build_login_form(self):
        tk.Label(self.login_frame, text="Welcome Back", font=FONT_TITLE, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w", pady=(10, 15))

        tk.Label(self.login_frame, text="Email", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_login_user = tk.Entry(self.login_frame, font=FONT_NORMAL)
        self.txt_login_user.pack(fill="x", pady=(2, 12), ipady=4)

        tk.Label(self.login_frame, text="Password", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_login_pass = tk.Entry(self.login_frame, font=FONT_NORMAL, show="*")
        self.txt_login_pass.pack(fill="x", pady=(2, 20), ipady=4)

        btn_submit = tk.Button(
            self.login_frame, text="LOG IN", command=self._handle_login,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, bd=0, pady=8, cursor="hand2"
        )
        btn_submit.pack(fill="x", pady=5)

        btn_forgot_password = tk.Button(
            self.login_frame,
            text="Forgot Password?",
            command=self.show_reset,
            bg=COLOR_WHITE,
            fg=COLOR_ACCENT,
            font=FONT_BOLD,
            bd=0,
            cursor="hand2",
        )
        btn_forgot_password.pack(pady=(8, 0))

    def _build_reset_form(self):
        form = self.reset_frame
        tk.Label(
            form, text="Reset Password", font=FONT_TITLE,
            bg=COLOR_WHITE, fg=COLOR_TEXT
        ).pack(anchor="w", pady=(0, 15))

        fields = []
        for label, show in (("Email", None), ("New Password", "*"), ("Confirm Password", "*")):
            tk.Label(form, text=label, font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
            entry = tk.Entry(form, font=FONT_NORMAL, show=show)
            entry.pack(fill="x", pady=(2, 8), ipady=3)
            fields.append(entry)

        def submit_reset():
            email, new_password, confirm_password = [field.get().strip() for field in fields]
            if not email or not new_password or not confirm_password:
                messagebox.showwarning("Warning", "Please fill in all fields.", parent=self)
                return

            success, message = self.auth_service.reset_password(
                email, new_password, confirm_password
            )
            if success:
                messagebox.showinfo("Success", message, parent=self)
                self.show_login()
            else:
                messagebox.showerror("Reset Failed", message, parent=self)

        tk.Button(
            form, text="RESET PASSWORD", command=submit_reset,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD,
            bd=0, pady=7, cursor="hand2"
        ).pack(fill="x", pady=(5, 0))

        tk.Button(
            form, text="Back to Login", command=self.show_login,
            bg=COLOR_WHITE, fg=COLOR_ACCENT, font=FONT_BOLD,
            bd=0, cursor="hand2"
        ).pack(pady=(8, 0))

    def _build_register_form(self):
        tk.Label(self.register_frame, text="Create Account", font=FONT_TITLE, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w", pady=(5, 10))

        tk.Label(self.register_frame, text="Full Name", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_reg_name = tk.Entry(self.register_frame, font=FONT_NORMAL)
        self.txt_reg_name.pack(fill="x", pady=(2, 6), ipady=3)

        tk.Label(self.register_frame, text="Phone", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_reg_phone = tk.Entry(self.register_frame, font=FONT_NORMAL)
        self.txt_reg_phone.pack(fill="x", pady=(2, 6), ipady=3)

        tk.Label(self.register_frame, text="Email", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_reg_email = tk.Entry(self.register_frame, font=FONT_NORMAL)
        self.txt_reg_email.pack(fill="x", pady=(2, 6), ipady=3)

        tk.Label(self.register_frame, text="Gender", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.cbo_reg_gender = ttk.Combobox(self.register_frame, values=["Male", "Female", "Other"], state="readonly", width=30)
        self.cbo_reg_gender.current(0)
        self.cbo_reg_gender.pack(fill="x", pady=(2, 6), ipady=3)

        tk.Label(self.register_frame, text="Date of Birth (YYYY-MM-DD)", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_reg_dob = tk.Entry(self.register_frame, font=FONT_NORMAL)
        self.txt_reg_dob.pack(fill="x", pady=(2, 6), ipady=3)

        tk.Label(self.register_frame, text="Password", font=FONT_BOLD, bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        self.txt_reg_pass = tk.Entry(self.register_frame, font=FONT_NORMAL, show="*")
        self.txt_reg_pass.pack(fill="x", pady=(2, 12), ipady=3)

        btn_submit = tk.Button(
            self.register_frame, text="REGISTER NOW", command=self._handle_register,
            bg=COLOR_ACCENT, fg=COLOR_WHITE, font=FONT_BOLD, bd=0, pady=8, cursor="hand2"
        )
        btn_submit.pack(fill="x", pady=5)

    def _handle_login(self):
        email = self.txt_login_user.get().strip()
        password = self.txt_login_pass.get().strip()

        if not email or not password:
            messagebox.showwarning("Warning", "Please enter both Email and Password.")
            return

        try:
            is_success, message, user = self.auth_service.login(email, password)

            if is_success and user:
                messagebox.showinfo("Success", f"Login successful! Welcome {user.get('full_name', email)}")
                if self.on_login_success:
                    self.on_login_success(user)
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Query Error", f"Database error:\n{e}")

    def _handle_register(self):
        fullname = self.txt_reg_name.get().strip()
        phone = self.txt_reg_phone.get().strip()
        email = self.txt_reg_email.get().strip()
        gender = self.cbo_reg_gender.get().strip()
        dob = self.txt_reg_dob.get().strip()
        password = self.txt_reg_pass.get().strip()

        if not all([fullname, phone, email, gender, dob, password]):
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

        try:
            success, message = self.auth_service.register(
                full_name=fullname,
                dob=dob,
                gender=gender,
                phone=phone,
                email=email,
                password=password,
                confirm_password=password,
            )

            if success:
                messagebox.showinfo("Success", message)
                self.show_login()
            else:
                messagebox.showerror("Registration Failed", message)
        except Exception as e:
            messagebox.showerror("Registration Failed", f"Error: {e}")


class LoginView(tk.Tk):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.title("Hotel Booking System")
        self.geometry("620x520")
        self.minsize(500, 440)
        self.configure(bg=COLOR_MAIN_BG)
        self.on_login_success = on_login_success

        self.login_frame = LoginRegisterView(
            self,
            db_conn=db.get_connection(),
            on_login_success=self._handle_success,
            on_back_guest=None,
        )
        self.login_frame.pack(fill="both", expand=True)

    def _handle_success(self, user):
        if self.on_login_success:
            self.on_login_success(user)
        else:
            self.destroy()