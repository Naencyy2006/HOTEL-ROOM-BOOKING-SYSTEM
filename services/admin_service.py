
"""
services/admin_service.py
--------------------------
Handles business logic for ADMINISTRATOR:
    - User management (users)
    - Room type management (room_types)
    - Room management (rooms)
    - Booking management (bookings)
    - Review management (reviews)
    - Statistics / reports (report)

Responsible person : Ly Tuan Dat
Deadline           : 08/09
"""

from config.database import db


class AdminService:
    """
    Contains all business logic for Admin.
    The view (views/admin.py) only calls methods from this service
    and does NOT execute SQL queries directly.
    """

    # ---------------------------------------------------------
    # INTERNAL METHOD: get a safe database connection
    # ---------------------------------------------------------
    def _connect(self):
        """
        Get a connection from db.get_connection().
        Raise ConnectionError with a clear message if the connection fails,
        instead of causing an AttributeError when conn = None.
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
        Get a list of all users.
        - role: filter by role ('Member', 'Receptionist', 'Admin'),
                None = get all users.
        May raise ConnectionError if the database connection fails.
        The view is responsible for handling this error.
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
        """Search for users by full name, email, or phone number using LIKE."""
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
        Change the role of a user
        (for example, promote a Member to Receptionist).

        new_role must be one of:
        {'Member', 'Receptionist', 'Admin'}
        according to the ENUM defined in the schema.
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

            return True, "User role updated successfully."

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
        """Lock a user account by setting status = 'Locked'."""
        return self._set_user_status(user_id, "Locked")

    def unlock_user(self, user_id):
        """Unlock a user account by setting status = 'Active'."""
        return self._set_user_status(user_id, "Active")

    def _set_user_status(self, user_id, status):
        """Internal helper method for changing the account status."""
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

        Bookings reference user_id with ON DELETE RESTRICT,
        so MySQL will prevent deletion if any booking exists.

        A check is performed first to provide a clearer error message
        instead of exposing the raw MySQL FOREIGN KEY constraint error.
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
                return False, "Cannot delete: user has booking history in the system."

            cursor.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,)
            )

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

    # Rooms depend on room_type_id.
    # Price and description are stored in room_types,
    # so room types should be managed before adding specific rooms.

    def get_all_room_types(self):
        """Get a list of all room types."""
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

    def add_room_type(
        self,
        type_name,
        capacity,
        price_per_night,
        description=""
    ):
        """Add a new room type such as Standard, Deluxe, or Suite."""
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO room_types "
                "(type_name, capacity, description, price_per_night) "
                "VALUES (%s, %s, %s, %s)",
                (
                    type_name,
                    capacity,
                    description,
                    price_per_night
                )
            )

            conn.commit()

            return True, "Room type added successfully."

        except ConnectionError as e:
            return False, str(e)

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error adding room type (name may already exist): {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room_type(
        self,
        room_type_id,
        type_name=None,
        capacity=None,
        price_per_night=None,
        description=None
    ):
        """
        Update room type information.

        Only fields with values different from None are updated.
        """
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
            return False, "No data provided for update."

        values.append(room_type_id)

        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE room_types SET {', '.join(fields)} "
                f"WHERE room_type_id = %s",
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

        rooms.room_type_id uses ON DELETE RESTRICT,
        so deletion is not allowed if rooms still belong to this type.

        A check is performed first to provide a user-friendly error message.
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
                return False, "Cannot delete: rooms still belong to this type."

            cursor.execute(
                "DELETE FROM room_types WHERE room_type_id = %s",
                (room_type_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return False, "Room type not found."

            return True, "Room type deleted successfully."

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
    # 3. ROOM MANAGEMENT (ROOMS)
    # ---------------------------------------------------------

    def get_all_rooms(self):
        """Get all rooms with room type name and price."""
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
        """
        Add a new room.

        The default room status is 'Available',
        according to the schema.
        """
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO rooms "
                "(room_number, room_type_id, floor, status) "
                "VALUES (%s, %s, %s, 'Available')",
                (
                    room_number,
                    room_type_id,
                    floor
                )
            )

            conn.commit()

            return True, "Room added successfully."

        except ConnectionError as e:
            return False, str(e)

        except Exception as e:
            if conn:
                conn.rollback()
            return False, (
                "Error adding room "
                "(room number may already exist or room type may be invalid): "
                f"{e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room(
        self,
        room_number,
        room_type_id=None,
        floor=None,
        status=None
    ):
        """
        Update room information.

        Only fields with values different from None are updated.
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
            return False, "No data provided for update."

        values.append(room_number)

        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE rooms SET {', '.join(fields)} "
                f"WHERE room_number = %s",
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

        bookings.room_id uses ON DELETE RESTRICT,
        so a room cannot be deleted if it appears in any booking,
        including completed or checked-out bookings.

        This preserves booking history.
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
                return False, "Cannot delete: room has booking history."

            cursor.execute(
                "DELETE FROM rooms WHERE room_number = %s",
                (room_number,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return False, "Room not found."

            return True, "Room deleted successfully."

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
    # 4. BOOKING MANAGEMENT (BOOKINGS)
    # ---------------------------------------------------------

    def get_all_bookings(self, status=None):
        """
        Get all bookings with joined user and room type information.

        rooms is not joined because room_id may be NULL.
        A LEFT JOIN would be required if room information is included.

        The result can optionally be filtered by booking status.
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
                cursor.execute(
                    base_query +
                    "WHERE b.status = %s ORDER BY b.booking_id DESC",
                    (status,)
                )
            else:
                cursor.execute(
                    base_query +
                    "ORDER BY b.booking_id DESC"
                )

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_booking_detail(self, booking_id):
        """Get detailed information about a specific booking, including payments."""
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT b.*, u.full_name, u.email, "
                "rt.type_name, rt.price_per_night "
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
                "SELECT * FROM payments WHERE booking_id = %s",
                (booking_id,)
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
        Force-cancel a booking as an administrator,
        for example when handling complaints or suspected fraud.

        This is different from cancellation_service.py,
        which handles customer-initiated cancellation.

        The cancellation time is stored in canceled_at.

        refund_price is not calculated here.
        If a refund is required, it should be handled separately
        through payment_service.py or cancellation_service.py.
        """
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE bookings "
                "SET status = 'Cancelled', canceled_at = NOW() "
                "WHERE booking_id = %s",
                (booking_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return False, "Booking not found."

            return True, (
                f"Booking #{booking_id} has been cancelled. "
                f"Reason: {reason or 'Not specified'}."
            )

        except ConnectionError as e:
            return False, str(e)

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Cancellation error: {e}"

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
        Get all reviews.

        only_visible=True:
        Return only reviews with status = 'Published'.
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
        """Hide a violating review, such as spam or inappropriate content."""
        return self._set_review_status(review_id, "Hidden")

    def unhide_review(self, review_id):
        """Make a previously hidden review visible again."""
        return self._set_review_status(review_id, "Published")

    def _set_review_status(self, review_id, status):
        """Internal helper method for changing the review status."""
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
                return False, "Review not found."

            action = "hidden" if status == "Hidden" else "shown again"

            return True, f"Review #{review_id} has been {action}."

        except ConnectionError as e:
            return False, str(e)

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Review update error: {e}"

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

            cursor.execute(
                "DELETE FROM reviews WHERE review_id = %s",
                (review_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return False, "Review not found."

            return True, "Review deleted successfully."

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
    # 6. STATISTICS / REPORTS (REPORT)
    # ---------------------------------------------------------

    def revenue_report(self, from_date, to_date):
        """
        Generate a revenue report for the date range [from_date, to_date].

        Date format: 'YYYY-MM-DD'.

        Only payments with status = 'Paid' are included.
        """
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) AS total_revenue, "
                "COUNT(*) AS total_transactions "
                "FROM payments "
                "WHERE status = 'Paid' "
                "AND payment_date BETWEEN %s AND %s",
                (from_date, to_date)
            )

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def booking_statistics(self):
        """
        Get the number of bookings grouped by status,
        such as Pending, Confirmed, Cancelled, etc.
        """
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT status, COUNT(*) AS total "
                "FROM bookings "
                "GROUP BY status"
            )

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def room_occupancy_report(self):
        """
        Generate a room usage report.

        Count the number of bookings for each room,
        excluding cancelled bookings.

        Only bookings with a specific room_id are counted.
        Bookings that only specify a room type and have not
        been assigned to a specific room are excluded.
        """
        conn, cursor = None, None

        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT r.room_number, rt.type_name, "
                "COUNT(b.booking_id) AS total_bookings "
                "FROM rooms r "
                "JOIN room_types rt "
                "ON r.room_type_id = rt.room_type_id "
                "LEFT JOIN bookings b "
                "ON r.room_number = b.room_id "
                "AND b.status != 'Cancelled' "
                "GROUP BY r.room_number "
                "ORDER BY total_bookings DESC"
            )

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

