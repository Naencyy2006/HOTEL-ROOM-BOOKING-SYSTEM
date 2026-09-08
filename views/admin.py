"""
views/admin.py
--------------
Giao diện (console) dành cho ADMINISTRATOR.
Chỉ chịu trách nhiệm hiển thị menu, nhận input và gọi AdminService để xử lý
nghiệp vụ -> KHÔNG chứa câu lệnh SQL trực tiếp ở đây (tách biệt view/service
đúng kiến trúc của dự án).

Người phụ trách : Lý Tuấn Đạt
Deadline        : 08/09
"""

from services.admin_service import AdminService

admin_service = AdminService()


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
        print("2. Quản lý phòng")
        print("3. Quản lý đặt phòng")
        print("4. Quản lý đánh giá")
        print("5. Thống kê / Báo cáo")
        print("0. Đăng xuất")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            manage_users_menu()
        elif choice == "2":
            manage_rooms_menu()
        elif choice == "3":
            manage_bookings_menu()
        elif choice == "4":
            manage_reviews_menu()
        elif choice == "5":
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
            _print_users(admin_service.get_all_users())
        elif choice == "2":
            keyword = input("Nhập từ khóa tìm kiếm (username/họ tên/email): ").strip()
            _print_users(admin_service.search_users(keyword))
        elif choice == "3":
            user_id = _input_int("Nhập ID user cần đổi vai trò: ")
            new_role = input("Vai trò mới (member/receptionist/admin): ").strip()
            ok, msg = admin_service.update_user_role(user_id, new_role)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            user_id = _input_int("Nhập ID user cần khóa: ")
            ok, msg = admin_service.lock_user(user_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "5":
            user_id = _input_int("Nhập ID user cần mở khóa: ")
            ok, msg = admin_service.unlock_user(user_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "6":
            user_id = _input_int("Nhập ID user cần xóa: ")
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
    print(f"{'ID':<4}{'Username':<15}{'Họ tên':<20}{'Email':<25}{'Vai trò':<12}{'Trạng thái'}")
    for u in users:
        print(f"{u['id']:<4}{u['username']:<15}{u['full_name']:<20}"
              f"{u['email']:<25}{u['role']:<12}{u['status']}")


# =====================================================
# 2. QUẢN LÝ PHÒNG
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
            _print_rooms(admin_service.get_all_rooms())
        elif choice == "2":
            room_number = input("Số phòng: ").strip()
            room_type = input("Loại phòng: ").strip()
            price = _input_float("Giá phòng: ")
            description = input("Mô tả (có thể để trống): ").strip()
            ok, msg = admin_service.add_room(room_number, room_type, price, description)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "3":
            room_id = _input_int("Nhập ID phòng cần cập nhật: ")
            print("(Để trống nếu không muốn thay đổi trường đó)")
            room_type = input("Loại phòng mới: ").strip() or None
            price_raw = input("Giá mới: ").strip()
            price = float(price_raw) if price_raw else None
            status = input("Trạng thái mới (available/booked/maintenance): ").strip() or None
            description = input("Mô tả mới: ").strip() or None
            ok, msg = admin_service.update_room(room_id, room_type, price, status, description)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            room_id = _input_int("Nhập ID phòng cần xóa: ")
            confirm = input(f"Xác nhận xóa phòng #{room_id}? (y/n): ").strip().lower()
            if confirm == "y":
                ok, msg = admin_service.delete_room(room_id)
                print(("✔ " if ok else "✘ ") + msg)
        elif choice == "0":
            break
        else:
            print(">> Lựa chọn không hợp lệ.")


def _print_rooms(rooms):
    if not rooms:
        print("Không có dữ liệu.")
        return
    print(f"{'ID':<4}{'Số phòng':<10}{'Loại':<15}{'Giá':<12}{'Trạng thái'}")
    for r in rooms:
        print(f"{r['id']:<4}{r['room_number']:<10}{r['room_type']:<15}"
              f"{r['price']:<12}{r['status']}")


# =====================================================
# 3. QUẢN LÝ ĐẶT PHÒNG
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
            _print_bookings(admin_service.get_all_bookings())
        elif choice == "2":
            status = input("Trạng thái (pending/confirmed/checked_in/checked_out/cancelled): ").strip()
            _print_bookings(admin_service.get_all_bookings(status))
        elif choice == "3":
            booking_id = _input_int("Nhập ID booking: ")
            detail = admin_service.get_booking_detail(booking_id)
            if not detail:
                print("Không tìm thấy booking.")
            else:
                print(f"\nBooking #{detail['id']} - Khách: {detail['full_name']}")
                print(f"Phòng: {detail['room_number']} ({detail['room_type']})")
                print(f"Nhận phòng: {detail['check_in']}  |  Trả phòng: {detail['check_out']}")
                print(f"Trạng thái: {detail['status']}")
                print("Thanh toán:")
                if detail["payments"]:
                    for p in detail["payments"]:
                        print(f"  - {p['amount']} ({p['method']}) - {p['status']}")
                else:
                    print("  (chưa có giao dịch thanh toán)")
        elif choice == "4":
            booking_id = _input_int("Nhập ID booking cần hủy: ")
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
    print(f"{'ID':<5}{'Khách hàng':<20}{'Phòng':<10}{'Nhận':<12}{'Trả':<12}{'Trạng thái'}")
    for b in bookings:
        print(f"{b['id']:<5}{b['full_name']:<20}{b['room_number']:<10}"
              f"{str(b['check_in']):<12}{str(b['check_out']):<12}{b['status']}")


# =====================================================
# 4. QUẢN LÝ ĐÁNH GIÁ
# =====================================================
def manage_reviews_menu():
    while True:
        print("\n--- QUẢN LÝ ĐÁNH GIÁ ---")
        print("1. Xem tất cả đánh giá")
        print("2. Chỉ xem đánh giá đang hiển thị")
        print("3. Ẩn đánh giá")
        print("4. Hiện lại đánh giá")
        print("5. Xóa đánh giá")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            _print_reviews(admin_service.get_all_reviews())
        elif choice == "2":
            _print_reviews(admin_service.get_all_reviews(only_visible=True))
        elif choice == "3":
            review_id = _input_int("Nhập ID đánh giá cần ẩn: ")
            ok, msg = admin_service.hide_review(review_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "4":
            review_id = _input_int("Nhập ID đánh giá cần hiện lại: ")
            ok, msg = admin_service.unhide_review(review_id)
            print(("✔ " if ok else "✘ ") + msg)
        elif choice == "5":
            review_id = _input_int("Nhập ID đánh giá cần xóa: ")
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
        visibility = "ẨN" if rv["hidden"] else "hiển thị"
        print(f"[{rv['id']}] {rv['username']} - Phòng {rv['room_number']} "
              f"- {rv['rating']}⭐ ({visibility})")
        print(f"     \"{rv['comment']}\"")


# =====================================================
# 5. THỐNG KÊ / BÁO CÁO
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
            report = admin_service.revenue_report(from_date, to_date)
            print(f"\nTổng doanh thu: {report['total_revenue']}")
            print(f"Số giao dịch thành công: {report['total_transactions']}")
        elif choice == "2":
            stats = admin_service.booking_statistics()
            for s in stats:
                print(f"- {s['status']}: {s['total']}")
        elif choice == "3":
            occupancy = admin_service.room_occupancy_report()
            for o in occupancy:
                print(f"- Phòng {o['room_number']} ({o['room_type']}): "
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
        if value.isdigit():
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
