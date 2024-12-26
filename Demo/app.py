import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from Demo.UI_components.createacc import Ui_Dialog as CreateAccountDialog
from Demo.UI_components.login import Ui_Dialog as LoginDialog
from Demo.UI_components import camera as cam
from Demo.db.db_connection import DatabaseConnection
from Demo.db.db_interface import UserModel
import model.api.api as api
from Demo.UI_components.profile import Ui_Dialog as ProfileDialog


class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.current_window = None
        self.db_connection = DatabaseConnection()
        self.db_interface = UserModel(self.db_connection)
        self.app.aboutToQuit.connect(self.on_close)

    def show_login(self):
        if self.current_window:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = LoginDialog()
        ui.setupUi(self.current_window)

        # Kết nối các nút
        ui.createaccbutton.clicked.connect(self.show_create_account)
        ui.capture.clicked.connect(lambda: self.handle_capture_login(ui))
        ui.loginbutton.clicked.connect(lambda: self.login_logic(ui.username.text().strip()))
        self.current_window.show()

    def login_logic(self, username):
        # Debug: Ensure username is passed correctly
        print(f"Debug: Username entered = {username}")

        # Check if username is empty
        if not username:
            QMessageBox.warning(self.current_window, "Error", "Please enter a username.")
            return

        # Fetch user data from the database
        user_exists = self.db_interface.get_user(username)
        print(f"Debug: User exists = {user_exists}")

        if not user_exists:
            QMessageBox.warning(self.current_window, "Error", "User not found in database.")
            return

        # Image comparison logic for login
        if self.compare_image_with_database(username):
            self.show_profile(username)
        else:
            QMessageBox.warning(self.current_window, "Error", "Face not recognized.")

    def compare_image_with_database(self, username):
        print("Start comparing")
        result = api.main(username)
        print(result)
        return result

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
            cam.start_cam_login(username)
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
        ui.capture.clicked.connect(lambda: self.handle_capture(ui))
        self.current_window.show()

    def handle_capture(self, ui):
        # Lấy thông tin từ giao diện
        username = ui.username.text().strip()
        email = ui.email.text().strip()
        name = ui.name.text().strip()

        # Kiểm tra nếu thông tin trống
        if not username or not email or not name:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập đủ thông tin trước khi chụp ảnh!")
            return

        # Tạo thư mục mới trong database_images dựa trên username
        folder_path = os.path.join("database_images", username)
        os.makedirs(folder_path, exist_ok=True)

        # Gọi hàm mở camera
        try:
            image_names = cam.start_cam_create(username)
            self.save_to_database(username, email, name, image_names)
            QMessageBox.information(self.current_window, "Thành công", "Đăng ký và lưu thông tin thành công!")
        except Exception as e:
            QMessageBox.critical(self.current_window, "Lỗi", str(e))

    def save_to_database(self, username, email, name, image_names):
        self.db_interface.add_user(username, email, name, image_names)

    def show_profile(self, username):
        user_data = self.db_interface.get_user(username)
        print(f"Debug: Retrieved user data = {user_data}")

        if user_data:
            QMessageBox.information(self.current_window, "Thành công", "Đăng nhập thành công!")
            self.current_window.hide()

            # Open the profile window
            self.current_window = QtWidgets.QDialog()
            profile_ui = ProfileDialog()
            profile_ui.setupUi(self.current_window)

            # Set user data in the profile labels
            profile_ui.label_2.setText(user_data[0])  # Username
            profile_ui.label_3.setText(user_data[1])  # Email
            profile_ui.label_4.setText(user_data[2])  # Name

            self.current_window.show()
        else:
            QMessageBox.warning(self.current_window, "Lỗi", "Không tìm thấy người dùng với username này!")

    def run(self):
        self.show_login()
        self.app.exec_()

    def on_close(self):
        self.db_connection.disconnect()


if __name__ == "__main__":
    app = MainApp()
    app.run()
