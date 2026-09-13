# 🏨 HOTEL ROOM BOOKING SYSTEM (DOCKERIZED)

The Hotel Management and Booking System is built with **Python (Tkinter GUI)** and the **MySQL 8.0** database management system. The project is fully packaged with **Docker & Docker Compose** and supports displaying the graphical interface directly in a web browser through **noVNC**.

---

## 📌 Key Features & Container Architecture

- **Zero dependency installation:** Users and instructors do not need to pre-install Python, Tkinter, MySQL, or an X11 Server on the host machine.
- **Web-based GUI access:** Integrates `Xvfb` (virtual display) and `noVNC` to stream the Tkinter application window through HTTP port `6080`.
- **Database automation:** Automatically creates the tables (`schema.sql`) and loads sample data (`seed.sql`) when the Docker container starts for the first time.
- **Healthcheck mechanism:** Ensures that the Python application only starts connecting after the MySQL Server is fully ready.

---

## 🛠 Environment Requirements

The computer running the application only needs:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (supports Windows, macOS, and Linux).

---

## 🚀 Quick Start

### Step 1: Open Terminal/PowerShell in the project directory

```bash
cd HOTEL-ROOM-BOOKING-SYSTEM
```

### Step 2: Start the system with Docker Compose

```bash
docker compose up -d --build
```

The system automatically pulls the required images, creates the MySQL database, loads the data, and starts the Python application in the background.

### Step 3: Open the application in a browser

Open any web browser (Chrome, Edge, or Firefox) and go to:

👉 [**http://localhost:6080**](http://localhost:6080)

Click **Connect** on the web page to interact with the application's Tkinter interface.

---

## 🔑 Sample Login Information & System Configuration

| Component | Details |
|---|---|
| **noVNC Web Interface** | `http://localhost:6080` |
| **MySQL Host Port** | `3307` (avoids conflicts with Windows' default port 3306) |
| **MySQL User / Password** | `root` / `rootpassword` |
| **Database Name** | `hotel_room_booking` |

---

## ⚙️ Useful Docker Management Commands

### Check container status

```bash
docker compose ps
```

### View live logs

```bash
docker compose logs -f
```

### Stop the system (preserve data)

```bash
docker compose stop
```

### Remove the system and reset the initial data (clean reset)

```bash
docker compose down -v
docker compose up -d
```

```text
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

```