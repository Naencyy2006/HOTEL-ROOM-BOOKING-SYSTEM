"""
views/admin.py
--------------
Giao diện GUI (Tkinter) dành cho ADMINISTRATOR.
Người phụ trách : Lý Tuấn Đạt
Deadline        : 08/09
Cấu trúc file:
    - Khai báo màu / font dùng chung
    - _safe_call(): gọi hàm đọc dữ liệu của service, bắt ConnectionError
      và hiển thị messagebox thay vì làm crash cửa sổ
    - FormDialog: hộp thoại nhập liệu dùng chung cho các form Thêm/Sửa
    - AdminApp: cửa sổ chính, có sidebar điều hướng + vùng nội dung
    - Các Page (UsersPage, RoomTypesPage, RoomsPage, BookingsPage,
      ReviewsPage, ReportsPage): mỗi Page tương ứng 1 chức năng quản lý
    - admin_menu(current_user): hàm khởi chạy, được gọi từ views/login.py
      sau khi đăng nhập thành công với role = 'Admin'
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.admin_service import AdminService

admin_service = AdminService()

# =====================================================
# BẢNG MÀU & FONT DÙNG CHUNG
# =====================================================
COLOR_MAIN_BG = "#F5EFFF"   # nền chính
COLOR_SIDEBAR = "#E5D9F2"   # nền sidebar
COLOR_BUTTON = "#CDC1FF"    # nút bấm thường
COLOR_ACCENT = "#A594F9"    # nút chính / mục đang chọn
COLOR_TEXT = "#3B2F63"      # chữ tối để tương phản trên nền tím nhạt
COLOR_WHITE = "#FFFFFF"

FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 15, "bold")


def _safe_call(parent, func, *args, **kwargs):
    """
    Gọi một hàm đọc dữ liệu của service; nếu bị mất kết nối DB
    (ConnectionError) thì hiện messagebox lỗi thay vì làm crash cửa sổ.
    Trả về None nếu lỗi, để nơi gọi tự xử lý (thường là bỏ qua fill dữ liệu).
    """
    try:
        return func(*args, **kwargs)
    except ConnectionError as e:
        messagebox.showerror("Lỗi kết nối", str(e), parent=parent)
        return None


def _make_button(parent, text, command, primary=False):
    """Tạo nút bấm đồng bộ theo bảng màu chung của giao diện."""
    return tk.Button(
        parent, text=text, command=command,
        bg=COLOR_ACCENT if primary else COLOR_BUTTON,
        fg=COLOR_WHITE if primary else COLOR_TEXT,
        activebackground=COLOR_ACCENT, activeforeground=COLOR_WHITE,
        font=FONT_NORMAL, bd=0, padx=12, pady=6, cursor="hand2"
    )


def _style_treeview():
    """Cấu hình style chung cho mọi Treeview trong màn Admin (gọi 1 lần khi khởi tạo app)."""
    style = ttk.Style()
    try:
        style.theme_use("clam")  # cần theme 'clam' để đổi được màu heading trên Windows
    except tk.TclError:
        pass
    style.configure(
        "Admin.Treeview",
        background=COLOR_WHITE, fieldbackground=COLOR_WHITE,
        foreground=COLOR_TEXT, rowheight=26, font=FONT_NORMAL
    )
    style.configure(
        "Admin.Treeview.Heading",
        background=COLOR_ACCENT, foreground=COLOR_WHITE, font=FONT_BOLD
    )
    style.map(
        "Admin.Treeview",
        background=[("selected", COLOR_BUTTON)],
        foreground=[("selected", COLOR_TEXT)]
    )


# =====================================================
# HỘP THOẠI NHẬP LIỆU DÙNG CHUNG (Thêm / Sửa)
# =====================================================
class FormDialog(tk.Toplevel):
    """
    Dialog nhập liệu dùng chung cho các form Thêm/Sửa.

    fields: list các tuple (key, label, kind, options)
        kind = "entry"     -> ô nhập văn bản thường
        kind = "combobox"  -> danh sách chọn, options = list giá trị hiển thị
    initial: dict giá trị khởi tạo (dùng khi Sửa, để điền sẵn dữ liệu cũ)

    Sau khi người dùng bấm "Lưu": self.result = dict {key: value (str)}.
    Nếu bấm "Hủy" hoặc đóng cửa sổ: self.result = None.
    Nơi gọi (page) chịu trách nhiệm ép kiểu (int/float) và validate.
    """

    def __init__(self, parent, title, fields, initial=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=COLOR_MAIN_BG)
        self.resizable(False, False)
        self.result = None
        self._vars = {}
        initial = initial or {}

        form = tk.Frame(self, bg=COLOR_MAIN_BG, padx=20, pady=20)
        form.pack(fill="both", expand=True)

        for i, (key, label, kind, options) in enumerate(fields):
            tk.Label(
                form, text=label, bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_NORMAL
            ).grid(row=i, column=0, sticky="w", pady=6)

            var = tk.StringVar(value=str(initial.get(key, "")))
            if kind == "combobox":
                widget = ttk.Combobox(
                    form, textvariable=var, values=options, state="readonly", width=27
                )
            else:
                widget = tk.Entry(form, textvariable=var, width=30, font=FONT_NORMAL)
            widget.grid(row=i, column=1, pady=6, padx=(10, 0))
            self._vars[key] = var

        btn_frame = tk.Frame(self, bg=COLOR_MAIN_BG, pady=10)
        btn_frame.pack(fill="x")
        _make_button(btn_frame, "Lưu", self._on_save, primary=True).pack(side="right", padx=10)
        _make_button(btn_frame, "Hủy", self.destroy).pack(side="right")

        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _on_save(self):
        self.result = {k: v.get().strip() for k, v in self._vars.items()}
        self.destroy()


# =====================================================
# CỬA SỔ CHÍNH: sidebar điều hướng + vùng nội dung
# =====================================================
class AdminApp(tk.Tk):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.title("Hotel Room Booking System - Quản trị")
        self.geometry("1080x640")
        self.minsize(960, 580)
        self.configure(bg=COLOR_MAIN_BG)

        _style_treeview()

        self._build_sidebar()
        self._build_content_area()

        self.pages = {}
        self._register_page("users", UsersPage)
        self._register_page("room_types", RoomTypesPage)
        self._register_page("rooms", RoomsPage)
        self._register_page("bookings", BookingsPage)
        self._register_page("reviews", ReviewsPage)
        self._register_page("reports", ReportsPage)

        self.show_page("users")

    # ------------------------ sidebar ------------------------
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="ADMIN", bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(pady=(24, 4))
        tk.Label(
            sidebar, text=self.current_user.get("full_name", "Admin"),
            bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=FONT_NORMAL
        ).pack(pady=(0, 24))

        nav_items = [
            ("users", "Người dùng"),
            ("room_types", "Loại phòng"),
            ("rooms", "Phòng"),
            ("bookings", "Đặt phòng"),
            ("reviews", "Đánh giá"),
            ("reports", "Báo cáo"),
        ]
        self.nav_buttons = {}
        for key, label in nav_items:
            btn = tk.Button(
                sidebar, text=label, anchor="w", bd=0, padx=20, pady=12,
                bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=FONT_NORMAL,
                activebackground=COLOR_ACCENT, activeforeground=COLOR_WHITE,
                cursor="hand2", command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        tk.Frame(sidebar, bg=COLOR_SIDEBAR).pack(expand=True, fill="both")

        tk.Button(
            sidebar, text="Đăng xuất", anchor="w", bd=0, padx=20, pady=12,
            bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=FONT_NORMAL,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_WHITE,
            cursor="hand2", command=self._logout
        ).pack(fill="x", side="bottom", pady=10)

    def _build_content_area(self):
        self.content = tk.Frame(self, bg=COLOR_MAIN_BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _register_page(self, key, page_class):
        page = page_class(self.content, self)
        page.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.pages[key] = page

    def show_page(self, key):
        """Chuyển trang: đổi màu nút đang chọn trên sidebar + đưa Page lên trên cùng."""
        for k, btn in self.nav_buttons.items():
            is_active = (k == key)
            btn.configure(
                bg=COLOR_ACCENT if is_active else COLOR_SIDEBAR,
                fg=COLOR_WHITE if is_active else COLOR_TEXT
            )
        self.pages[key].tkraise()
        if hasattr(self.pages[key], "on_show"):
            self.pages[key].on_show()

    def _logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?", parent=self):
            self.destroy()


# =====================================================
# 1. TRANG QUẢN LÝ NGƯỜI DÙNG (users)
# =====================================================
class UsersPage(tk.Frame):
    COLUMNS = ("user_id", "full_name", "email", "phone", "role", "status")
    HEADERS = ("ID", "Họ tên", "Email", "SĐT", "Vai trò", "Trạng thái")

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Quản lý người dùng", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        toolbar = tk.Frame(self, bg=COLOR_MAIN_BG)
        toolbar.pack(fill="x", padx=20)

        self.search_var = tk.StringVar()
        tk.Entry(toolbar, textvariable=self.search_var, width=28, font=FONT_NORMAL).pack(
            side="left", padx=(0, 8))
        _make_button(toolbar, "Tìm kiếm", self._search).pack(side="left", padx=4)
        _make_button(toolbar, "Làm mới", self.on_show).pack(side="left", padx=4)
        _make_button(toolbar, "Đổi vai trò", self._change_role).pack(side="left", padx=4)
        _make_button(toolbar, "Khóa", self._lock).pack(side="left", padx=4)
        _make_button(toolbar, "Mở khóa", self._unlock).pack(side="left", padx=4)
        _make_button(toolbar, "Xóa", self._delete, primary=True).pack(side="left", padx=4)

        self.tree = self._build_tree()

    def _build_tree(self):
        tree_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show="headings",
                             style="Admin.Treeview")
        for col, head in zip(self.COLUMNS, self.HEADERS):
            tree.heading(col, text=head)
            tree.column(col, width=140, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def on_show(self):
        """Tải lại danh sách user mỗi khi trang được hiển thị hoặc bấm 'Làm mới'."""
        users = _safe_call(self.app, admin_service.get_all_users)
        self._fill(users or [])

    def _search(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.on_show()
            return
        users = _safe_call(self.app, admin_service.search_users, keyword)
        self._fill(users or [])

    def _fill(self, users):
        self.tree.delete(*self.tree.get_children())
        for u in users:
            self.tree.insert("", "end", iid=str(u["user_id"]), values=(
                u["user_id"], u["full_name"], u["email"], u["phone"] or "",
                u["role"], u["status"]
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một user trong danh sách.",
                                    parent=self.app)
            return None
        return int(sel[0])

    def _change_role(self):
        user_id = self._selected_id()
        if user_id is None:
            return
        dialog = FormDialog(self.app, "Đổi vai trò", [
            ("new_role", "Vai trò mới", "combobox", ["Member", "Receptionist", "Admin"]),
        ])
        if dialog.result:
            ok, msg = admin_service.update_user_role(user_id, dialog.result["new_role"])
            self._notify(ok, msg)

    def _lock(self):
        user_id = self._selected_id()
        if user_id is None:
            return
        ok, msg = admin_service.lock_user(user_id)
        self._notify(ok, msg)

    def _unlock(self):
        user_id = self._selected_id()
        if user_id is None:
            return
        ok, msg = admin_service.unlock_user(user_id)
        self._notify(ok, msg)

    def _delete(self):
        user_id = self._selected_id()
        if user_id is None:
            return
        if messagebox.askyesno("Xác nhận", f"Xóa user #{user_id}?", parent=self.app):
            ok, msg = admin_service.delete_user(user_id)
            self._notify(ok, msg)

    def _notify(self, ok, msg):
        (messagebox.showinfo if ok else messagebox.showerror)(
            "Thành công" if ok else "Lỗi", msg, parent=self.app)
        self.on_show()


# =====================================================
# 2. TRANG QUẢN LÝ LOẠI PHÒNG (room_types)
# =====================================================
class RoomTypesPage(tk.Frame):
    COLUMNS = ("room_type_id", "type_name", "capacity", "price_per_night", "description")
    HEADERS = ("ID", "Tên loại", "Sức chứa", "Giá/đêm", "Mô tả")

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Quản lý loại phòng", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        toolbar = tk.Frame(self, bg=COLOR_MAIN_BG)
        toolbar.pack(fill="x", padx=20)
        _make_button(toolbar, "Làm mới", self.on_show).pack(side="left", padx=4)
        _make_button(toolbar, "Thêm mới", self._add).pack(side="left", padx=4)
        _make_button(toolbar, "Sửa", self._edit).pack(side="left", padx=4)
        _make_button(toolbar, "Xóa", self._delete, primary=True).pack(side="left", padx=4)

        self.tree = self._build_tree()

    def _build_tree(self):
        tree_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show="headings",
                             style="Admin.Treeview")
        for col, head in zip(self.COLUMNS, self.HEADERS):
            tree.heading(col, text=head)
            tree.column(col, width=140, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def on_show(self):
        room_types = _safe_call(self.app, admin_service.get_all_room_types)
        self._fill(room_types or [])

    def _fill(self, room_types):
        self.tree.delete(*self.tree.get_children())
        for rt in room_types:
            self.tree.insert("", "end", iid=str(rt["room_type_id"]), values=(
                rt["room_type_id"], rt["type_name"], rt["capacity"],
                rt["price_per_night"], rt["description"] or ""
            ))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một loại phòng.", parent=self.app)
            return None
        return sel[0], self.tree.item(sel[0])["values"]

    def _add(self):
        dialog = FormDialog(self.app, "Thêm loại phòng", [
            ("type_name", "Tên loại (VD: Deluxe)", "entry", None),
            ("capacity", "Sức chứa (số người)", "entry", None),
            ("price_per_night", "Giá / đêm", "entry", None),
            ("description", "Mô tả", "entry", None),
        ])
        if not dialog.result:
            return
        capacity, price = self._parse_numbers(dialog.result)
        if capacity is None:
            return
        ok, msg = admin_service.add_room_type(
            dialog.result["type_name"], capacity, price, dialog.result["description"]
        )
        self._notify(ok, msg)

    def _edit(self):
        selected = self._selected()
        if not selected:
            return
        iid, values = selected
        dialog = FormDialog(self.app, "Cập nhật loại phòng", [
            ("type_name", "Tên loại", "entry", None),
            ("capacity", "Sức chứa", "entry", None),
            ("price_per_night", "Giá / đêm", "entry", None),
            ("description", "Mô tả", "entry", None),
        ], initial={
            "type_name": values[1], "capacity": values[2],
            "price_per_night": values[3], "description": values[4],
        })
        if not dialog.result:
            return
        capacity, price = self._parse_numbers(dialog.result)
        if capacity is None:
            return
        ok, msg = admin_service.update_room_type(
            int(iid), dialog.result["type_name"], capacity, price, dialog.result["description"]
        )
        self._notify(ok, msg)

    def _parse_numbers(self, data):
        """Ép kiểu sức chứa (int) và giá (float); báo lỗi nếu người dùng nhập sai."""
        try:
            capacity = int(data["capacity"])
            price = float(data["price_per_night"])
            return capacity, price
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Sức chứa và giá phải là số.", parent=self.app)
            return None, None

    def _delete(self):
        selected = self._selected()
        if not selected:
            return
        iid, _ = selected
        if messagebox.askyesno("Xác nhận", f"Xóa loại phòng #{iid}?", parent=self.app):
            ok, msg = admin_service.delete_room_type(int(iid))
            self._notify(ok, msg)

    def _notify(self, ok, msg):
        (messagebox.showinfo if ok else messagebox.showerror)(
            "Thành công" if ok else "Lỗi", msg, parent=self.app)
        self.on_show()


# =====================================================
# 3. TRANG QUẢN LÝ PHÒNG (rooms)
# =====================================================
class RoomsPage(tk.Frame):
    COLUMNS = ("room_number", "floor", "type_name", "price_per_night", "status")
    HEADERS = ("Số phòng", "Tầng", "Loại", "Giá/đêm", "Trạng thái")

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Quản lý phòng", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        toolbar = tk.Frame(self, bg=COLOR_MAIN_BG)
        toolbar.pack(fill="x", padx=20)
        _make_button(toolbar, "Làm mới", self.on_show).pack(side="left", padx=4)
        _make_button(toolbar, "Thêm mới", self._add).pack(side="left", padx=4)
        _make_button(toolbar, "Sửa", self._edit).pack(side="left", padx=4)
        _make_button(toolbar, "Xóa", self._delete, primary=True).pack(side="left", padx=4)

        self.tree = self._build_tree()

    def _build_tree(self):
        tree_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show="headings",
                             style="Admin.Treeview")
        for col, head in zip(self.COLUMNS, self.HEADERS):
            tree.heading(col, text=head)
            tree.column(col, width=140, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def on_show(self):
        rooms = _safe_call(self.app, admin_service.get_all_rooms)
        self._fill(rooms or [])

    def _fill(self, rooms):
        self.tree.delete(*self.tree.get_children())
        for r in rooms:
            self.tree.insert("", "end", iid=r["room_number"], values=(
                r["room_number"], r["floor"], r["type_name"],
                r["price_per_night"], r["status"]
            ))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một phòng.", parent=self.app)
            return None
        return sel[0], self.tree.item(sel[0])["values"]

    def _room_type_options(self):
        """Danh sách 'ID - Tên loại' để chọn trong combobox khi thêm/sửa phòng."""
        room_types = _safe_call(self.app, admin_service.get_all_room_types) or []
        return [f"{rt['room_type_id']} - {rt['type_name']}" for rt in room_types]

    def _add(self):
        options = self._room_type_options()
        if not options:
            messagebox.showwarning(
                "Chưa có loại phòng",
                "Vui lòng thêm loại phòng trước khi thêm phòng cụ thể.", parent=self.app)
            return
        dialog = FormDialog(self.app, "Thêm phòng", [
            ("room_number", "Số phòng (VD: P101)", "entry", None),
            ("room_type", "Loại phòng", "combobox", options),
            ("floor", "Tầng", "entry", None),
        ])
        if not dialog.result:
            return
        try:
            room_type_id = int(dialog.result["room_type"].split(" - ")[0])
            floor = int(dialog.result["floor"])
        except (ValueError, IndexError):
            messagebox.showerror("Lỗi nhập liệu", "Loại phòng / Tầng không hợp lệ.", parent=self.app)
            return
        ok, msg = admin_service.add_room(dialog.result["room_number"], room_type_id, floor)
        self._notify(ok, msg)

    def _edit(self):
        selected = self._selected()
        if not selected:
            return
        room_number, values = selected
        options = self._room_type_options()
        dialog = FormDialog(self.app, "Cập nhật phòng", [
            ("room_type", "Loại phòng mới", "combobox", options),
            ("floor", "Tầng mới", "entry", None),
            ("status", "Trạng thái mới", "combobox", ["Available", "Booked", "Maintenance"]),
        ], initial={"floor": values[1], "status": values[4]})
        if not dialog.result:
            return

        room_type_id = None
        if dialog.result["room_type"]:
            try:
                room_type_id = int(dialog.result["room_type"].split(" - ")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Lỗi nhập liệu", "Loại phòng không hợp lệ.", parent=self.app)
                return
        floor = int(dialog.result["floor"]) if dialog.result["floor"] else None
        status = dialog.result["status"] or None

        ok, msg = admin_service.update_room(room_number, room_type_id, floor, status)
        self._notify(ok, msg)

    def _delete(self):
        selected = self._selected()
        if not selected:
            return
        room_number, _ = selected
        if messagebox.askyesno("Xác nhận", f"Xóa phòng {room_number}?", parent=self.app):
            ok, msg = admin_service.delete_room(room_number)
            self._notify(ok, msg)

    def _notify(self, ok, msg):
        (messagebox.showinfo if ok else messagebox.showerror)(
            "Thành công" if ok else "Lỗi", msg, parent=self.app)
        self.on_show()


# =====================================================
# 4. TRANG QUẢN LÝ ĐẶT PHÒNG (bookings)
# =====================================================
class BookingsPage(tk.Frame):
    COLUMNS = ("booking_id", "full_name", "room_id", "check_in", "check_out",
               "total_price", "status")
    HEADERS = ("ID", "Khách hàng", "Phòng", "Nhận", "Trả", "Tổng tiền", "Trạng thái")
    STATUS_OPTIONS = ["Tất cả", "Pending", "Confirmed", "CheckedIn", "CheckedOut", "Cancelled"]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Quản lý đặt phòng", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        toolbar = tk.Frame(self, bg=COLOR_MAIN_BG)
        toolbar.pack(fill="x", padx=20)

        self.status_var = tk.StringVar(value="Tất cả")
        ttk.Combobox(toolbar, textvariable=self.status_var, values=self.STATUS_OPTIONS,
                     state="readonly", width=14).pack(side="left", padx=(0, 8))
        _make_button(toolbar, "Lọc", self.on_show).pack(side="left", padx=4)
        _make_button(toolbar, "Xem chi tiết", self._view_detail).pack(side="left", padx=4)
        _make_button(toolbar, "Hủy booking", self._cancel, primary=True).pack(side="left", padx=4)

        self.tree = self._build_tree()

    def _build_tree(self):
        tree_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show="headings",
                             style="Admin.Treeview")
        for col, head in zip(self.COLUMNS, self.HEADERS):
            tree.heading(col, text=head)
            tree.column(col, width=120, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def on_show(self):
        status = self.status_var.get()
        status = None if status == "Tất cả" else status
        bookings = _safe_call(self.app, admin_service.get_all_bookings, status)
        self._fill(bookings or [])

    def _fill(self, bookings):
        self.tree.delete(*self.tree.get_children())
        for b in bookings:
            self.tree.insert("", "end", iid=str(b["booking_id"]), values=(
                b["booking_id"], b["full_name"], b["room_id"] or "-",
                b["check_in"], b["check_out"], b["total_price"], b["status"]
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một booking.", parent=self.app)
            return None
        return int(sel[0])

    def _view_detail(self):
        booking_id = self._selected_id()
        if booking_id is None:
            return
        detail = _safe_call(self.app, admin_service.get_booking_detail, booking_id)
        if not detail:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy booking.", parent=self.app)
            return

        win = tk.Toplevel(self.app)
        win.title(f"Chi tiết booking #{detail['booking_id']}")
        win.configure(bg=COLOR_MAIN_BG)

        info = (
            f"Khách hàng : {detail['full_name']} ({detail['email']})\n"
            f"Loại phòng : {detail['type_name']}\n"
            f"Phòng      : {detail['room_id'] or '(chưa xếp phòng)'}\n"
            f"Nhận phòng : {detail['check_in']}\n"
            f"Trả phòng  : {detail['check_out']}\n"
            f"Tổng tiền  : {detail['total_price']}\n"
            f"Hoàn tiền  : {detail['refund_price']}\n"
            f"Trạng thái : {detail['status']}"
        )
        tk.Label(win, text=info, bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_NORMAL,
                 justify="left", anchor="w").pack(padx=20, pady=(20, 10), anchor="w")

        tk.Label(win, text="Thanh toán:", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=FONT_BOLD).pack(padx=20, anchor="w")
        if detail["payments"]:
            for p in detail["payments"]:
                tk.Label(
                    win, text=f"  - {p['amount']} ({p['payment_method']}) - {p['status']}",
                    bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_NORMAL, anchor="w"
                ).pack(padx=20, anchor="w")
        else:
            tk.Label(win, text="  (chưa có giao dịch thanh toán)", bg=COLOR_MAIN_BG,
                     fg=COLOR_TEXT, font=FONT_NORMAL).pack(padx=20, anchor="w")

        _make_button(win, "Đóng", win.destroy, primary=True).pack(pady=16)

    def _cancel(self):
        booking_id = self._selected_id()
        if booking_id is None:
            return
        dialog = FormDialog(self.app, "Hủy booking", [
            ("reason", "Lý do hủy", "entry", None),
        ])
        if dialog.result is None:
            return
        if not messagebox.askyesno("Xác nhận", f"Xác nhận hủy booking #{booking_id}?",
                                    parent=self.app):
            return
        ok, msg = admin_service.force_cancel_booking(booking_id, dialog.result["reason"])
        (messagebox.showinfo if ok else messagebox.showerror)(
            "Thành công" if ok else "Lỗi", msg, parent=self.app)
        self.on_show()


# =====================================================
# 5. TRANG QUẢN LÝ ĐÁNH GIÁ (reviews)
# =====================================================
class ReviewsPage(tk.Frame):
    COLUMNS = ("review_id", "full_name", "room_id", "rating", "status", "comment")
    HEADERS = ("ID", "Khách", "Phòng", "Rating", "Trạng thái", "Bình luận")

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Quản lý đánh giá", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        toolbar = tk.Frame(self, bg=COLOR_MAIN_BG)
        toolbar.pack(fill="x", padx=20)

        self.only_visible_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            toolbar, text="Chỉ hiển thị (Published)", variable=self.only_visible_var,
            bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_NORMAL,
            selectcolor=COLOR_MAIN_BG, command=self.on_show
        ).pack(side="left", padx=(0, 12))
        _make_button(toolbar, "Làm mới", self.on_show).pack(side="left", padx=4)
        _make_button(toolbar, "Ẩn", self._hide).pack(side="left", padx=4)
        _make_button(toolbar, "Hiện lại", self._unhide).pack(side="left", padx=4)
        _make_button(toolbar, "Xóa", self._delete, primary=True).pack(side="left", padx=4)

        self.tree = self._build_tree()

    def _build_tree(self):
        tree_frame = tk.Frame(self, bg=COLOR_MAIN_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=12)
        widths = {"review_id": 60, "full_name": 140, "room_id": 80,
                  "rating": 60, "status": 100, "comment": 300}
        tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show="headings",
                             style="Admin.Treeview")
        for col, head in zip(self.COLUMNS, self.HEADERS):
            tree.heading(col, text=head)
            tree.column(col, width=widths.get(col, 120), anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def on_show(self):
        reviews = _safe_call(self.app, admin_service.get_all_reviews,
                              only_visible=self.only_visible_var.get())
        self._fill(reviews or [])

    def _fill(self, reviews):
        self.tree.delete(*self.tree.get_children())
        for rv in reviews:
            self.tree.insert("", "end", iid=str(rv["review_id"]), values=(
                rv["review_id"], rv["full_name"], rv["room_id"] or "-",
                rv["rating"], rv["status"], (rv["comment"] or "")[:80]
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một đánh giá.", parent=self.app)
            return None
        return int(sel[0])

    def _hide(self):
        review_id = self._selected_id()
        if review_id is None:
            return
        ok, msg = admin_service.hide_review(review_id)
        self._notify(ok, msg)

    def _unhide(self):
        review_id = self._selected_id()
        if review_id is None:
            return
        ok, msg = admin_service.unhide_review(review_id)
        self._notify(ok, msg)

    def _delete(self):
        review_id = self._selected_id()
        if review_id is None:
            return
        if messagebox.askyesno("Xác nhận", f"Xóa đánh giá #{review_id}?", parent=self.app):
            ok, msg = admin_service.delete_review(review_id)
            self._notify(ok, msg)

    def _notify(self, ok, msg):
        (messagebox.showinfo if ok else messagebox.showerror)(
            "Thành công" if ok else "Lỗi", msg, parent=self.app)
        self.on_show()


# =====================================================
# 6. TRANG THỐNG KÊ / BÁO CÁO
# =====================================================
class ReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_MAIN_BG)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self, text="Thống kê / Báo cáo", bg=COLOR_MAIN_BG, fg=COLOR_TEXT, font=FONT_TITLE
        ).pack(anchor="w", padx=20, pady=(16, 8))

        # --- Báo cáo doanh thu ---
        revenue_box = tk.LabelFrame(
            self, text="Doanh thu theo khoảng thời gian", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
            font=FONT_BOLD, padx=12, pady=12
        )
        revenue_box.pack(fill="x", padx=20, pady=8)

        tk.Label(revenue_box, text="Từ ngày (YYYY-MM-DD):", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=FONT_NORMAL).grid(row=0, column=0, sticky="w")
        self.from_date_var = tk.StringVar()
        tk.Entry(revenue_box, textvariable=self.from_date_var, width=14,
                 font=FONT_NORMAL).grid(row=0, column=1, padx=6)

        tk.Label(revenue_box, text="Đến ngày (YYYY-MM-DD):", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=FONT_NORMAL).grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.to_date_var = tk.StringVar()
        tk.Entry(revenue_box, textvariable=self.to_date_var, width=14,
                 font=FONT_NORMAL).grid(row=0, column=3, padx=6)

        _make_button(revenue_box, "Xem báo cáo", self._show_revenue, primary=True).grid(
            row=0, column=4, padx=12)

        self.revenue_result_var = tk.StringVar(value="")
        tk.Label(revenue_box, textvariable=self.revenue_result_var, bg=COLOR_MAIN_BG,
                 fg=COLOR_TEXT, font=FONT_NORMAL, justify="left").grid(
            row=1, column=0, columnspan=5, sticky="w", pady=(10, 0))

        # --- Thống kê booking theo trạng thái ---
        booking_box = tk.LabelFrame(
            self, text="Thống kê booking theo trạng thái", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
            font=FONT_BOLD, padx=12, pady=12
        )
        booking_box.pack(fill="x", padx=20, pady=8)
        _make_button(booking_box, "Xem thống kê", self._show_booking_stats).pack(anchor="w")
        self.booking_tree = ttk.Treeview(
            booking_box, columns=("status", "total"), show="headings",
            height=6, style="Admin.Treeview"
        )
        self.booking_tree.heading("status", text="Trạng thái")
        self.booking_tree.heading("total", text="Số lượng")
        self.booking_tree.pack(fill="x", pady=(8, 0))

        # --- Tỉ lệ sử dụng phòng ---
        occupancy_box = tk.LabelFrame(
            self, text="Tỉ lệ sử dụng phòng", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
            font=FONT_BOLD, padx=12, pady=12
        )
        occupancy_box.pack(fill="both", expand=True, padx=20, pady=8)
        _make_button(occupancy_box, "Xem thống kê", self._show_occupancy).pack(anchor="w")
        self.occupancy_tree = ttk.Treeview(
            occupancy_box, columns=("room_number", "type_name", "total_bookings"),
            show="headings", height=6, style="Admin.Treeview"
        )
        self.occupancy_tree.heading("room_number", text="Số phòng")
        self.occupancy_tree.heading("type_name", text="Loại phòng")
        self.occupancy_tree.heading("total_bookings", text="Lượt đặt")
        self.occupancy_tree.pack(fill="both", expand=True, pady=(8, 0))

    def on_show(self):
        # Báo cáo chỉ tải khi người dùng chủ động bấm nút, tránh query không cần thiết
        # mỗi lần chuyển sang tab này.
        pass

    def _show_revenue(self):
        from_date = self.from_date_var.get().strip()
        to_date = self.to_date_var.get().strip()
        if not from_date or not to_date:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ khoảng thời gian.",
                                    parent=self.app)
            return
        report = _safe_call(self.app, admin_service.revenue_report, from_date, to_date)
        if report is not None:
            self.revenue_result_var.set(
                f"Tổng doanh thu: {report['total_revenue']}    |    "
                f"Số giao dịch thành công: {report['total_transactions']}"
            )

    def _show_booking_stats(self):
        stats = _safe_call(self.app, admin_service.booking_statistics)
        self.booking_tree.delete(*self.booking_tree.get_children())
        for s in (stats or []):
            self.booking_tree.insert("", "end", values=(s["status"], s["total"]))

    def _show_occupancy(self):
        occupancy = _safe_call(self.app, admin_service.room_occupancy_report)
        self.occupancy_tree.delete(*self.occupancy_tree.get_children())
        for o in (occupancy or []):
            self.occupancy_tree.insert("", "end", values=(
                o["room_number"], o["type_name"], o["total_bookings"]
            ))


# =====================================================
# ĐIỂM KHỞI CHẠY (được gọi từ views/login.py sau khi đăng nhập role='Admin')
# =====================================================
def admin_menu(current_user):
    """
    Khởi chạy giao diện GUI cho Admin.
    current_user: dict thông tin admin đang đăng nhập, tối thiểu cần 'full_name'.
    """
    app = AdminApp(current_user)
    app.mainloop()


if __name__ == "__main__":
    # Cho phép chạy thử độc lập file này khi chưa nối được với login.py
    admin_menu({"full_name": "Admin Test"})
