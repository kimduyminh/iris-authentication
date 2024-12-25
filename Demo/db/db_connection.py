import psycopg2
from psycopg2 import sql


class DatabaseConnection:
    def __init__(self):
        self.host = "localhost"
        self.database = "iris_authentication"
        self.user = "nguynmjnk"
        self.password = "minh2004"
        self.port = "5432"
        self.connection = None

    def connect(self):
        """Establish connection to the database."""
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                print("Database connection successful.")
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                raise e

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database disconnected.")

    def get_cursor(self):
        """Return a new database cursor."""
        if self.connection is None:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        """Commit the current transaction."""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback the current transaction."""
        if self.connection:
            self.connection.rollback()
