class UserModel:
    def __init__(self, db):
        self.db = db  # DatabaseConnection object

    def create_table(self):
        """Create the users table in the database."""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            iris_image VARCHAR(255) NOT NULL
        );
        """
        cursor = self.db.get_cursor()
        try:
            cursor.execute(query)
            self.db.commit()
            print("Users table created successfully.")
        except Exception as e:
            self.db.rollback()
            print(f"Error creating users table: {e}")

    def add_user(self, username, email, name, iris_image):
        """Insert a new user into the database."""
        query = """
        INSERT INTO users (username, email, name, iris_image)
        VALUES (%s, %s, %s, %s);
        """
        cursor = self.db.get_cursor()
        try:
            cursor.execute(query, (username, email, name, iris_image))
            self.db.commit()
            print("User added successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error adding user: {e}")
            return False

    def get_user(self, username):
        """Retrieve a user by username."""
        query = """
        SELECT * FROM users WHERE username = %s;
        """
        cursor = self.db.get_cursor()
        try:
            cursor.execute(query, (username,))
            return cursor.fetchone()  # Returns the first matching row
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user_email(self, username, new_email):
        """Update the email for a specific user."""
        query = """
        UPDATE users SET email = %s WHERE username = %s;
        """
        cursor = self.db.get_cursor()
        try:
            cursor.execute(query, (new_email, username))
            self.db.commit()
            print("User email updated successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error updating email: {e}")
            return False

    def delete_user(self, username):
        """Delete a user by username."""
        query = """
        DELETE FROM users WHERE username = %s;
        """
        cursor = self.db.get_cursor()
        try:
            cursor.execute(query, (username,))
            self.db.commit()
            print("User deleted successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting user: {e}")
            return False
