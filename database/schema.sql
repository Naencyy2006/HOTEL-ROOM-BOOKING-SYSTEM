CREATE DATABASE IF NOT EXISTS hotel_room_booking
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE hotel_room_booking;

-- Drop tables in dependency order so the script can be re-run
-- Xóa các bảng theo thứ tự phụ thuộc để có thể chạy lại script
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_types;
DROP TABLE IF EXISTS users;


-- 1. USERS

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    gender VARCHAR(20),
    year_of_birth INT,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Member', 'Receptionist', 'Admin') NOT NULL DEFAULT 'Member',
    status VARCHAR(30) NOT NULL DEFAULT 'Active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);



-- 2. ROOM_TYPES---

CREATE TABLE room_types (
    room_type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    capacity INT NOT NULL,
    description TEXT,
    price_per_night DECIMAL(12,2) NOT NULL
);


-- 3. ROOMS

CREATE TABLE rooms (
    room_number VARCHAR(20) PRIMARY KEY,
    room_type_id INT NOT NULL,
    floor INT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Available',

    CONSTRAINT fk_rooms_room_type
        FOREIGN KEY (room_type_id)
        REFERENCES room_types(room_type_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- 4. BOOKINGS

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id VARCHAR(20),
    room_type_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    refund_price DECIMAL(12,2) DEFAULT 0.00,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    canceled_at DATETIME,

    CONSTRAINT fk_bookings_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_bookings_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(room_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_bookings_room_type
        FOREIGN KEY (room_type_id)
        REFERENCES room_types(room_type_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_booking_dates
        CHECK (check_out > check_in),

    CONSTRAINT chk_booking_prices
        CHECK (total_price >= 0 AND refund_price >= 0)
);


-- 5. PAYMENTS

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL,
    transaction_code VARCHAR(100),
    status VARCHAR(30) NOT NULL DEFAULT 'Paid',

    CONSTRAINT fk_payments_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0)
);


-- 6. REVIEWS

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id VARCHAR(20),
    booking_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'Published',
    review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_reviews_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(room_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_reviews_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_review_rating
        CHECK (rating BETWEEN 1 AND 5)
);



-- INDEXES

CREATE INDEX idx_rooms_room_type
    ON rooms(room_type_id);

CREATE INDEX idx_rooms_status
    ON rooms(status);

CREATE INDEX idx_bookings_user
    ON bookings(user_id);

CREATE INDEX idx_bookings_room
    ON bookings(room_id);

CREATE INDEX idx_bookings_room_type
    ON bookings(room_type_id);

CREATE INDEX idx_bookings_dates
    ON bookings(check_in, check_out);

CREATE INDEX idx_bookings_status
    ON bookings(status);

CREATE INDEX idx_payments_booking
    ON payments(booking_id);

CREATE INDEX idx_reviews_user
    ON reviews(user_id);

CREATE INDEX idx_reviews_room
    ON reviews(room_id);

CREATE INDEX idx_reviews_booking
    ON reviews(booking_id);
