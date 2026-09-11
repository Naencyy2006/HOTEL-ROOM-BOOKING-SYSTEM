import getpass
from services.auth_service import AuthService

class LoginView:
    def __init__(self):
        self.auth_service = AuthService()

    def display_menu(self):
        while True:
            print("\n" + "="*35)
            print(" HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN ")
            print("="*35)
            print("1. Đăng nhập[cite: 1]")
            print("2. Đăng ký tài khoản[cite: 1]")
            print("3. Quên mật khẩu[cite: 1]")
            print("0. Thoát")
            
            choice = input("Vui lòng chọn chức năng (0-3): ").strip()

            if choice == '1':
                user = self.show_login()
                if user:
                    return user  # Trả về thông tin user để main.py điều hướng theo Role[cite: 1]
            elif choice == '2':
                self.show_register()
            elif choice == '3':
                self.show_reset_password()
            elif choice == '0':
                print("Cảm ơn bạn đã sử dụng dịch vụ!")
                return None
            else:
                print("Lựa chọn không hợp lệ, vui lòng thử lại.")

    def show_login(self):
        print("\n--- ĐĂNG NHẬP[cite: 1] ---")
        email = input("Email: ").strip()
        password = getpass.getpass("Mật khẩu: ").strip()

        success, message, user = self.auth_service.login(email, password)
        print(message)
        return user if success else None

    def show_register(self):
        print("\n--- ĐĂNG KÝ TÀI KHOẢN MỚI[cite: 1] ---")
        full_name = input("Họ và tên *: ").strip()
        dob = input("Ngày sinh (YYYY-MM-DD): ").strip()
        gender = input("Giới tính (Male/Female/Other): ").strip()
        phone = input("Số điện thoại: ").strip()
        email = input("Email *: ").strip()
        password = getpass.getpass("Mật khẩu (ít nhất 6 ký tự) *: ").strip()[cite: 1]
        confirm_password = getpass.getpass("Xác nhận mật khẩu *: ").strip()[cite: 1]

        success, message = self.auth_service.register(
            full_name, dob, gender, phone, email, password, confirm_password
        )
        print(f"\n{message}")

    def show_reset_password(self):
        print("\n--- KHÔI PHỤC MẬT KHẨU[cite: 1] ---")
        email = input("Nhập email đã đăng ký: ").strip()
        new_password = getpass.getpass("Mật khẩu mới: ").strip()
        confirm_password = getpass.getpass("Xác nhận mật khẩu mới: ").strip()

        success, message = self.auth_service.reset_password(email, new_password, confirm_password)
        print(f"\n{message}")