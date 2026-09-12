from config.database import db
from utils.password import hash_password, verify_password
from utils.validators import validate_email, validate_password, validate_phone

class AuthService:
    # This class provides authentication services for user registration, login, logout, and password reset.
    def __init__(self):
        # Initialize the AuthService with a database connection and a placeholder for the current user session.
        self.current_user = None

    # Register a new user account with the provided details.
    def register(self, full_name: str, dob: str, gender: str, phone: str, email: str, password: str, confirm_password: str):
        # check if the email is already registered in the database
        if not validate_email(email):
            return False, "Invalid email address format."

        # Validate the password and confirmation.
        if not validate_password(password):
            return False, "Password must be at least 6 characters long."

        # Check if the password and confirmation match.
        if password != confirm_password:
            return False, "Password confirmation does not match."

        # Validate the phone number format.
        if not validate_phone(phone):
            return False, "Invalid phone number format."

        # Establish a database connection and perform the registration process.
        conn = db.get_connection()
        if not conn:
            return False, "Database connection error."
        cursor = conn.cursor(dictionary=True)

        try:
            # Check if the email already exists in the USERS table
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "This email is already registered in the system."

            # Hash the password before storing it in the database.
            hashed_pwd = hash_password(password)
         
            # Extract the year of birth from a YYYY-MM-DD date of birth string.
            year_of_birth = int(dob.split('-')[0]) if '-' in dob and dob.split('-')[0].isdigit() else None

            # Insert the new user record into the USERS table with the provided details.
            query = """
                INSERT INTO USERS (full_name, email, phone, gender, year_of_birth, password_hash, role, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Member', 'Active')
            """

            # Execute the query with the user details and commit the transaction to save the new user in the database.  
            cursor.execute(query, (full_name, email, phone, gender, year_of_birth, hashed_pwd))
            conn.commit()
            return True, "Account registered successfully!"

        # Handle any exceptions that occur during the registration process, rolling back the transaction if necessary.    
        except Exception as e:
            conn.rollback()
            return False, f"Database error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    # Log in a user with the provided email and password, returning the user details if successful.
    def login(self, email: str, password: str):
    
        conn = db.get_connection()
        if not conn:
            return False, "Database connection error.", None
        cursor = conn.cursor(dictionary=True)

        # Attempt to retrieve the user record from the database and verify the provided credentials.
        try:
            # Execute a query to find the user by email.
            cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()

            # Check if the user exists and verify the password hash. If either check fails, return an error message.
            if not user or not verify_password(user['password_hash'], password):
                return False, "Invalid email address or password.", None

            # Check if the account is locked by Administrator
            if user['status'] == 'Locked':
                return False, "Your account is locked due to policy violations. Contact support.", None

            # Login successful, save the session information
            self.current_user = user
            return True, "Login successful!", user
        finally:
            cursor.close()
            conn.close()

    # Log out the currently logged-in user by clearing the session information.
    def logout(self):
        # Clear the current user session information to log out the user.
        self.current_user = None
        return True, "Logged out successfully."

    # Reset the password for a user account, validating the new password and updating it in the database.
    def reset_password(self, email: str, new_password: str, confirm_password: str):
        # Validate the new password requirements.
        if not validate_password(new_password):
            return False, "New password must be at least 6 characters long."
        if new_password != confirm_password:
            return False, "Password confirmation does not match."

        conn = db.get_connection()
        if not conn:
            return False, "Database connection error."
        cursor = conn.cursor(dictionary=True)

        try:
            # Check whether the email exists.
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Email address not found."

            # Hash and update the new password.
            hashed_pwd = hash_password(new_password)
            cursor.execute("UPDATE USERS SET password_hash = %s WHERE email = %s", (hashed_pwd, email))
            conn.commit()
            return True, "Password updated successfully."
        except Exception as e:
            conn.rollback()
            return False, f"Error updating password: {str(e)}"
        finally:
            cursor.close()
            conn.close()