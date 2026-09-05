HotelRoomBookingSystem/
│
├── main.py                         # File chính, khởi động toàn bộ hệ thống
│
├── config/
│   └── database.py                 # Cấu hình và tạo kết nối đến Database
│
├── database/
│   └── schema.sql                  # Tạo Database, các bảng, khóa và ràng buộc
│
├── models/
│   ├── user.py                     # Model User: thông tin tài khoản và phân quyền
│   ├── room.py                     # Model Room: thông tin phòng vật lý
│   ├── booking.py                  # Model Booking: thông tin đặt phòng
│   ├── payment.py                  # Model Payment: thông tin thanh toán
│   └── review.py                   # Model Review: đánh giá và nhận xét của khách
│
├── services/
│   ├── auth_service.py             # Xử lý nghiệp vụ đăng ký, đăng nhập, đổi/reset mật khẩu
│   ├── room_service.py             # Xử lý nghiệp vụ tìm kiếm và quản lý phòng
│   ├── booking_service.py          # Xử lý nghiệp vụ đặt phòng và lịch sử đặt phòng
│   ├── payment_service.py          # Xử lý thanh toán và cập nhật trạng thái thanh toán
│   ├── cancellation_service.py     # Xử lý hủy phòng, phí hủy và tiền hoàn lại
│   ├── receptionist_service.py     # Xử lý nghiệp vụ của lễ tân
│   │                               # (walk-in, check-in, check-out, quản lý reservation)
│   └── admin_service.py            # Xử lý nghiệp vụ quản trị hệ thống
│                                   # (quản lý user, room, booking, review, report)
│
├── views/
│   ├── login.py                    # Giao diện đăng nhập, đăng ký và reset mật khẩu
│   ├── member.py                   # Giao diện dành cho Member/khách hàng
│   ├── receptionist.py             # Giao diện dành cho Receptionist/lễ tân
│   └── admin.py                    # Giao diện dành cho Administrator
│
└── utils/
    ├── validators.py               # Các hàm kiểm tra dữ liệu đầu vào
    │                               # (email, password, ngày tháng, số điện thoại...)
    └── password.py                 # Mã hóa/hash và kiểm tra mật khấu