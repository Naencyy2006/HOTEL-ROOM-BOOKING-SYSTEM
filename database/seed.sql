-- 1. USERS 
INSERT INTO users (user_id, full_name, email, phone, gender, year_of_birth, password_hash, role, status) VALUES
(1, 'HighHotel Administrator', 'admin@hotel.com', '0901234567', 'Male', 1990, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Admin', 'Active'),
(2, 'Le Thi Receptionist', 'receptionist1@hotel.com', '0912345678', 'Female', 1995, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Receptionist', 'Active'),
(3, 'Nguyen Van Receptionist', 'receptionist2@hotel.com', '0912345679', 'Male', 1996, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Receptionist', 'Active'),
(4, 'Nguyen Van An', 'an.nguyen@gmail.com', '0945112233', 'Male', 1994, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(5, 'Hoang Van Tung', 'tung.hoang@gmail.com', '0966778899', 'Male', 1990, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(6, 'Ly Minh Triet', 'triet.ly@outlook.com', '0938223344', 'Male', 1985, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(7, 'Ngo Thanh Van', 'van.ngo@yahoo.com', '0918990011', 'Female', 1998, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(8, 'Bui Anh Tuan', 'tuan.bui@gmail.com', '0971239876', 'Male', 2001, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(9, 'Pham Tran Bao Ngoc', 'ngoc.pham@gmail.com', '0912998877', 'Female', 1997, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(10, 'Dang Quoc Huy', 'huy.dang@yahoo.com', '0933112244', 'Male', 1991, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(11, 'Vu Minh Thu', 'thu.vu@gmail.com', '0978665544', 'Female', 1999, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active'),
(12, 'Ho Van Nam', 'nam.ho@gmail.com', '0905554433', 'Male', 1989, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Member', 'Active')
ON DUPLICATE KEY UPDATE
	full_name=VALUES(full_name),
	email=VALUES(email),
	gender=VALUES(gender);

-- 2. ROOM TYPES
INSERT INTO room_types (room_type_id, type_name, capacity, description, price_per_night) VALUES
(1, 'Standard Single', 1, 'Cozy standard single room with essential amenities.', 500000.00),
(2, 'Standard Double', 2, 'Standard double room suitable for two guests or couples.', 800000.00),
(3, 'Deluxe Suite', 2, 'Premium suite with city views and modern amenities.', 1500000.00),
(4, 'Executive VIP', 4, 'Spacious family VIP room with a living room and two bedrooms.', 3000000.00)
ON DUPLICATE KEY UPDATE
	type_name=VALUES(type_name),
	capacity=VALUES(capacity),
	description=VALUES(description),
	price_per_night=VALUES(price_per_night);

-- 3. ROOMS 
INSERT INTO rooms (room_number, room_type_id, floor, status) VALUES
('101', 1, 1, 'Available'),
('102', 1, 1, 'Available'),
('103', 1, 1, 'Available'),
('104', 1, 1, 'Maintenance'),
('105', 1, 1, 'Available'),
('201', 2, 2, 'Available'),
('202', 2, 2, 'Available'),
('203', 2, 2, 'Occupied'),
('204', 2, 2, 'Available'),
('205', 2, 2, 'Occupied'),
('301', 3, 3, 'Available'),
('302', 3, 3, 'Occupied'),
('303', 3, 3, 'Occupied'),
('304', 3, 3, 'Maintenance'),
('305', 3, 3, 'Available'),
('401', 4, 4, 'Available'),
('402', 4, 4, 'Occupied'),
('403', 4, 4, 'Available'),
('404', 4, 4, 'Available')
ON DUPLICATE KEY UPDATE floor=VALUES(floor), status=VALUES(status);


-- 4. BOOKINGS 
INSERT INTO bookings (booking_id, user_id, room_id, room_type_id, check_in, check_out, total_price, refund_price, status, created_at) VALUES
(2001, 4, '203', 2, '2026-10-01', '2026-10-03', 1600000.00, 0.00, 'Checked-in', '2026-09-25 09:15:00'),
(2002, 5, '303', 3, '2026-10-05', '2026-10-08', 4500000.00, 0.00, 'Checked-in', '2026-09-26 14:00:00'),
(2003, 6, NULL,  1, '2026-10-10', '2026-10-12', 1000000.00, 0.00, 'Confirmed', '2026-09-28 10:30:00'),
(2004, 7, '403', 4, '2026-09-15', '2026-09-18', 9000000.00, 0.00, 'Completed', '2026-09-01 11:20:00'),
(2005, 8, NULL,  2, '2026-10-20', '2026-10-22', 1600000.00, 0.00, 'Pending Payment', '2026-10-01 16:45:00'),
(2006, 4, '103', 1, '2026-10-25', '2026-10-27', 1000000.00, 0.00, 'Confirmed', '2026-10-02 08:00:00'),
(2007, 5, NULL,  1, '2026-09-01', '2026-09-02', 500000.00, 500000.00, 'Cancelled', '2026-08-20 15:30:00'),
(2008, 9, '302', 3, '2026-09-11', '2026-09-14', 4500000.00, 0.00, 'Checked-in', '2026-09-05 10:00:00'),
(2009, 10, '402', 4, '2026-09-10', '2026-09-13', 9000000.00, 0.00, 'Checked-in', '2026-09-02 15:30:00'),
(2010, 11, '201', 2, '2026-08-20', '2026-08-23', 2400000.00, 0.00, 'Completed', '2026-08-10 11:00:00'),
(2011, 12, '101', 1, '2026-09-01', '2026-09-04', 1500000.00, 0.00, 'Completed', '2026-08-25 09:00:00'),
(2012, 9, NULL,  2, '2026-09-25', '2026-09-28', 2400000.00, 0.00, 'Confirmed', '2026-09-10 14:20:00'),
(2013, 10, NULL,  3, '2026-10-15', '2026-10-18', 4500000.00, 0.00, 'Pending Payment', '2026-09-12 09:00:00'),
(2014, 11, NULL,  4, '2026-09-05', '2026-09-07', 6000000.00, 6000000.00, 'Cancelled', '2026-08-28 16:00:00')
ON DUPLICATE KEY UPDATE status=VALUES(status), total_price=VALUES(total_price);

-- 5. PAYMENTS 
INSERT INTO payments (payment_id, booking_id, amount, payment_date, payment_method, transaction_code, status) VALUES
(101, 2001, 1600000.00, '2026-09-25 09:20:00', 'Bank Transfer', 'TXN200001', 'Paid'),
(102, 2002, 4500000.00, '2026-09-26 14:05:00', 'Credit Card', 'TXN200002', 'Paid'),
(103, 2004, 9000000.00, '2026-09-01 11:25:00', 'Cash', 'TXN200003', 'Paid'),
(104, 2007, 500000.00,  '2026-08-20 15:35:00', 'Bank Transfer', 'TXN200004', 'Refunded'),
(105, 2008, 4500000.00, '2026-09-05 10:10:00', 'MoMo', 'TXN200005', 'Paid'),
(106, 2009, 9000000.00, '2026-09-02 15:35:00', 'Credit Card', 'TXN200006', 'Paid'),
(107, 2010, 2400000.00, '2026-08-10 11:05:00', 'Bank Transfer', 'TXN200007', 'Paid'),
(108, 2011, 1500000.00, '2026-08-25 09:15:00', 'Cash', 'TXN200008', 'Paid'),
(109, 2012, 2400000.00, '2026-09-10 14:25:00', 'Bank Transfer', 'TXN200009', 'Paid'),
(110, 2014, 6000000.00, '2026-08-28 16:10:00', 'Credit Card', 'TXN200010', 'Refunded')
ON DUPLICATE KEY UPDATE amount=VALUES(amount), status=VALUES(status);

-- 6. REVIEWS 
INSERT INTO reviews (review_id, user_id, room_id, booking_id, rating, comment, status, review_date) VALUES
(1, 7, '403', 2004, 5, 'The Executive VIP room was spacious with a beautiful view and excellent service!', 'Published', '2026-09-18 10:00:00'),
(2, 11, '201', 2010, 4, 'The room was clean, reasonably priced, and the receptionist was very attentive.', 'Published', '2026-08-23 14:00:00'),
(3, 12, '101', 2011, 5, 'The hotel was quiet, the bed was comfortable, and the location was convenient.', 'Published', '2026-09-04 11:30:00')
ON DUPLICATE KEY UPDATE rating=VALUES(rating), comment=VALUES(comment);