# services/receptionist_service.py
# Business logic module for receptionist operations (view reservations, walk-in booking, check-in, check-out)

from database import db
from datetime import datetime

class ReceptionistService:
    def __init__(self):
        # Use the database connection configured in the db module
        self.db = db

    def view_reservations(self, filter_status=None, check_in_date=None, guest_name=None):
        """
        Retrieve a list of all booking records filtered by status, check-in date, or guest name.
        """
        connection = self.db.get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        # Query booking details along with guest name, room type name, and assigned room number
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

        # Filter by booking status if provided
        if filter_status:
            query += " AND b.status = %s"
            params.append(filter_status)

        # Filter by check-in date if provided
        if check_in_date:
            query += " AND b.check_in = %s"
            params.append(check_in_date)

        # Search by guest full name if provided
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

    def create_walkin_booking(self, full_name, email, phone, gender, year_of_birth, room_type_id, room_id, check_in, check_out, total_price, payment_method):
        """
        Create a quick member account for walk-in guests, generate a booking record, and record the payment.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        try:
            # Check if the guest email already exists in the system
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                user_id = existing_user["user_id"]
            else:
                # Insert a new member account with a default hashed password for walk-in guests
                insert_user_query = """
                    INSERT INTO users (full_name, email, phone, gender, year_of_birth, password_hash, role, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Member', 'Active')
                """
                default_password_hash = "walkin_default_hash"
                cursor.execute(insert_user_query, (full_name, email, phone, gender, year_of_birth, default_password_hash))
                user_id = cursor.lastrowid

            # Verify physical room availability if a room is assigned upfront
            if room_id:
                cursor.execute("SELECT room_type_id, status FROM rooms WHERE room_number = %s", (room_id,))
                room = cursor.fetchone()
                if not room:
                    return False, f"Room number {room_id} does not exist."
                if room["room_type_id"] != room_type_id:
                    return False, f"Room {room_id} does not match selected room type ID {room_type_id}."
                if room["status"] != "Available":
                    return False, f"Room {room_id} is currently not available."

            # Insert the new booking record
            insert_booking_query = """
                INSERT INTO bookings (user_id, room_id, room_type_id, check_in, check_out, total_price, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Confirmed')
            """
            cursor.execute(insert_booking_query, (user_id, room_id, room_type_id, check_in, check_out, total_price))
            booking_id = cursor.lastrowid

            # Record the payment transaction
            insert_payment_query = """
                INSERT INTO payments (booking_id, amount, payment_method, transaction_code, status)
                VALUES (%s, %s, %s, %s, 'Paid')
            """
            transaction_code = f"WALKIN-{booking_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
            cursor.execute(insert_payment_query, (booking_id, total_price, payment_method, transaction_code))

            # Update physical room status to Occupied if a room was assigned
            if room_id:
                cursor.execute("UPDATE rooms SET status = 'Occupied' WHERE room_number = %s", (room_id,))

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
        Handle guest check-in procedure: Validate booking status, assign/verify physical room,
        and update room status to Occupied.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        try:
            # 1. Verify the booking record exists and has valid status
            cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                return False, "Booking record not found."
            
            if booking["status"] == "Checked-in":
                return False, f"Booking #{booking_id} is already checked-in."
            elif booking["status"] != "Confirmed":
                return False, f"Cannot check-in booking #{booking_id} with status '{booking['status']}'."

            # 2. Determine room number to check-in
            target_room = room_number if room_number else booking.get("room_id")
            if not target_room:
                return False, "No physical room specified. Please assign a room number for check-in."

            # 3. Verify the physical room details
            cursor.execute("SELECT * FROM rooms WHERE room_number = %s", (target_room,))
            room = cursor.fetchone()
            if not room:
                return False, f"Room number {target_room} does not exist."
            
            if room["room_type_id"] != booking["room_type_id"]:
                return False, f"Room {target_room} does not match booking room type ID {booking['room_type_id']}."
                
            if room["status"] != "Available":
                return False, f"Room {target_room} is currently '{room['status']}' and cannot be occupied."

            # 4. Update booking record: assign room_id and set status to Checked-in
            update_booking_query = """
                UPDATE bookings 
                SET room_id = %s, status = 'Checked-in' 
                WHERE booking_id = %s
            """
            cursor.execute(update_booking_query, (target_room, booking_id))

            # 5. Update physical room status to Occupied
            update_room_query = "UPDATE rooms SET status = 'Occupied' WHERE room_number = %s"
            cursor.execute(update_room_query, (target_room,))

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
        Handle guest check-out procedure: Validate status, set booking status to Completed,
        and release room status back to Available.
        """
        connection = self.db.get_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        try:
            # 1. Retrieve booking information
            cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                return False, "Booking record not found."

            if booking["status"] == "Completed":
                return False, f"Booking #{booking_id} has already been checked-out."
            elif booking["status"] != "Checked-in":
                return False, f"Cannot check-out booking #{booking_id} with status '{booking['status']}'. Guest must be checked-in first."

            room_number = booking.get("room_id")

            # 2. Update booking status to Completed
            update_booking_query = "UPDATE bookings SET status = 'Completed' WHERE booking_id = %s"
            cursor.execute(update_booking_query, (booking_id,))

            # 3. Reset physical room status back to Available
            if room_number:
                update_room_query = "UPDATE rooms SET status = 'Available' WHERE room_number = %s"
                cursor.execute(update_room_query, (room_number,))

            connection.commit()
            return True, f"Check-out successful for Booking #{booking_id}. Room {room_number} is now Available."

        except Exception as e:
            connection.rollback()
            return False, f"Error during check-out process: {e}"
        finally:
            cursor.close()
            connection.close()