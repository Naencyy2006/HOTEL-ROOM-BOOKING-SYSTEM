HotelRoomBookingSystem/
│
├── main.py                         # File chạy chính của hệ thống (Entry point)
├── README.md                       # Mô tả dự án và hướng dẫn cài đặt/chạy
├── requirements.txt                # Danh sách thư viện Python phụ thuộc
├── .gitignore                      # Các file và thư mục bỏ qua, không đưa lên GitHub
│
├── config/                         # Thư mục cấu hình hệ thống
│   └── database.py                 # Cấu hình và kết nối Python với Database
│
├── database/                       # Thư mục chứa các kịch bản SQL
│   ├── schema.sql                  # Tạo Database, định nghĩa các bảng và ràng buộc (PK/FK)
│   └── seed.sql                    # Khởi tạo dữ liệu mẫu ban đầu cho hệ thống
│
├── docs/                           # Tài liệu phân tích và thiết kế hệ thống
│   ├── RequirementAndDesignDocument_Group.docx # Tài liệu yêu cầu & thiết kế (File Word)
│   └── RequirementAndDesignDocument_Group.pdf  # Tài liệu yêu cầu & thiết kế (File PDF)
│
├── models/                         # Tầng Dữ liệu (Data Layer) - Các class đại diện cho bảng
│   ├── __init__.py                 # Khởi tạo package models
│   ├── user.py                     # Model đại diện cho bảng Users (Người dùng)
│   ├── room_type.py                # Model đại diện cho bảng RoomTypes (Loại phòng)
│   ├── room.py                     # Model đại diện cho bảng Rooms (Phòng)
│   ├── booking.py                  # Model đại diện cho bảng Bookings (Đơn đặt phòng)
│   ├── payment.py                  # Model đại diện cho bảng Payments (Thanh toán)
│   └── review.py                   # Model đại diện cho bảng Reviews (Đánh giá)
│
├── services/                       # Tầng Nghiệp vụ (Business Logic Layer)
│   ├── admin_service.py            # Quản lý Rooms, Users, Bookings và xuất báo cáo
│   ├── auth_service.py             # Xử lý Đăng ký, Đăng nhập, Đăng xuất, Đổi mật khẩu
│   ├── booking_service.py          # Xử lý luồng đặt phòng và quản lý lịch sử đặt phòng
│   ├── cancellation_service.py    # Xử lý hủy phòng và tính toán số tiền hoàn trả
│   ├── payment_service.py          # Xử lý giao dịch thanh toán và xuất hóa đơn
│   ├── receptionist_service.py     # Nghiệp vụ lễ tân: Đặt trực tiếp, Check-in, Check-out
│   ├── review_service.py           # Quản lý, gửi và hiển thị đánh giá từ khách hàng
│   ├── room_service.py             # Tìm kiếm, lọc và kiểm tra phòng khả dụng
│   └── user_service.py             # Cập nhật và quản lý thông tin tài khoản người dùng
│
├── utils/                          # Thư mục chứa các hàm tiện ích dùng chung
│   ├── password.py                 # Mã hóa (Hash) và kiểm tra tính hợp lệ của mật khẩu
│   └── validators.py               # Kiểm tra định dạng dữ liệu đầu vào (Email, SĐT, Ngày...)
│
└── views/                          # Tầng Giao diện / Điều hướng người dùng (UI Layer)
    ├── admin.py                    # Menu và giao diện chức năng dành cho Administrator
    ├── guest.py                    # Menu và chức năng dành cho Khách vãng lai (Chưa đăng nhập)
    ├── login.py                    # Giao diện màn hình đăng nhập và đăng ký tài khoản
    ├── member.py                   # Menu và giao diện dành cho Khách hàng thành viên
    └── receptionist.py             # Menu và giao diện chức năng dành cho Lễ tân