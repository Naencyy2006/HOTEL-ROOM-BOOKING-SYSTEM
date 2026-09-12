# main.py
import tkinter as tk
from config.database import db
from views.guest import GuestView
from views.login import LoginRegisterView
from views.admin import AdminApp
from views.member import MemberDashboard
from views.receptionist import ReceptionistView

WINDOW_SIZE = "1100x650"

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Room Booking System")
        self.geometry(WINDOW_SIZE)

        # Kiểm tra kết nối CSDL
        self.conn = db.get_connection() if db.test_connection() else None
        self.current_frame = None

        # Hiển thị giao diện Khách ban đầu
        self.show_guest_view()

    def switch_frame(self, new_frame):
        """Hàm xoá màn hình cũ và thay bằng màn hình mới ngay trong 1 cửa sổ"""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_guest_view(self):
        guest_view = GuestView(
            self, 
            db_conn=self.conn, 
            on_open_auth=self.show_auth_view
        )
        self.switch_frame(guest_view)

    def show_auth_view(self, tab="login"):
        auth_view = LoginRegisterView(
            self,
            db_conn=self.conn,
            initial_tab=tab,
            on_login_success=self.on_login_success,
            on_back_guest=self.show_guest_view
        )
        self.switch_frame(auth_view)

    def on_login_success(self, user):
        role = user.get("role", "Member")
        
        if role == "Admin":
            self.destroy()
            app = AdminApp(current_user=user, on_logout=self._show_guest_after_role_logout)
            app.geometry(WINDOW_SIZE)
            app.mainloop()

        elif role == "Receptionist":
            self.destroy()
            app = ReceptionistView(on_logout=self._show_guest_after_role_logout)
            app.geometry(WINDOW_SIZE)
            app.run()

        elif role == "Member":
            dashboard = MemberDashboard(self, self.conn, user, on_logout=self.show_guest_view)
            self.switch_frame(dashboard)

    def _show_guest_after_role_logout(self):
        """Mở lại màn hình Guest sau khi một cửa sổ theo role đăng xuất."""
        app = MainApp()
        app.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()