USE hotel_room_booking;

-- 1. TẠO DỮ LIỆU BẢNG USERS
-- Mật khẩu mặc định cho tất cả tài khoản: 123456 
-- (Đã mã hóa SHA-256: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92)
INSERT INTO users (user_id, full_name, email, phone, gender, year_of_birth, password_hash, role, status) VALUES
(1, 'Quản Trị Viên HighHotel', 'admin@hotel.com', '0901234567', 'Nam', 1990, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Admin', 'Active'),
(2, 'Lê Thị Lễ Tân', 'receptionist1@hotel.com', '0912345678', 'Nữ', 1995, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Receptionist', 'Active'),
(3, 'Nguyễn Văn Lễ Tân', 'receptionist2@hotel.com', '0912345679', 'Nam', 1996, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Receptionist', 'Active'),
(4, 'Nguyễn Văn Khách', 'khach1@gmail.com', '0987654321', 'Nam', 1998, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(5, 'Trần Thị Mai', 'khach2@gmail.com', '0987654322', 'Nữ', 2000, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(6, 'Phạm Hoàng Anh', 'khach3@gmail.com', '0987654323', 'Nam', 1992, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active');

-- 2. TẠO DỮ LIỆU BẢNG ROOM_TYPES
INSERT INTO room_types (room_type_id, type_name, capacity, description, price_per_night) VALUES
(1, 'Standard Single', 1, 'Phòng đơn tiêu chuẩn, ấm cúng, đầy đủ tiện nghi cơ bản.', 500000.00),
(2, 'Standard Double', 2, 'Phòng đôi tiêu chuẩn thích hợp cho 2 người hoặc cặp đôi.', 800000.00),
(3, 'Deluxe Suite', 2, 'Phòng Suite cao cấp, view thành phố, trang thiết bị hiện đại.', 1500000.00),
(4, 'Executive VIP', 4, 'Phòng VIP gia đình rộng rãi, bao gồm phòng khách và 2 phòng ngủ.', 3000000.00);

-- 3. TẠO DỮ LIỆU BẢNG ROOMS
INSERT INTO rooms (room_number, room_type_id, floor, status) VALUES
('101', 1, 1, 'Available'),
('102', 1, 1, 'Available'),
('103', 2, 1, 'Occupied'),
('104', 2, 1, 'Available'),
('201', 2, 2, 'Available'),
('202', 3, 2, 'Occupied'),
('203', 3, 2, 'Available'),
('301', 4, 3, 'Available'),
('302', 4, 3, 'Maintenance');


-- 4. TẠO DỮ LIỆU BẢNG BOOKINGS
INSERT INTO bookings (booking_id, user_id, room_id, room_type_id, check_in, check_out, total_price, refund_price, status, created_at) VALUES
-- Đơn đã hoàn thành (quá khứ)
(1, 4, '103', 2, '2026-08-01', '2026-08-03', 1600000.00, 0.00, 'Completed', '2026-07-25 10:00:00'),
(2, 5, '202', 3, '2026-08-10', '2026-08-12', 3000000.00, 0.00, 'Completed', '2026-08-01 14:30:00'),
-- Đơn đang ở (Checked-in)
(3, 6, '103', 2, '2026-09-10', '2026-09-14', 3200000.00, 0.00, 'Checked-in', '2026-09-08 09:15:00'),
-- Đơn đã xác nhận (Sắp tới - Confirmed)
(4, 4, NULL, 3, '2026-10-01', '2026-10-03', 3000000.00, 0.00, 'Confirmed', '2026-09-11 16:20:00'),
-- Đơn bị hủy (Canceled)
(5, 5, NULL, 1, '2026-09-01', '2026-09-02', 500000.00, 500000.00, 'Cancelled', '2026-08-20 11:00:00');


-- 5. TẠO DỮ LIỆU BẢNG PAYMENTS
INSERT INTO payments (payment_id, booking_id, amount, payment_date, payment_method, transaction_code, status) VALUES
(1, 1, 1600000.00, '2026-07-25 10:05:00', 'Bank Transfer', 'TXN100001', 'Paid'),
(2, 2, 3000000.00, '2026-08-01 14:35:00', 'Credit Card', 'TXN100002', 'Paid'),
(3, 3, 3200000.00, '2026-09-08 09:20:00', 'MoMo', 'TXN100003', 'Paid'),
(4, 4, 3000000.00, '2026-09-11 16:25:00', 'Credit Card', 'TXN100004', 'Paid'),
(5, 5, 500000.00, '2026-08-20 11:05:00', 'Bank Transfer', 'TXN100005', 'Refunded');

-- 6. TẠO DỮ LIỆU BẢNG REVIEWS
INSERT INTO reviews (review_id, user_id, room_id, booking_id, rating, comment, status, review_date) VALUES
(1, 4, '103', 1, 5, 'Phòng rất sạch sẽ, dịch vụ hỗ trợ chu đáo. Rất hài lòng!', 'Published', '2026-08-03 11:00:00'),
(2, 5, '202', 2, 4, 'Phòng Suite rất đẹp, view xịn nhưng wifi ở tầng 2 hơi yếu một chút.', 'Published', '2026-08-12 10:30:00');