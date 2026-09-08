"""
views/admin.py
--------------
Giao diện (console) dành cho ADMINISTRATOR.
Chỉ chịu trách nhiệm hiển thị menu, nhận input và gọi AdminService để xử lý
nghiệp vụ.

Người phụ trách : Lý Tuấn Đạt
Deadline        : 08/09
"""

from services.admin_service import AdminService

admin_service = AdminService()


def _safe_call(func, *args, **kwargs):
    """
    Gọi một hàm đọc dữ liệu của service; nếu bị mất kết nối DB (ConnectionError)
    thì in thông báo lỗi thân thiện và trả về None thay vì làm crash chương trình.
    """
    try:
        return func(*args, **kwargs)
    except ConnectionError as e:
        print(f"✘ {e}")
        return None


def admin_menu(current_user):
    """
    Menu chính của Admin.
    current_user: dict thông tin admin đang đăng nhập (lấy từ auth_service),
                  dùng để hiển thị lời chào.
    """
    while True:
        print("\n===== TRANG QUẢN TRỊ (ADMIN) =====")
        print(f"Xin chào, {current_user.get('full_name', 'Admin')}!")
        print("1. Quản lý người dùng")
        print("2. Quản lý loại phòng")
        print("3. Quản lý phòng")
        print("4. Quản lý đặt phòng")
        print("5. Quản lý đánh giá")
        print("6. Thống kê / Báo cáo")
        print("0. Đăng xuất")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            manage_users_menu()
        elif choice == "2":
            manage_room_types_menu()
        elif choice == "3":
            manage_rooms_menu()
        elif choice == "4":
            manage_bookings_menu()
        elif choice == "5":
            manage_reviews_menu()
        elif choice == "6":
            reports_menu()
        elif choice == "0":
            print("Đăng xuất khỏi tài khoản Admin.")
            break
        else:
            print(">> Lựa chọn không hợp lệ, vui lòng chọn lại.")


# =====================================================
# 1. QUẢN LÝ NGƯỜI DÙNG
# =====================================================
def manage_users_menu():
    while True:
        print("\n--- QUẢN LÝ NGƯỜI DÙNG ---")
        print("1. Xem danh sách user")
        print("2. Tìm kiếm user")
        print("3. Đổi vai trò user")
        print("4. Khóa tài khoản")
        print("5. Mở khóa tài khoản")
        print("6. Xóa user")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            users = _safe_call(admin_service.get_all_users)
            if users is not None:
                _print_users(users)
        elif choice == "2":
            keyword = input("Nhập từ khóa tìm kiếm (họ tên/email/SĐT): ").strip()
            users = _safe_call(admin_service.search_users, keyword)
            if users is not None:
                _print_users(users)
        elif choice == "3":
            user_id = _input_int("Nhập user_id cần đổi vai trò: ")
            new_role = input("Vai trò mới (Member/Receptionist/Admin): ").strip()
            ok, msg = admin_service.update_user_role(user_id, new_role)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            user_id = _input_int("Nhập user_id cần khóa: ")
            ok, msg = admin_service.lock_user(user_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "5":
            user_id = _input_int("Nhập user_id cần mở khóa: ")
            ok, msg = admin_service.unlock_user(user_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "6":
            user_id = _input_int("Nhập user_id cần xóa: ")
            confirm = input(f"Xác nhận xóa user #{user_id}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.delete_user(user_id)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_users(users):
    """In danh sách user dạng bảng đơn giản."""
    if not users:
        print("Không có dữ liệu.")
        return
    print(f"{'ID':<5}{'Họ tên':<20}{'Email':<25}{'SĐT':<15}{'Vai trò':<13}{'Trạng thái'}")
    for u in users:
        print(f"{u['user_id']:<5}{u['full_name']:<20}{u['email']:<25}"
              f"{(u['phone'] or ''):<15}{u['role']:<13}{u['status']}")


# =====================================================
# 2. QUẢN LÝ LOẠI PHÒNG (room_types)
# =====================================================
def manage_room_types_menu():
    while True:
        print("\n--- QUẢN LÝ LOẠI PHÒNG ---")
        print("1. Xem danh sách loại phòng")
        print("2. Thêm loại phòng mới")
        print("3. Cập nhật loại phòng")
        print("4. Xóa loại phòng")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            room_types = _safe_call(admin_service.get_all_room_types)
            if room_types is not None:
                _print_room_types(room_types)
        elif choice == "2":
            type_name = input("Tên loại phòng (VD: Standard, Deluxe, Suite): ").strip()
            capacity = _input_int("Sức chứa (số người): ")
            price = _input_float("Giá mỗi đêm: ")
            description = input("Mô tả (có thể để trống): ").strip()
            ok, msg = admin_service.add_room_type(type_name, capacity, price, description)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "3":
            room_type_id = _input_int("Nhập room_type_id cần cập nhật: ")
            print("(Để trống nếu không muốn thay đổi trường đó)")
            type_name = input("Tên loại phòng mới: ").strip() or None
            capacity_raw = input("Sức chứa mới: ").strip()
            capacity = int(capacity_raw) if capacity_raw else None
            price_raw = input("Giá mới: ").strip()
            price = float(price_raw) if price_raw else None
            description = input("Mô tả mới: ").strip() or None
            ok, msg = admin_service.update_room_type(room_type_id, type_name, capacity, price, description)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            room_type_id = _input_int("Nhập room_type_id cần xóa: ")
            confirm = input(f"Xác nhận xóa loại phòng #{room_type_id}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.delete_room_type(room_type_id)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_room_types(room_types):
    if not room_types:
        print("Không có dữ liệu.")
        return
    print(f"{'ID':<4}{'Tên loại':<15}{'Sức chứa':<10}{'Giá/đêm':<12}{'Mô tả'}")
    for rt in room_types:
        print(f"{rt['room_type_id']:<4}{rt['type_name']:<15}{rt['capacity']:<10}"
              f"{rt['price_per_night']:<12}{rt['description'] or ''}")


# =====================================================
# 3. QUẢN LÝ PHÒNG (rooms)
# =====================================================
def manage_rooms_menu():
    while True:
        print("\n--- QUẢN LÝ PHÒNG ---")
        print("1. Xem danh sách phòng")
        print("2. Thêm phòng mới")
        print("3. Cập nhật phòng")
        print("4. Xóa phòng")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            rooms = _safe_call(admin_service.get_all_rooms)
            if rooms is not None:
                _print_rooms(rooms)
        elif choice == "2":
            # Cần chọn room_type_id có sẵn -> hiển thị danh sách loại phòng trước
            room_types = _safe_call(admin_service.get_all_room_types)
            if room_types is not None:
                _print_room_types(room_types)
            room_number = input("Số phòng (VD: P101): ").strip()
            room_type_id = _input_int("Nhập room_type_id (xem danh sách phía trên): ")
            floor = _input_int("Tầng: ")
            ok, msg = admin_service.add_room(room_number, room_type_id, floor)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "3":
            room_number = input("Nhập số phòng cần cập nhật: ").strip()
            print("(Để trống nếu không muốn thay đổi trường đó)")
            room_type_id_raw = input("room_type_id mới: ").strip()
            room_type_id = int(room_type_id_raw) if room_type_id_raw else None
            floor_raw = input("Tầng mới: ").strip()
            floor = int(floor_raw) if floor_raw else None
            status = input("Trạng thái mới (Available/Booked/Maintenance): ").strip() or None
            ok, msg = admin_service.update_room(room_number, room_type_id, floor, status)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            room_number = input("Nhập số phòng cần xóa: ").strip()
            confirm = input(f"Xác nhận xóa phòng {room_number}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.delete_room(room_number)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_rooms(rooms):
    if not rooms:
        print("Không có dữ liệu.")
        return
    print(f"{'Số phòng':<10}{'Tầng':<6}{'Loại':<15}{'Giá/đêm':<12}{'Trạng thái'}")
    for r in rooms:
        print(f"{r['room_number']:<10}{r['floor']:<6}{r['type_name']:<15}"
              f"{r['price_per_night']:<12}{r['status']}")


# =====================================================
# 4. QUẢN LÝ ĐẶT PHÒNG (bookings)
# =====================================================
def manage_bookings_menu():
    while True:
        print("\n--- QUẢN LÝ ĐẶT PHÒNG ---")
        print("1. Xem tất cả booking")
        print("2. Lọc booking theo trạng thái")
        print("3. Xem chi tiết booking")
        print("4. Hủy booking (bắt buộc)")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            bookings = _safe_call(admin_service.get_all_bookings)
            if bookings is not None:
                _print_bookings(bookings)
        elif choice == "2":
            status = input("Trạng thái (Pending/Confirmed/CheckedIn/CheckedOut/Cancelled): ").strip()
            bookings = _safe_call(admin_service.get_all_bookings, status)
            if bookings is not None:
                _print_bookings(bookings)
        elif choice == "3":
            booking_id = _input_int("Nhập booking_id: ")
            detail = _safe_call(admin_service.get_booking_detail, booking_id)
            if detail is None:
                print("Không tìm thấy booking (hoặc lỗi kết nối).")
            else:
                print(f"\nBooking #{detail['booking_id']} - Khách: {detail['full_name']} ({detail['email']})")
                print(f"Loại phòng: {detail['type_name']}  |  Phòng: {detail['room_id'] or '(chưa xếp phòng)'}")
                print(f"Nhận phòng: {detail['check_in']}  |  Trả phòng: {detail['check_out']}")
                print(f"Tổng tiền: {detail['total_price']}  |  Hoàn tiền: {detail['refund_price']}")
                print(f"Trạng thái: {detail['status']}")
                print("Thanh toán:")
                if detail["payments"]:
                    for p in detail["payments"]:
                        print(f"  - {p['amount']} ({p['payment_method']}) - {p['status']}")
                else:
                    print("  (chưa có giao dịch thanh toán)")
        elif choice == "4":
            booking_id = _input_int("Nhập booking_id cần hủy: ")
            reason = input("Lý do hủy: ").strip()
            confirm = input(f"Xác nhận hủy booking #{booking_id}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.force_cancel_booking(booking_id, reason)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_bookings(bookings):
    if not bookings:
        print("Không có dữ liệu.")
        return
    print(f"{'ID':<5}{'Khách hàng':<20}{'Phòng':<10}{'Nhận':<12}{'Trả':<12}{'Tổng tiền':<12}{'Trạng thái'}")
    for b in bookings:
        room_display = b["room_id"] or "-"
        print(f"{b['booking_id']:<5}{b['full_name']:<20}{room_display:<10}"
              f"{str(b['check_in']):<12}{str(b['check_out']):<12}"
              f"{b['total_price']:<12}{b['status']}")


# =====================================================
# 5. QUẢN LÝ ĐÁNH GIÁ (reviews)
# =====================================================
def manage_reviews_menu():
    while True:
        print("\n--- QUẢN LÝ ĐÁNH GIÁ ---")
        print("1. Xem tất cả đánh giá")
        print("2. Chỉ xem đánh giá đang hiển thị (Published)")
        print("3. Ẩn đánh giá")
        print("4. Hiện lại đánh giá")
        print("5. Xóa đánh giá")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            reviews = _safe_call(admin_service.get_all_reviews)
            if reviews is not None:
                _print_reviews(reviews)
        elif choice == "2":
            reviews = _safe_call(admin_service.get_all_reviews, only_visible=True)
            if reviews is not None:
                _print_reviews(reviews)
        elif choice == "3":
            review_id = _input_int("Nhập review_id cần ẩn: ")
            ok, msg = admin_service.hide_review(review_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            review_id = _input_int("Nhập review_id cần hiện lại: ")
            ok, msg = admin_service.unhide_review(review_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "5":
            review_id = _input_int("Nhập review_id cần xóa: ")
            confirm = input(f"Xác nhận xóa đánh giá #{review_id}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.delete_review(review_id)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_reviews(reviews):
    if not reviews:
        print("Không có dữ liệu.")
        return
    for rv in reviews:
        print(f"[{rv['review_id']}] {rv['full_name']} - Phòng {rv['room_id'] or '-'} "
              f"- {rv['rating']}⭐ ({rv['status']})")
        print(f"     \"{rv['comment']}\"")


# =====================================================
# 6. THỐNG KÊ / BÁO CÁO
# =====================================================
def reports_menu():
    while True:
        print("\n--- THỐNG KÊ / BÁO CÁO ---")
        print("1. Báo cáo doanh thu theo khoảng thời gian")
        print("2. Thống kê booking theo trạng thái")
        print("3. Thống kê tỉ lệ sử dụng phòng")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            from_date = input("Từ ngày (YYYY-MM-DD): ").strip()
            to_date = input("Đến ngày (YYYY-MM-DD): ").strip()
            report = _safe_call(admin_service.revenue_report, from_date, to_date)
            if report is not None:
                print(f"\nTổng doanh thu: {report['total_revenue']}")
                print(f"Số giao dịch thành công: {report['total_transactions']}")
        elif choice == "2":
            stats = _safe_call(admin_service.booking_statistics)
            if stats is not None:
                for s in stats:
                    print(f"- {s['status']}: {s['total']}")
        elif choice == "3":
            occupancy = _safe_call(admin_service.room_occupancy_report)
            if occupancy is not None:
                for o in occupancy:
                    print(f"- Phòng {o['room_number']} ({o['type_name']}): "
                          f"{o['total_bookings']} lượt đặt")
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


# =====================================================
# HÀM TIỆN ÍCH INPUT (validate cơ bản, tránh crash khi nhập sai)
# =====================================================
def _input_int(prompt):
    """Bắt người dùng nhập số nguyên hợp lệ, lặp lại nếu nhập sai."""
    while True:
        value = input(prompt).strip()
        if value.lstrip("-").isdigit():
            return int(value)
        print(">> Vui lòng nhập số nguyên hợp lệ.")


def _input_float(prompt):
    """Bắt người dùng nhập số thực hợp lệ (dùng cho giá phòng)."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print(">> Vui lòng nhập số hợp lệ.")
