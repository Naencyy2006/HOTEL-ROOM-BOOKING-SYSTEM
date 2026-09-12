import os
import mysql.connector
from mysql.connector import Error

# Database class for managing MySQL database connections.
class Database:

    # Initialize the Database object with database connection settings.
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")   # Read the host from DB_HOST, defaulting to "localhost".
        self.port = int(os.getenv("DB_PORT", "3306"))   # Read the port from DB_PORT, defaulting to 3306.
        self.database = os.getenv("DB_NAME", "hotel_room_booking") # Read the database name from DB_NAME.
        self.user = os.getenv("DB_USER", "root")        # Read the username from DB_USER, defaulting to "root".
        self.password = os.getenv("DB_PASSWORD", "")    # Read the password from DB_PASSWORD, defaulting to an empty string.

    # Create a connection to the MySQL database.
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )

            # Check whether the connection was established successfully.
            if connection.is_connected():
                return connection
            
            return None

        # Handle database connection errors.
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    # Test the database connection.
    def test_connection(self):
        connection = self.get_connection()

        # Close the connection after a successful test.
        if connection:
            connection.close()
            return True

        return False

# Create a Database instance for use throughout the application.
db = Database()

# Test the database connection when this file is run directly.
if __name__ == "__main__":
    if db.test_connection():
        print("Database connection successful!")
    else:
        print("Database connection failed!")
