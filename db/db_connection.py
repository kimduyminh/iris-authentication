import psycopg2

# Kết nối PostgreSQL
DB_HOST = "localhost"
DB_NAME = "iris_authentication"
DB_USER = "nguynmjnk"
DB_PASSWORD = "minh2004"
DB_PORT = "5432"

def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Kết nối đến PostgreSQL thất bại:", e)
        return None
