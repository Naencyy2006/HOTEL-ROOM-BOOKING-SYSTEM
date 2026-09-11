import getpass
from services.auth_service import AuthService

class LoginView:
    def __init__(self):
        self.auth_service = AuthService()

    def display_menu(self):
        # Hiển thị menu chức năng chính của giao diện xác thực
        while True:
            print("\n" + "=" * 40)
            print("      HOTEL ROOM BOOKING SYSTEM      ")
            print("=" * 40)
            print("1. Login")
            print("2. Register Member Account")
            print("3. Forgot Password")
            print("0. Exit")
            
            choice = input("\nPlease select an option (0-3): ").strip()

            if choice == '1':
                user = self.show_login()
                if user:
                    # Trả về thông tin user để main.py điều hướng theo Role
                    return user
            elif choice == '2':
                self.show_register()
            elif choice == '3':
                self.show_reset_password()
            elif choice == '0':
                print("Thank you for visiting our system!")
                return None
            else:
                print("Invalid option selected. Please try again.")

    def show_login(self):
        # Xử lý nhập thông tin đăng nhập từ người dùng
        print("\n--- USER LOGIN ---")
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ").strip()

        success, message, user = self.auth_service.login(email, password)
        print(f"\nResult: {message}")
        return user if success else None

    def show_register(self):
        # Xử lý nhập thông tin đăng ký tài khoản Member mới
        print("\n--- MEMBER ACCOUNT REGISTRATION ---")
        full_name = input("Full Name *: ").strip()
        dob = input("Date of Birth (YYYY-MM-DD): ").strip()
        gender = input("Gender (Male/Female/Other): ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email Address *: ").strip()
        password = getpass.getpass("Password (min 6 chars) *: ").strip()
        confirm_password = getpass.getpass("Confirm Password *: ").strip()

        success, message = self.auth_service.register(
            full_name, dob, gender, phone, email, password, confirm_password
        )
        print(f"\nResult: {message}")

    def show_reset_password(self):
        # Xử lý nhập thông tin khôi phục mật khẩu
        print("\n--- RESET ACCOUNT PASSWORD ---")
        email = input("Enter your registered Email: ").strip()
        new_password = getpass.getpass("New Password: ").strip()
        confirm_password = getpass.getpass("Confirm New Password: ").strip()

        success, message = self.auth_service.reset_password(email, new_password, confirm_password)
        print(f"\nResult: {message}")