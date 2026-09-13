HotelRoomBookingSystem/
│
├── main.py                         # System entry point
├── README.md                       # Project overview and setup/usage instructions
├── requirements.txt                # List of Python dependencies
├── .gitignore                      # Files and directories ignored by Git
│
├── config/                         # System configuration directory
│   └── database.py                 # Database configuration and connection setup
│
├── database/                       # SQL scripts directory
│   ├── schema.sql                  # Database schema definition, tables, and constraints (PK/FK)
│   └── seed.sql                    # Initial seed data for system testing/demo
│
├── docs/                           # System analysis and design documentation
│   └── RequirementAndDesignDocument_Group.pdf  # Requirements & Design Document (PDF)
│
├── models/                         # Data Layer - Classes representing database tables
│   ├── __init__.py                 # Package initializer for models
│   ├── user.py                     # Model representing the Users table
│   ├── room_type.py                # Model representing the RoomTypes table
│   ├── room.py                     # Model representing the Rooms table
│   ├── booking.py                  # Model representing the Bookings table
│   ├── payment.py                  # Model representing the Payments table
│   └── review.py                   # Model representing the Reviews table
│
├── services/                       # Business Logic Layer
│   ├── admin_service.py            # Admin operations: Room/User/Booking management & reporting
│   ├── auth_service.py             # Authentication: Registration, Login, Logout, Password reset
│   ├── booking_service.py          # Room booking workflows and booking history management
│   ├── cancellation_service.py     # Room cancellation processing and refund calculations
│   ├── payment_service.py          # Payment processing and invoice generation
│   ├── receptionist_service.py     # Receptionist operations: Walk-in bookings, Check-in, Check-out
│   ├── review_service.py           # Customer review management, submission, and display
│   ├── room_service.py             # Room search, filtering, and availability checking
│   └── user_service.py             # User profile updates and account management
│
├── utils/                          # Shared utility functions
│   ├── password.py                 # Password hashing and verification
│   └── validators.py               # Input validation (Email, Phone, Dates, etc.)
│
└── views/                          # UI Layer / User Interface Navigation
    ├── admin.py                    # Interface and navigation for Administrators
    ├── guest.py                    # Interface and features for unregistered Guests
    ├── login.py                    # Login and Registration user interfaces
    ├── member.py                   # Interface and navigation for registered Members
    └── receptionist.py             # Interface and navigation for Receptionists