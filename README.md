# HOTEL ROOM BOOKING SYSTEM
hotel_booking_app/
│── assets/                  # Hình ảnh, icon giao diện (PNG, ICO)
│── config.py                # Cấu hình hệ thống (Chuỗi kết nối CSDL, secret key)
│── database/                # Khởi tạo CSDL, session,
│── models/                  # Định nghĩa ORM bằng SQLAlchemy (User, Room, Booking,...)
│── controllers/             # Logic xử lý nghiệp vụ (Auth, Booking, Check-in, Reports)
│── views/                   # Giao diện GUI (CustomTkinter / PyQt)
│   ├── components/          # Component dùng chung (Custom Card, Dialog, Table)
│   ├── auth/                # Màn hình Đăng nhập, Đăng ký, Quên mật khẩu
│   ├── member/              # Màn hình Tìm phòng, Đặt phòng, Lịch sử, Review
│   ├── receptionist/        # Màn hình Check-in, Check-out, Khách vãng lai
│   └── admin/               # Màn hình CRUD Phòng, User, Báo cáo (Doanh thu/Công suất)
│── utils/                   # Hàm bổ trợ (Mã hóa mật khẩu, Validator, Export PDF/Excel)
│── tests/                   # Script kiểm thử tự động
│── docs/                    # Chứa các file tài liệu yêu cầu 
│── main.py                  # Entry point chính chạy ứng dụng Desktop
│── Dockerfile               # Cấu hình Docker
└── requirements.txt         # Thư viện phụ thuộc (customtkinter/pyqt6, sqlalchemy,...)
