import os
import mysql.connector
from mysql.connector import Error

# Lớp Database để quản lý kết nối cơ sở dữ liệu MySQL
class Database:

    # Khởi tạo đối tượng Database với các thông tin kết nối cơ sở dữ liệu
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")   # Lấy địa chỉ host từ biến môi trường DB_HOST, nếu không có thì mặc định là "localhost"
        self.port = int(os.getenv("DB_PORT", "3306"))   # Lấy cổng kết nối từ biến môi trường DB_PORT, nếu không có thì mặc định là 3306
        self.database = os.getenv("DB_NAME", "hotel_room_booking") # Lấy tên cơ sở dữ liệu từ biến môi trường DB_NAME, nếu không có thì mặc định là "hotel_room_booking"
        self.user = os.getenv("DB_USER", "root")        # Lấy tên người dùng từ biến môi trường DB_USER, nếu không có thì mặc định là "root"
        self.password = os.getenv("DB_PASSWORD", "")    # Lấy mật khẩu từ biến môi trường DB_PASSWORD, nếu không có thì mặc định là chuỗi rỗng

    # Phương thức để tạo kết nối đến cơ sở dữ liệu MySQL
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )

            # Kiểm tra xem kết nối có thành công hay không
            if connection.is_connected():
                return connection

            return None

        # Xử lý lỗi kết nối cơ sở dữ liệu
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    # Phương thức để kiểm tra kết nối cơ sở dữ liệu
    def test_connection(self):
        connection = self.get_connection()

        # Kiểm tra xem kết nối có thành công hay không
        if connection:
            connection.close()
            return True

        return False

# Tạo một đối tượng Database để sử dụng trong ứng dụng
db = Database()

# Kiểm tra kết nối cơ sở dữ liệu khi chạy trực tiếp file này
if __name__ == "__main__":
    if db.test_connection():
        print("Database connection successful!")
    else:
        print("Database connection failed!")
