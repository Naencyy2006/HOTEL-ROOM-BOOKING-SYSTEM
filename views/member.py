import os
import sys

# Cho phép chạy trực tiếp file này (bấm nút Run trong VSCode) mà vẫn import
# được thư mục services/ nằm ở gốc project, dù member.py nằm trong views/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from services import booking_service, payment_service, cancellation_service

# ---------- Bảng màu ----------
BG_LIGHT = "#F5EFFF"
BG_SIDEBAR = "#E5D9F2"
ACCENT = "#CDC1FF"
ACCENT2 = "#A594F9"
TEXT_DARK = "#332B4D"
DANGER = "#E27D60"
SUCCESS = "#4CAF50"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


class MemberDashboard(tk.Frame):
    def __init__(self, master, conn, user, **kwargs):
        super().__init__(master, bg=BG_LIGHT, **kwargs)
        self.conn = conn
        self.user = user  # dict: user_id, full_name, email, ...

        self._build_sidebar()
        self._build_content_area()
        self.show_my_bookings()

    # ---------------- Sidebar ----------------
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="🏨 Hotel Booking", bg=BG_SIDEBAR, fg=TEXT_DARK,
            font=FONT_BOLD, pady=20,
        ).pack(fill="x")

        buttons = [
            ("My Booking", self.show_my_bookings),
            ("History", self.show_history),
            ("Profile", self.show_profile),
        ]
        for text, cmd in buttons:
            tk.Button(
                sidebar, text=text, command=cmd, bg=BG_SIDEBAR, fg=TEXT_DARK,
                font=FONT_LABEL, relief="flat", anchor="w", padx=20, pady=10,
                activebackground=ACCENT,
            ).pack(fill="x")

        tk.Button(
            sidebar, text="Logout", command=self._logout, bg=DANGER, fg="white",
            font=FONT_BOLD, relief="flat", pady=10,
        ).pack(side="bottom", fill="x")

    def _logout(self):
        # TODO: gọi hàm logout thật của module đăng nhập (views/login.py)
        self.master.destroy()

    # ---------------- Content area ----------------
    def _build_content_area(self):
        self.content = tk.Frame(self, bg=BG_LIGHT)
        self.content.pack(side="left", fill="both", expand=True, padx=30, pady=20)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ============================================================
    # SCREEN 1: My Bookings
    # ============================================================
    def show_my_bookings(self):
        self._clear_content()
        tk.Label(
            self.content, text="📅 My Bookings", bg=BG_LIGHT, fg=TEXT_DARK,
            font=FONT_TITLE,
        ).pack(anchor="w", pady=(0, 15))

        bookings = [
            b for b in booking_service.list_bookings_by_member(self.conn, self.user["user_id"])
            if b["status"] in ("Confirmed", "Pending Payment")
        ]

        if not bookings:
            tk.Label(self.content, text="Bạn chưa có booking nào.", bg=BG_LIGHT).pack()
            return

        for b in bookings:
            self._render_booking_card(b)

    def _render_booking_card(self, b):
        card = tk.Frame(self.content, bg="white", padx=15, pady=15, highlightbackground=ACCENT,
                         highlightthickness=1)
        card.pack(fill="x", pady=8)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x")
        tk.Label(top, text=f"BOOKING ID: #{b['booking_id']}", bg="white",
                 fg="gray", font=("Segoe UI", 8)).pack(side="left")
        status_color = SUCCESS if b["status"] == "Confirmed" else "#E8A33D"
        tk.Label(top, text=b["status"].upper(), bg="white", fg=status_color,
                 font=FONT_BOLD).pack(side="right")

        tk.Label(card, text=f"Room Type #{b['room_type_id']}", bg="white",
                 fg=ACCENT2, font=FONT_BOLD).pack(anchor="w", pady=(5, 0))
        tk.Label(
            card,
            text=f"Check-in: {b['check_in']}   →   Check-out: {b['check_out']}",
            bg="white", font=FONT_LABEL,
        ).pack(anchor="w")
        tk.Label(
            card, text=f"Total: {b['total_price']:,.0f} VND", bg="white",
            font=FONT_LABEL,
        ).pack(anchor="w")

        actions = tk.Frame(card, bg="white")
        actions.pack(anchor="e", pady=(10, 0))

        if b["status"] == "Pending Payment":
            tk.Button(
                actions, text="Pay Now", bg=SUCCESS, fg="white", relief="flat",
                padx=15, pady=5, command=lambda: self._pay_now(b),
            ).pack(side="right", padx=5)
        else:
            tk.Button(
                actions, text="Cancel Booking", bg=DANGER, fg="white", relief="flat",
                padx=15, pady=5, command=lambda: self._cancel_booking(b),
            ).pack(side="right", padx=5)

    def _pay_now(self, booking):
        method = simpledialog.askstring(
            "Thanh toán", "Chọn phương thức (VNPay/Momo/Visa):", parent=self
        )
        if not method:
            return
        try:
            payment = payment_service.process_payment(self.conn, booking["booking_id"], method)
            messagebox.showinfo("Thành công", f"Thanh toán thành công!\nMã GD: {payment['transaction_code']}")
            self.show_my_bookings()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def _cancel_booking(self, booking):
        preview = cancellation_service.calculate_refund(
            booking["total_price"],
            __import__("datetime").datetime.combine(
                booking["check_in"], __import__("datetime").datetime.min.time()
            ),
        )
        confirm = messagebox.askyesno(
            "Xác nhận huỷ",
            f"Bạn sẽ được hoàn {preview['refund_percent'] * 100:.0f}% "
            f"({preview['refund_amount']:,.0f} VND). Xác nhận huỷ booking?",
        )
        if not confirm:
            return
        try:
            cancellation_service.cancel_booking(self.conn, booking["booking_id"])
            messagebox.showinfo("Đã huỷ", "Booking đã được huỷ thành công.")
            self.show_my_bookings()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ============================================================
    # SCREEN 2: Booking History & Reviews
    # ============================================================
    def show_history(self):
        self._clear_content()
        tk.Label(
            self.content, text="📖 Booking History", bg=BG_LIGHT, fg=TEXT_DARK,
            font=FONT_TITLE,
        ).pack(anchor="w", pady=(0, 15))

        history = [
            b for b in booking_service.list_bookings_by_member(self.conn, self.user["user_id"])
            if b["status"] in ("Completed", "Cancelled")
        ]

        if not history:
            tk.Label(self.content, text="Chưa có lịch sử booking.", bg=BG_LIGHT).pack()
            return

        for b in history:
            self._render_history_card(b)

    def _render_history_card(self, b):
        card = tk.Frame(self.content, bg="white", padx=15, pady=12, highlightbackground=ACCENT,
                         highlightthickness=1)
        card.pack(fill="x", pady=6)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x")
        tk.Label(top, text=f"Room Type #{b['room_type_id']}", bg="white",
                 fg=ACCENT2, font=FONT_BOLD).pack(side="left")
        color = SUCCESS if b["status"] == "Completed" else DANGER
        tk.Label(top, text=b["status"], bg="white", fg=color, font=FONT_BOLD).pack(side="right")

        tk.Label(card, text=f"Dates: {b['check_in']} - {b['check_out']}", bg="white",
                 font=FONT_LABEL).pack(anchor="w")
        tk.Label(card, text=f"{b['total_price']:,.0f} VND", bg="white",
                 font=FONT_BOLD).pack(anchor="w")

        if b["status"] == "Completed":
            tk.Button(
                card, text="⭐ Write Review", bg="#E8A33D", fg="white", relief="flat",
                padx=12, pady=4, command=lambda: self._open_review_dialog(b),
            ).pack(anchor="e", pady=(8, 0))

    def _open_review_dialog(self, booking):
        """
        TODO: gọi review_service (nếu có) để INSERT vào bảng reviews.
        Ở đây chỉ dựng dialog nhập rating + comment theo đúng use-case
        "Write review" (mục 4.4.9).
        """
        win = tk.Toplevel(self)
        win.title("Write Review")
        win.configure(bg="white")

        tk.Label(win, text="Rating (1-5):", bg="white").pack(pady=(10, 0))
        rating_var = tk.IntVar(value=5)
        tk.Spinbox(win, from_=1, to=5, textvariable=rating_var).pack()

        tk.Label(win, text="Comment:", bg="white").pack(pady=(10, 0))
        comment_box = tk.Text(win, width=40, height=5)
        comment_box.pack(padx=10)

        def submit():
            # TODO: review_service.create_review(conn, user_id, booking, rating, comment)
            messagebox.showinfo("Cảm ơn!", "Đánh giá của bạn đã được ghi nhận.")
            win.destroy()

        tk.Button(win, text="Submit", bg=ACCENT2, fg="white", command=submit).pack(pady=10)

    # ============================================================
    # SCREEN 3: Profile / Settings
    # ============================================================
    def show_profile(self):
        self._clear_content()
        tk.Label(
            self.content, text="👤 My Profile", bg=BG_LIGHT, fg=TEXT_DARK,
            font=FONT_TITLE,
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self.content, bg="white", padx=20, pady=20)
        card.pack(fill="x")

        fields = [
            ("Full Name", self.user.get("full_name", "")),
            ("Email", self.user.get("email", "")),
            ("Phone", self.user.get("phone", "")),
            ("Date of Birth", self.user.get("year_of_birth", "")),
        ]
        self._profile_entries = {}
        for label, value in fields:
            tk.Label(card, text=label.upper(), bg="white", fg="gray",
                      font=("Segoe UI", 8)).pack(anchor="w", pady=(8, 0))
            entry = tk.Entry(card, font=FONT_LABEL, width=40)
            entry.insert(0, str(value))
            entry.pack(anchor="w", pady=(0, 5))
            self._profile_entries[label] = entry

        tk.Button(
            card, text="Save Changes", bg=ACCENT2, fg="white", relief="flat",
            padx=15, pady=6, command=self._save_profile,
        ).pack(anchor="e", pady=(10, 0))

    def _save_profile(self):
        """
        TODO: gọi member_service/account_service.update_profile(conn, user_id, data)
        tương ứng User.updateProfile() trong Class Diagram.
        """
        messagebox.showinfo("Đã lưu", "Cập nhật thông tin thành công (demo).")


def open_member_dashboard(root, conn, user):
    """Hàm public để main.py / views/login.py gọi sau khi Member đăng nhập."""
    for w in root.winfo_children():
        w.destroy()
    root.title("Hotel Booking System - Member")
    root.geometry("900x600")
    dashboard = MemberDashboard(root, conn, user)
    dashboard.pack(fill="both", expand=True)
    return dashboard


if __name__ == "__main__":
    # Chạy thử độc lập với dữ liệu giả (không cần DB thật) để xem giao diện.
    class _FakeCursor:
        def execute(self, *a, **k): pass
        def fetchall(self): return []
        def fetchone(self): return None
        def close(self): pass
        rowcount = 0
        lastrowid = 1

    class _FakeConn:
        def cursor(self, dictionary=False): return _FakeCursor()
        def commit(self): pass

    root = tk.Tk()
    fake_user = {"user_id": 1, "full_name": "Nguyen Van A", "email": "a@test.com", "phone": "0900000000"}
    open_member_dashboard(root, _FakeConn(), fake_user)
    root.mainloop()