# views/receptionist.py
# User interface module for Receptionist operations

from services.receptionist_service import ReceptionistService

class ReceptionistView:
    def __init__(self):
        # Initialize service instance to handle receptionist business logic
        self.service = ReceptionistService()

    def display_menu(self):
        """
        Display the main operation menu for the Receptionist.
        """
        print("\n==========================================")
        print("      HOTEL RECEPTIONIST SYSTEM MENU      ")
        print("==========================================")
        print("1. View Reservations")
        print("2. Create Walk-in Guest Booking")
        print("3. Process Check-in")
        print("4. Process Check-out")
        print("0. Logout / Back")
        print("==========================================")

    def handle_view_reservations(self):
        """
        Display booking records based on user-entered filter criteria.
        """
        print("\n--- RESERVATION LIST ---")
        status_input = input("Filter by status (Pending/Confirmed/Checked-in/Completed/Canceled) [Leave blank for All]: ").strip()
        guest_name_input = input("Filter by guest name [Leave blank for All]: ").strip()

        filter_status = status_input if status_input else None
        guest_name = guest_name_input if guest_name_input else None

        # Fetch reservations from service layer
        reservations = self.service.view_reservations(filter_status=filter_status, guest_name=guest_name)

        if not reservations:
            print("No matching reservation records found.")
            return

        print(f"\nFound {len(reservations)} booking(s):")
        print("-" * 85)
        print(f"{'ID':<6} | {'Guest Name':<20} | {'Phone':<12} | {'Room':<8} | {'Check-in':<11} | {'Status':<12}")
        print("-" * 85)
        for r in reservations:
            room_str = r['room_id'] if r['room_id'] else "Unassigned"
            check_in_str = str(r['check_in'])
            print(f"{r['booking_id']:<6} | {r['full_name']:<20} | {r['phone']:<12} | {room_str:<8} | {check_in_str:<11} | {r['status']:<12}")
        print("-" * 85)

    def handle_walkin_booking(self):
        """
        Collect inputs and invoke service to create a walk-in guest reservation.
        """
        print("\n--- CREATE WALK-IN GUEST BOOKING ---")
        try:
            full_name = input("Guest Full Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone Number: ").strip()
            gender = input("Gender (Male/Female/Other): ").strip()
            year_of_birth = int(input("Year of Birth: "))
            
            room_type_id = int(input("Room Type ID: "))
            room_id = input("Room Number [Press Enter if unassigned]: ").strip()
            if not room_id:
                room_id = None

            check_in = input("Check-in Date (YYYY-MM-DD): ").strip()
            check_out = input("Check-out Date (YYYY-MM-DD): ").strip()
            total_price = float(input("Total Price (VND): "))
            payment_method = input("Payment Method (Cash/Card/Transfer): ").strip()

            # Execute walk-in booking business logic
            success, message = self.service.create_walkin_booking(
                full_name, email, phone, gender, year_of_birth,
                room_type_id, room_id, check_in, check_out, total_price, payment_method
            )
            print(f"\n--> Result: {message}")

        except ValueError:
            print("Invalid input format: Please enter numerical values for Year of Birth, Room Type ID, and Total Price.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_check_in(self):
        """
        Process guest arrival and assign physical room number.
        """
        print("\n--- PROCESS CHECK-IN ---")
        try:
            booking_id = int(input("Enter Booking ID: "))
            room_number = input("Enter physical Room Number [Press Enter to keep pre-assigned room]: ").strip()
            if not room_number:
                room_number = None

            success, message = self.service.process_check_in(booking_id, room_number)
            print(f"\n--> Result: {message}")
        except ValueError:
            print("Booking ID must be an integer.")

    def handle_check_out(self):
        """
        Process guest departure and finalize booking status.
        """
        print("\n--- PROCESS CHECK-OUT ---")
        try:
            booking_id = int(input("Enter Booking ID: "))

            success, message = self.service.process_check_out(booking_id)
            print(f"\n--> Result: {message}")
        except ValueError:
            print("Booking ID must be an integer.")

    def run(self):
        """
        Main execution loop for Receptionist View.
        """
        while True:
            self.display_menu()
            choice = input("Select an option (0-4): ").strip()

            if choice == "1":
                self.handle_view_reservations()
            elif choice == "2":
                self.handle_walkin_booking()
            elif choice == "3":
                self.handle_check_in()
            elif choice == "4":
                self.handle_check_out()
            elif choice == "0":
                print("Exited Receptionist system menu.")
                break
            else:
                print("Invalid choice, please try again!")