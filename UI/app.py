import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from createacc import Ui_Dialog as CreateAccountDialog
from login import Ui_Dialog as LoginDialog
import cam_detection as cd
import cam_detection2 as cd2  # Module dành riêng cho phần login
import psycopg2  # Thêm để kết nối với PostgreSQL

class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.current_window = None

    def show_login(self):
        if self.current_window:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = LoginDialog()
        ui.setupUi(self.current_window)

        # Kết nối các nút
        ui.createaccbutton.clicked.connect(self.show_create_account)
        ui.capture.clicked.connect(lambda: self.handle_capture_login(ui))  # Xử lý logic capture

        self.current_window.show()

    def handle_capture_login(self, ui):
        # Lấy username từ giao diện
        username = ui.username.text().strip()

        # Kiểm tra nếu username trống
        if not username:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập username trước khi chụp ảnh!")
            return

        # Tạo thư mục captured nếu chưa tồn tại
        folder_path = "captured"
        os.makedirs(folder_path, exist_ok=True)

        # Gọi hàm mở camera
        try:
            image_names = cd2.start_cam_login(username)  # Sử dụng hàm từ cam_detection2 cho phần login
            QMessageBox.information(self.current_window, "Thành công", "Chụp ảnh thành công!")
        except Exception as e:
            QMessageBox.critical(self.current_window, "Lỗi", str(e))

    def show_create_account(self):
        if self.current_window:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = CreateAccountDialog()
        ui.setupUi(self.current_window)

        # Kết nối các nút
        ui.login.clicked.connect(self.show_login)
        ui.capture.clicked.connect(lambda: self.handle_capture(ui))  # Kết nối hàm xử lý capture

        self.current_window.show()

    def handle_capture(self, ui):
        # Lấy username từ giao diện
        username = ui.username.text().strip()
        email = ui.email.text().strip()
        name = ui.name.text().strip()

        # Kiểm tra nếu username trống
        if not username or not email or not name:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập đủ thông tin trước khi chụp ảnh!")
            return

        # Tạo thư mục mới trong database_images dựa trên username
        folder_path = os.path.join("database_images", username)
        os.makedirs(folder_path, exist_ok=True)

        # Gọi hàm mở camera
        try:
            image_names = cd.start_cam_create(username)  # Sử dụng hàm từ cam_detection cho phần create account
            self.save_to_database(username, email, name, image_names)
            QMessageBox.information(self.current_window, "Thành công", "Đăng ký và lưu thông tin thành công!")
        except Exception as e:
            QMessageBox.critical(self.current_window, "Lỗi", str(e))

    def save_to_database(self, username, email, name, image_names):
        try:
            # Kết nối đến PostgreSQL
            conn = psycopg2.connect(
                host="postgres",  # Tên dịch vụ trong Docker Compose
                database="iris_authentication",
                user="nguynmjnk",
                password="minh2004"
            )
            cursor = conn.cursor()

            # Chèn dữ liệu vào bảng
            cursor.execute("""
                INSERT INTO users (username, email, name, iris_image)
                VALUES (%s, %s, %s, %s)
            """, (username, email, name, ', '.join(image_names)))  # Lưu danh sách tên ảnh dưới dạng chuỗi

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise Exception(f"Lỗi khi lưu vào database: {e}")

    def run(self):
        self.show_login()
        self.app.exec_()


if __name__ == "__main__":
    app = MainApp()
    app.run()
