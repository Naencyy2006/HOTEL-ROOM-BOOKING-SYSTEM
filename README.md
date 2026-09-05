HotelRoomBookingSystem/
│
├── main.py                         # File chạy chính của hệ thống
├── README.md                       # Mô tả project + hướng dẫn cài đặt/chạy
├── requirements.txt                # Danh sách thư viện Python cần dùng
├── .gitignore                      # Các file không đưa lên GitHub
│
├── config/
│   └── database.py                 # Cấu hình và kết nối Python với Database
│
├── database/
│   └── schema.sql                  # Tạo Database + 6 bảng + PK/FK/Constraints
│
├── models/                         # Đại diện cho các đối tượng dữ liệu
│   ├── user.py                     # Model của bảng Users
│   ├── room_type.py                # Model của bảng RoomTypes
│   ├── room.py                     # Model của bảng Rooms
│   ├── booking.py                  # Model của bảng Bookings
│   ├── payment.py                  # Model của bảng Payments
│   └── review.py                   # Model của bảng Reviews
│
├── services/                       # Xử lý nghiệp vụ của hệ thống
│   ├── auth_service.py             # Register, Login, Logout, Reset Password
│   ├── room_service.py             # Tìm kiếm + kiểm tra phòng
│   ├── booking_service.py          # Đặt phòng + lịch sử booking
│   ├── payment_service.py          # Xử lý thanh toán + receipt
│   ├── cancellation_service.py     # Hủy phòng + tính tiền hoàn
│   ├── receptionist_service.py     # Walk-in, Check-in, Check-out
│   └── admin_service.py            # Quản lý Rooms, Users, Bookings, Reports
│
├── views/                          # Giao diện/menu người dùng
│   ├── login.py                    # Giao diện đăng nhập/đăng ký
│   ├── member.py                   # Menu và giao diện Member
│   ├── receptionist.py             # Menu và giao diện Receptionist
│   └── admin.py                    # Menu và giao diện Administrator
│
├── utils/                          # Các chức năng dùng chung
│   ├── validators.py               # Kiểm tra dữ liệu nhập vào
│   └── password.py                 # Hash và kiểm tra password
│
└── assets/                         # Tài nguyên giao diện
    ├── images/                     # Hình ảnh ( nếu có)
    └── icons/                      # Icon (nếu có )