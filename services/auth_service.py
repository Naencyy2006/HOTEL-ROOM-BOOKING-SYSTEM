from config.database import db
from utils.password import hash_password, verify_password
from utils.validators import validate_email, validate_password, validate_phone

class AuthService:
    def __init__(self):
        # Lưu thông tin phiên đăng nhập của người dùng hiện tại
        self.current_user = None

    def register(self, full_name: str, dob: str, gender: str, phone: str, email: str, password: str, confirm_password: str):
        # Bước 1: Kiểm tra tính hợp lệ của dữ liệu đầu vào
        if not validate_email(email):
            return False, "Invalid email address format."
        if not validate_password(password):
            return False, "Password must be at least 6 characters long."
        if password != confirm_password:
            return False, "Password confirmation does not match."
        if not validate_phone(phone):
            return False, "Invalid phone number format."

        conn = db.get_connection()
        if not conn:
            return False, "Database connection error."
        cursor = conn.cursor(dictionary=True)

        try:
            # Bước 2: Kiểm tra email đã tồn tại trong bảng USERS chưa
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "This email is already registered in the system."

            # Bước 3: Mã hóa mật khẩu
            hashed_pwd = hash_password(password)
            
            # Trích xuất năm sinh từ chuỗi ngày sinh YYYY-MM-DD
            year_of_birth = int(dob.split('-')[0]) if '-' in dob and dob.split('-')[0].isdigit() else None

            # Bước 4: Thêm tài khoản Member mới vào CSDL
            query = """
                INSERT INTO USERS (full_name, email, phone, gender, year_of_birth, password_hash, role, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Member', 'Active')
            """
            cursor.execute(query, (full_name, email, phone, gender, year_of_birth, hashed_pwd))
            conn.commit()
            return True, "Account registered successfully!"
            
        except Exception as e:
            conn.rollback()
            return False, f"Database error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    def login(self, email: str, password: str):
        conn = db.get_connection()
        if not conn:
            return False, "Database connection error.", None
        cursor = conn.cursor(dictionary=True)

        try:
            # Lấy thông tin tài khoản theo email
            cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()

            # Kiểm tra sự tồn tại tài khoản và xác thực mật khẩu
            if not user or not verify_password(user['password_hash'], password):
                return False, "Invalid email address or password.", None

            # Kiểm tra xem tài khoản có bị khóa bởi Administrator không
            if user['status'] == 'Locked':
                return False, "Your account is locked due to policy violations. Contact support.", None

            # Đăng nhập thành công, lưu thông tin phiên làm việc
            self.current_user = user
            return True, "Login successful!", user
        finally:
            cursor.close()
            conn.close()

    def logout(self):
        # Xóa thông tin phiên làm việc hiện tại
        self.current_user = None
        return True, "Logged out successfully."

    def reset_password(self, email: str, new_password: str, confirm_password: str):
        # Validate the new password requirements.
        if not validate_password(new_password):
            return False, "New password must be at least 6 characters long."
        if new_password != confirm_password:
            return False, "Password confirmation does not match."

        conn = db.get_connection()
        if not conn:
            return False, "Database connection error."
        cursor = conn.cursor(dictionary=True)

        try:
            # Check whether the email exists.
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Email address not found."

            # Hash and update the new password.
            hashed_pwd = hash_password(new_password)
            cursor.execute("UPDATE USERS SET password_hash = %s WHERE email = %s", (hashed_pwd, email))
            conn.commit()
            return True, "Password updated successfully."
        except Exception as e:
            conn.rollback()
            return False, f"Error updating password: {str(e)}"
        finally:
            cursor.close()
            conn.close()