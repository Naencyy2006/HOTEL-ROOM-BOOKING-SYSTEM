"""
services/admin_service.py
--------------------------
Xử lý các nghiệp vụ dành cho ADMINISTRATOR:
    - Quản lý người dùng (users)
    - Quản lý loại phòng (room_types)
    - Quản lý phòng (rooms)
    - Quản lý đặt phòng (bookings)
    - Quản lý đánh giá (reviews)
    - Thống kê / báo cáo (report)

Người phụ trách : Lý Tuấn Đạt
Deadline        : 08/09
"""

from config.database import db


class AdminService:
    """
    Toàn bộ nghiệp vụ (business logic) dành cho Admin.
    View (views/admin.py) chỉ gọi các hàm ở đây, KHÔNG thao tác SQL trực tiếp.
    """

    # ---------------------------------------------------------
    # HÀM NỘI BỘ: lấy kết nối an toàn
    # ---------------------------------------------------------
    def _connect(self):
        """
        Lấy connection từ db.get_connection().
        Ném ConnectionError với thông báo rõ ràng nếu kết nối thất bại,
        thay vì để crash bằng AttributeError khi conn = None.
        """
        conn = db.get_connection()
        if conn is None:
            raise ConnectionError("Không thể kết nối tới cơ sở dữ liệu.")
        return conn

    # ---------------------------------------------------------
    # 1. QUẢN LÝ NGƯỜI DÙNG (USERS)
    # ---------------------------------------------------------
    def get_all_users(self, role=None):
        """
        Lấy danh sách toàn bộ user.
        - role: lọc theo vai trò ('Member', 'Receptionist', 'Admin'),
                None = lấy tất cả.
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
        """Tìm user theo họ tên, email hoặc số điện thoại (dùng LIKE)."""
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
        Đổi vai trò của user (ví dụ: nâng Member lên Receptionist).
        new_role phải thuộc {'Member', 'Receptionist', 'Admin'} (đúng ENUM trong schema).
        """
        valid_roles = ("Member", "Receptionist", "Admin")
        if new_role not in valid_roles:
            return False, "Vai trò không hợp lệ."

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
                return False, "Không tìm thấy user."
            return True, "Cập nhật vai trò thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi cập nhật: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def lock_user(self, user_id):
        """Khóa tài khoản user (đặt status = 'Locked')."""
        return self._set_user_status(user_id, "Locked")

    def unlock_user(self, user_id):
        """Mở khóa tài khoản user (đặt status = 'Active')."""
        return self._set_user_status(user_id, "Active")

    def _set_user_status(self, user_id, status):
        """Hàm dùng chung để đổi trạng thái tài khoản (nội bộ, không expose ra view)."""
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
                return False, "Không tìm thấy user."
            return True, f"Đã đổi trạng thái user sang '{status}'."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi cập nhật trạng thái: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_user(self, user_id):
        """
        Xóa user khỏi hệ thống.
        Bookings tham chiếu user_id với ON DELETE RESTRICT nên MySQL sẽ tự
        chặn nếu còn booking bất kỳ (không riêng booking đang hoạt động).
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
                return False, "Không thể xóa: user đã có lịch sử booking trong hệ thống."

            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy user."
            return True, "Xóa user thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi xóa user: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 2. QUẢN LÝ LOẠI PHÒNG (ROOM_TYPES)
    # ---------------------------------------------------------
    def get_all_room_types(self):
        """Lấy danh sách toàn bộ loại phòng."""
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
        """Thêm loại phòng mới (ví dụ: Standard, Deluxe, Suite...)."""
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
            return True, "Thêm loại phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi thêm loại phòng (có thể trùng tên): {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room_type(self, room_type_id, type_name=None, capacity=None,
                          price_per_night=None, description=None):
        """Cập nhật loại phòng. Chỉ cập nhật trường được truyền vào (khác None)."""
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
            return False, "Không có dữ liệu nào để cập nhật."

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
                return False, "Không tìm thấy loại phòng."
            return True, "Cập nhật loại phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi cập nhật loại phòng: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_room_type(self, room_type_id):
        """
        Xóa loại phòng.
        rooms.room_type_id có ON DELETE RESTRICT -> không xóa được nếu còn
        phòng thuộc loại này. Kiểm tra trước để báo lỗi rõ ràng.
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
                return False, "Không thể xóa: vẫn còn phòng thuộc loại này."

            cursor.execute("DELETE FROM room_types WHERE room_type_id = %s", (room_type_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy loại phòng."
            return True, "Xóa loại phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi xóa loại phòng: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 3. QUẢN LÝ PHÒNG (ROOMS)
    # ---------------------------------------------------------
    def get_all_rooms(self):
        """Lấy danh sách toàn bộ phòng, kèm tên loại phòng và giá (join room_types)."""
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
        """Thêm phòng mới. Trạng thái mặc định = 'Available' (theo DEFAULT của schema)."""
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
            return True, "Thêm phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi thêm phòng (có thể trùng số phòng hoặc sai loại phòng): {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_room(self, room_number, room_type_id=None, floor=None, status=None):
        """
        Cập nhật thông tin phòng.
        Chỉ cập nhật các trường được truyền vào (khác None).
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
            return False, "Không có dữ liệu nào để cập nhật."

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
                return False, "Không tìm thấy phòng."
            return True, "Cập nhật phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi cập nhật phòng: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_room(self, room_number):
        """
        Xóa phòng.
        bookings.room_id có ON DELETE RESTRICT -> không xóa được nếu phòng
        còn xuất hiện trong booking nào (kể cả đã checkout, để giữ lịch sử).
        Kiểm tra trước để báo lỗi thân thiện.
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
                return False, "Không thể xóa: phòng đã có lịch sử booking."

            cursor.execute("DELETE FROM rooms WHERE room_number = %s", (room_number,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy phòng."
            return True, "Xóa phòng thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi xóa phòng: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 4. QUẢN LÝ ĐẶT PHÒNG (BOOKINGS)
    # ---------------------------------------------------------
    def get_all_bookings(self, status=None):
        """
        Lấy danh sách booking, join users + room_types (+ rooms nếu đã gán phòng).
        room_id có thể NULL nên dùng LEFT JOIN cho rooms.
        Có thể lọc theo status.
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
        """Xem chi tiết 1 booking cụ thể (kèm thông tin thanh toán nếu có)."""
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
        Admin hủy booking bắt buộc (ví dụ: xử lý khiếu nại, gian lận...).
        Khác với cancellation_service.py (khách tự hủy) vì đây là quyền can
        thiệp trực tiếp của admin. Ghi nhận thời điểm hủy vào canceled_at.
        Không tự tính refund_price ở đây -> nếu cần hoàn tiền, phối hợp với
        payment_service.py / cancellation_service.py xử lý riêng.
        """
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bookings SET status = 'Cancelled', canceled_at = NOW() "
                "WHERE booking_id = %s",
                (booking_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy booking."
            return True, f"Đã hủy booking #{booking_id}. Lý do: {reason or 'không nêu rõ'}."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi hủy booking: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 5. QUẢN LÝ ĐÁNH GIÁ (REVIEWS)
    # ---------------------------------------------------------
    def get_all_reviews(self, only_visible=False):
        """
        Lấy danh sách đánh giá.
        - only_visible=True: chỉ lấy review có status = 'Published'.
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
        """Ẩn một đánh giá vi phạm (spam, ngôn từ không phù hợp...) thay vì xóa hẳn."""
        return self._set_review_status(review_id, "Hidden")

    def unhide_review(self, review_id):
        """Hiện lại đánh giá đã bị ẩn trước đó."""
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
        """Xóa vĩnh viễn một đánh giá."""
        conn, cursor = None, None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False, "Không tìm thấy đánh giá."
            return True, "Xóa đánh giá thành công."
        except ConnectionError as e:
            return False, str(e)
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi xóa đánh giá: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------------------------------------------------
    # 6. THỐNG KÊ / BÁO CÁO (REPORT)
    # ---------------------------------------------------------
    def revenue_report(self, from_date, to_date):
        """
        Báo cáo doanh thu trong khoảng thời gian [from_date, to_date].
        Định dạng ngày: 'YYYY-MM-DD'. Chỉ tính các payment có status = 'Paid'.
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
        """Thống kê số lượng booking theo từng trạng thái (Pending, Confirmed, ...)."""
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
        Thống kê mức độ sử dụng từng phòng: số lần được đặt (không tính
        booking đã hủy). Chỉ tính các booking đã gán room_id cụ thể
        (bỏ qua booking chỉ đặt theo loại phòng, chưa xếp phòng).
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
                "ON r.room_number = b.room_id AND b.status != 'Cancelled' "
                "GROUP BY r.room_number "
                "ORDER BY total_bookings DESC"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
