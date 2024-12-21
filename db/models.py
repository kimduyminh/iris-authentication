from .db_connection import get_connection

# Hàm thêm người dùng
def add_user(username, email, name, iris_image_right, iris_image_left):
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, name, iris_image_right, iris_image_left)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, name, iris_image_right, iris_image_left))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        return False
    except Exception as e:
        print("Lỗi khi thêm người dùng:", e)
        return False

# Hàm tìm kiếm người dùng
def find_user_by_username(username):
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = %s
            """, (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        return None
    except Exception as e:
        print("Lỗi khi tìm kiếm người dùng:", e)
        return None
