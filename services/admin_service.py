
from config.database import db


class AdminService:
    """
    All business logic for the Admin role.
    The view (views/admin.py) only calls these methods and does not execute SQL directly.
    """

    # ---------------------------------------------------------
    # INTERNAL METHOD: get a safe connection
    # ---------------------------------------------------------
    def _connect(self):
        """
        Get a connection from db.get_connection().
        Raise ConnectionError with a clear message if the connection fails,
        instead of allowing an AttributeError when conn is None.
        """
        conn = db.get_connection()
        if conn is None:
            raise ConnectionError("Unable to connect to the database.")
        return conn

    # ---------------------------------------------------------
    # 1. USER MANAGEMENT (USERS)
    # ---------------------------------------------------------
    def get_all_users(self, role=None):
        """
        Get all users.
        - role: filter by role ('Member', 'Receptionist', 'Admin'),
            None = get all users.
        May raise ConnectionError if the database is unavailable; the view handles it.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            if role:
                cursor.execute(
                    "SELECT user_id, full_name, email, phone, gender, year_of_birth, "
                    "role, status, created_at "
                    "FROM users WHERE role = %s ORDER BY user_id",
                    (role,)
                )
            else:
                cursor.execute(
                    "SELECT user_id, full_name, email, phone, gender, year_of_birth, "
                    "role, status, created_at "
                    "FROM users ORDER BY user_id"
                )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def search_users(self, keyword):
        """Find users by full name, email, or phone number using LIKE."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            like_kw = f"%{keyword}%"
            cursor.execute(
                "SELECT user_id, full_name, email, phone, role, status "
                "FROM users "
                "WHERE full_name LIKE %s OR email LIKE %s OR phone LIKE %s",
                (like_kw, like_kw, like_kw)
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_user_role(self, user_id, new_role):
        """
        Change a user's role, for example promoting a Member to Receptionist.
        new_role must be one of {'Member', 'Receptionist', 'Admin'} as defined in the schema.
        """
        valid_roles = ("Member", "Receptionist", "Admin")
        if new_role not in valid_roles:
            return False, "Invalid role."

        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET role = %s WHERE user_id = %s",
                (new_role, user_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "User not found."
            return True, "Role updated successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Update error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def lock_user(self, user_id):
        """Lock a user account by setting status to 'Locked'."""
        return self._set_user_status(user_id, "Locked")

    def unlock_user(self, user_id):
        """Unlock a user account by setting status to 'Active'."""
        return self._set_user_status(user_id, "Active")

    def _set_user_status(self, user_id, status):
        """Shared internal method for changing account status."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET status = %s WHERE user_id = %s",
                (status, user_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "User not found."
            return True, f"User status changed to '{status}'."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Status update error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_user(self, user_id):
        """
        Delete a user from the system.
        Bookings reference user_id with ON DELETE RESTRICT, so MySQL blocks deletion
        if any booking exists, not only active bookings. Check first to provide a
        clear message instead of exposing the raw MySQL foreign-key error.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings WHERE user_id = %s",
                (user_id,)
            )
            (total_bookings,) = cursor.fetchone()
            if total_bookings > 0:
                return False, "Cannot delete: the user has booking history in the system."

            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "User not found."
            return True, "User deleted successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Delete error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 2. ROOM TYPE MANAGEMENT (ROOM_TYPES)
    # ---------------------------------------------------------
    # Rooms depend on room_type_id, which contains the price and description,
    # so room types must be managed before individual rooms are added.
    def get_all_room_types(self):
        """Get all room types."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT room_type_id, type_name, capacity, description, price_per_night "
                "FROM room_types ORDER BY room_type_id"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_room_type(self, type_name, capacity, price_per_night, description=""):
        """Add a new room type, such as Standard, Deluxe, or Suite."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO room_types (type_name, capacity, description, price_per_night) "
                "VALUES (%s, %s, %s, %s)",
                (type_name, capacity, description, price_per_night)
            )
            conn.commit()
            return True, "Room type added successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error adding room type (the name may already exist): {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room_type(self, room_type_id, type_name=None, capacity=None,
                          price_per_night=None, description=None):
        """Update a room type, changing only fields whose values are not None."""
        fields, values = [], []
        if type_name is not None:
            fields.append("type_name = %s")
            values.append(type_name)
        if capacity is not None:
            fields.append("capacity = %s")
            values.append(capacity)
        if price_per_night is not None:
            fields.append("price_per_night = %s")
            values.append(price_per_night)
        if description is not None:
            fields.append("description = %s")
            values.append(description)

        if not fields:
                return False, "There is no data to update."

        values.append(room_type_id)
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE room_types SET {', '.join(fields)} WHERE room_type_id = %s",
                tuple(values)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Room type not found."
            return True, "Room type updated successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Room type update error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_room_type(self, room_type_id):
        """
        Delete a room type.
        rooms.room_type_id uses ON DELETE RESTRICT, so deletion is blocked while
        rooms of this type exist. Check first to provide a clear error.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM rooms WHERE room_type_id = %s",
                (room_type_id,)
            )
            (total_rooms,) = cursor.fetchone()
            if total_rooms > 0:
                return False, "Cannot delete: rooms of this type still exist."

            cursor.execute("DELETE FROM room_types WHERE room_type_id = %s", (room_type_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Room type not found."
            return True, "Room type deleted successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Room type deletion error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 3. ROOM MANAGEMENT (ROOMS)
    # ---------------------------------------------------------
    def get_all_rooms(self):
        """Get all rooms with their type names and prices by joining room_types."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT r.room_number, r.floor, r.status, "
                "rt.room_type_id, rt.type_name, rt.price_per_night "
                "FROM rooms r "
                "JOIN room_types rt ON r.room_type_id = rt.room_type_id "
                "ORDER BY r.room_number"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_room(self, room_number, room_type_id, floor):
        """Add a new room with the schema's default status of 'Available'."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rooms (room_number, room_type_id, floor, status) "
                "VALUES (%s, %s, %s, 'Available')",
                (room_number, room_type_id, floor)
            )
            conn.commit()
            return True, "Room added successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error adding room (the room number may already exist or the room type is invalid): {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room(self, room_number, room_type_id=None, floor=None, status=None):
        """
        Update room information.
        Change only fields whose values are not None.
        """
        fields, values = [], []
        if room_type_id is not None:
            fields.append("room_type_id = %s")
            values.append(room_type_id)
        if floor is not None:
            fields.append("floor = %s")
            values.append(floor)
        if status is not None:
            fields.append("status = %s")
            values.append(status)

        if not fields:
                return False, "There is no data to update."

        values.append(room_number)
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE rooms SET {', '.join(fields)} WHERE room_number = %s",
                tuple(values)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Room not found."
            return True, "Room updated successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Room update error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_room(self, room_number):
        """
        Delete a room.
        bookings.room_id uses ON DELETE RESTRICT, so deletion is blocked if the room
        appears in any booking, including completed bookings, to preserve history.
        Check first to provide a friendly error.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings WHERE room_id = %s",
                (room_number,)
            )
            (total_bookings,) = cursor.fetchone()
            if total_bookings > 0:
                return False, "Cannot delete: the room has booking history."

            cursor.execute("DELETE FROM rooms WHERE room_number = %s", (room_number,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Room not found."
            return True, "Room deleted successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Room deletion error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 4. BOOKING MANAGEMENT (BOOKINGS)
    # ---------------------------------------------------------
    def get_all_bookings(self, status=None):
        """
        Get bookings by joining users and room_types, and rooms when assigned.
        room_id may be NULL, so use a LEFT JOIN for rooms.
        Results can be filtered by status.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            base_query = (
                "SELECT b.booking_id, u.full_name, u.email, "
                "b.room_id, rt.type_name, "
                "b.check_in, b.check_out, b.total_price, b.refund_price, "
                "b.status, b.created_at "
                "FROM bookings b "
                "JOIN users u ON b.user_id = u.user_id "
                "JOIN room_types rt ON b.room_type_id = rt.room_type_id "
            )
            if status:
                cursor.execute(base_query + "WHERE b.status = %s ORDER BY b.booking_id DESC", (status,))
            else:
                cursor.execute(base_query + "ORDER BY b.booking_id DESC")
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_booking_detail(self, booking_id):
        """Get one booking's details, including payment information when available."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT b.*, u.full_name, u.email, rt.type_name, rt.price_per_night "
                "FROM bookings b "
                "JOIN users u ON b.user_id = u.user_id "
                "JOIN room_types rt ON b.room_type_id = rt.room_type_id "
                "WHERE b.booking_id = %s",
                (booking_id,)
            )
            booking = cursor.fetchone()
            if not booking:
                return None

            cursor.execute(
                "SELECT * FROM payments WHERE booking_id = %s", (booking_id,)
            )
            booking["payments"] = cursor.fetchall()
            return booking
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def force_cancel_booking(self, booking_id, reason=""):
        """
        Force-cancel a booking as an admin, for example when handling complaints
        or fraud. Unlike cancellation_service.py, this is direct administrator
        intervention. Record the cancellation time in canceled_at.
        Do not calculate refund_price here; handle refunds separately through
        payment_service.py or cancellation_service.py when needed.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bookings SET status = 'Canceled', canceled_at = NOW() "
                "WHERE booking_id = %s",
                (booking_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy booking."
                return True, f"Booking #{booking_id} cancelled. Reason: {reason or 'not specified'}."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Booking cancellation error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 5. REVIEW MANAGEMENT (REVIEWS)
    # ---------------------------------------------------------
    def get_all_reviews(self, only_visible=False):
        """
        Get reviews.
        - only_visible=True: return only reviews with status = 'Published'.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            query = (
                "SELECT rv.review_id, u.full_name, rv.room_id, rv.booking_id, "
                "rv.rating, rv.comment, rv.status, rv.review_date "
                "FROM reviews rv "
                "JOIN users u ON rv.user_id = u.user_id "
            )
            if only_visible:
                query += "WHERE rv.status = 'Published' "
            query += "ORDER BY rv.review_date DESC"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def hide_review(self, review_id):
        """Hide an offending review instead of deleting it."""
        return self._set_review_status(review_id, "Hidden")

    def unhide_review(self, review_id):
        """Republish a review that was previously hidden."""
        return self._set_review_status(review_id, "Published")

    def _set_review_status(self, review_id, status):
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reviews SET status = %s WHERE review_id = %s",
                (status, review_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy đánh giá."
            action = "ẩn" if status == "Hidden" else "hiện lại"
            return True, f"Đã {action} đánh giá #{review_id}."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi cập nhật đánh giá: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_review(self, review_id):
        """Permanently delete a review."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Review not found."
            return True, "Review deleted successfully."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Review deletion error: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 6. STATISTICS / REPORTS (REPORT)
    # ---------------------------------------------------------
    def revenue_report(self, from_date, to_date):
        """
        Revenue report for the [from_date, to_date] period.
        Date format: 'YYYY-MM-DD'. Include only payments with status = 'Paid'.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) AS total_revenue, "
                "COUNT(*) AS total_transactions "
                "FROM payments "
                "WHERE status = 'Paid' AND payment_date BETWEEN %s AND %s",
                (from_date, to_date)
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def booking_statistics(self):
        """Count bookings by status (Pending, Confirmed, and so on)."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT status, COUNT(*) AS total FROM bookings GROUP BY status"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def room_occupancy_report(self):
        """
        Report room usage by counting bookings, excluding canceled bookings.
        Count only bookings assigned to a specific room_id; ignore bookings made
        only by room type that have not yet been assigned a room.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT r.room_number, rt.type_name, "
                "COUNT(b.booking_id) AS total_bookings "
                "FROM rooms r "
                "JOIN room_types rt ON r.room_type_id = rt.room_type_id "
                "LEFT JOIN bookings b "
                "ON r.room_number = b.room_id AND b.status != 'Canceled' "
                "GROUP BY r.room_number "
                "ORDER BY total_bookings DESC"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
