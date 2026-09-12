# services/receptionist_service.py
# Business logic module for receptionist operations
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.database import db
from datetime import datetime, date
from services import room_service

class ReceptionistService:
    def __init__(self):
        self.db = db

    def view_reservations(self, filter_status=None, check_in_date=None, guest_name=None):
        """
        Xem danh sách tất cả booking slips, hỗ trợ lọc theo trạng thái, ngày check-in hoặc tên khách hàng.
        """
        connection = self.db.get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT b.booking_id, b.user_id, u.full_name, u.phone, u.email,
                   b.room_id, b.room_type_id, rt.type_name, 
                   b.check_in, b.check_out, b.total_price, b.status, b.created_at
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN room_types rt ON b.room_type_id = rt.room_type_id
            WHERE 1=1
        """
        params = []

        if filter_status:
            query += " AND b.status = %s"
            params.append(filter_status)

        if check_in_date:
            query += " AND b.check_in = %s"
            params.append(check_in_date)

        if guest_name:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{guest_name}%")

        query += " ORDER BY b.check_in DESC"

        try:
            cursor.execute(query, tuple(params))
            reservations = cursor.fetchall()
            return reservations
        except Exception as e:
            print(f"Error fetching reservations: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def create_walkin_booking(self, full_name, email, phone, gender, year_of_birth, 
                              room_type_id, room_id, check_in, check_out, 
                              total_price=None, payment_method="Cash"):
        """
        Tạo tài khoản nhanh cho khách walk-in, kiểm tra trùng phòng, tạo lịch đặt phòng và thanh toán.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        # Chuyển đổi định dạng ngày nếu là chuỗi
        d_in = datetime.strptime(check_in, "%Y-%m-%d").date() if isinstance(check_in, str) else check_in
        d_out = datetime.strptime(check_out, "%Y-%m-%d").date() if isinstance(check_out, str) else check_out

        if d_out <= d_in:
            return False, "Check-out date must be after check-in date."

        # 1. Kiểm tra xem loại phòng còn trống trong khoảng ngày này không
        if not room_service.is_room_type_available(connection, room_type_id, d_in, d_out):
            connection.close()
            return False, "No available rooms left for the selected room type and dates."

        cursor = connection.cursor(dictionary=True)
        try:
            # 2. Kiểm tra hoặc tạo tài khoản Member mới cho khách
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                user_id = existing_user["user_id"]
            else:
                insert_user_query = """
                    INSERT INTO users (full_name, email, phone, gender, year_of_birth, password_hash, role, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Member', 'Active')
                """
                default_password_hash = "walkin_default_hash"
                cursor.execute(insert_user_query, (full_name, email, phone, gender, year_of_birth, default_password_hash))
                user_id = cursor.lastrowid

            # 3. Tính tổng tiền nếu không truyền vào
            if total_price is None or total_price <= 0:
                rt_info = room_service.get_room_type_info(connection, room_type_id)
                if not rt_info:
                    return False, f"Room type ID {room_type_id} does not exist."
                
                nights = (d_out - d_in).days
                total_price = nights * float(rt_info["price_per_night"])

            # 4. Kiểm tra phòng vật lý cụ thể (nếu được chọn)
            if room_id:
                cursor.execute("SELECT room_type_id, status FROM rooms WHERE room_number = %s", (room_id,))
                room = cursor.fetchone()
                if not room:
                    return False, f"Room number {room_id} does not exist."
                if room["room_type_id"] != room_type_id:
                    return False, f"Room {room_id} does not match selected room type ID {room_type_id}."
                if room["status"] == "Maintenance":
                    return False, f"Room {room_id} is currently under maintenance."

                # Kiểm tra va chạm lịch đặt phòng khác (Overlap Check)
                overlap_query = """
                    SELECT booking_id FROM bookings
                    WHERE room_id = %s 
                      AND status IN ('Confirmed', 'Checked-in')
                      AND check_in < %s AND check_out > %s
                """
                cursor.execute(overlap_query, (room_id, d_out, d_in))
                if cursor.fetchone():
                    return False, f"Room {room_id} is already booked for the selected dates."

            # 5. Thêm bản ghi booking mới (Trạng thái Confirmed)
            insert_booking_query = """
                INSERT INTO bookings (user_id, room_id, room_type_id, check_in, check_out, total_price, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Confirmed')
            """
            cursor.execute(insert_booking_query, (user_id, room_id, room_type_id, d_in, d_out, total_price))
            booking_id = cursor.lastrowid

            # 6. Ghi nhận giao dịch thanh toán
            insert_payment_query = """
                INSERT INTO payments (booking_id, amount, payment_method, transaction_code, status)
                VALUES (%s, %s, %s, %s, 'Paid')
            """
            transaction_code = f"WALKIN-{booking_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
            cursor.execute(insert_payment_query, (booking_id, total_price, payment_method, transaction_code))

            # 7. Cập nhật trạng thái phòng thành Occupied nếu nhận phòng ngay hôm nay
            today = date.today()
            if room_id and d_in == today:
                room_service.update_room_status(connection, room_id, "Occupied")

            connection.commit()
            return True, f"Walk-in booking created successfully! Booking ID: {booking_id}"

        except Exception as e:
            connection.rollback()
            return False, f"Error creating walk-in booking: {e}"
        finally:
            cursor.close()
            connection.close()

    def process_check_in(self, booking_id, room_number=None):
        """
        Xử lý thủ tục Check-in: Gán số phòng vật lý, chuyển trạng thái Booking thành 'Checked-in'
        và chuyển trạng thái Phòng thành 'Occupied'.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                return False, "Booking record not found."
            
            if booking["status"] == "Checked-in":
                return False, f"Booking #{booking_id} is already checked-in."
            elif booking["status"] != "Confirmed":
                return False, f"Cannot check-in booking #{booking_id} with status '{booking['status']}'."

            target_room = room_number if room_number else booking.get("room_id")
            if not target_room:
                return False, "No physical room specified. Please assign a room number for check-in."

            cursor.execute("SELECT * FROM rooms WHERE room_number = %s", (target_room,))
            room = cursor.fetchone()
            if not room:
                return False, f"Room number {target_room} does not exist."
            
            if room["room_type_id"] != booking["room_type_id"]:
                return False, f"Room {target_room} does not match booking room type ID {booking['room_type_id']}."
                
            if room["status"] != "Available":
                return False, f"Room {target_room} is currently '{room['status']}' and cannot be occupied."

            # Cập nhật booking: Gán room_id và đổi status -> Checked-in
            update_booking_query = """
                UPDATE bookings 
                SET room_id = %s, status = 'Checked-in' 
                WHERE booking_id = %s
            """
            cursor.execute(update_booking_query, (target_room, booking_id))

            # Cập nhật phòng vật lý -> Occupied thông qua room_service
            room_service.update_room_status(connection, target_room, "Occupied")

            connection.commit()
            return True, f"Check-in successful for Booking #{booking_id} in Room {target_room}."

        except Exception as e:
            connection.rollback()
            return False, f"Error during check-in process: {e}"
        finally:
            cursor.close()
            connection.close()

    def process_check_out(self, booking_id):
        """
        Xử lý thủ tục Check-out: Chuyển trạng thái Booking thành 'Completed'
        và trả trạng thái Phòng vật lý về 'Available'.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                return False, "Booking record not found."

            if booking["status"] == "Completed":
                return False, f"Booking #{booking_id} has already been checked-out."
            elif booking["status"] != "Checked-in":
                return False, f"Cannot check-out booking #{booking_id} with status '{booking['status']}'. Guest must be checked-in first."

            room_number = booking.get("room_id")

            # Cập nhật status booking -> Completed
            update_booking_query = "UPDATE bookings SET status = 'Completed' WHERE booking_id = %s"
            cursor.execute(update_booking_query, (booking_id,))

            # Trả phòng về trạng thái -> Available thông qua room_service
            if room_number:
                room_service.release_room(connection, room_number)

            connection.commit()
            return True, f"Check-out successful for Booking #{booking_id}. Room {room_number} is now Available."

        except Exception as e:
            connection.rollback()
            return False, f"Error during check-out process: {e}"
        finally:
            cursor.close()
            connection.close()
