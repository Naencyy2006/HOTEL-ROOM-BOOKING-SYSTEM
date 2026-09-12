# main.py
import tkinter as tk
from config.database import db
from views.guest import GuestView
from views.login import LoginRegisterView
from views.admin import AdminApp
from views.member import MemberDashboard
from views.receptionist import ReceptionistView

WINDOW_SIZE = "1100x650"

# Main application class that manages the overall flow of the hotel room booking system, including user authentication and role-based access.
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Room Booking System")
        self.geometry(WINDOW_SIZE)

        # Initialize the database connection and set up the main application window.
        self.conn = db.get_connection() if db.test_connection() else None
        self.current_frame = None

        # Show the guest view as the initial screen when the application starts.
        self.show_guest_view()

    def switch_frame(self, new_frame):
        # Switch the currently displayed frame with a new one.
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_guest_view(self):
        # Display the guest view, allowing users to browse available rooms and access authentication options.
        guest_view = GuestView(
            self, 
            db_conn=self.conn, 
            on_open_auth=self.show_auth_view
        )
        self.switch_frame(guest_view)

    def show_auth_view(self, tab="login"):
        # Display the authentication view (login or register) based on the specified tab.
        auth_view = LoginRegisterView(
            self,
            db_conn=self.conn,
            initial_tab=tab,
            on_login_success=self.on_login_success,
            on_back_guest=self.show_guest_view
        )
        self.switch_frame(auth_view)

    def on_login_success(self, user):
        # Handle successful login by checking the user's role and displaying the appropriate dashboard or view.
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
        # Handle logout from role-specific dashboards (Admin or Receptionist) and return to the guest view.
        app = MainApp()
        app.mainloop()

# Entry point of the application, creating an instance of MainApp and starting the Tkinter main loop.
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()