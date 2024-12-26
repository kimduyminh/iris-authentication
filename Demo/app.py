import os
<<<<<<< HEAD
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
=======

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
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
<<<<<<< HEAD
        print(f"Debug: Username entered = {username}")

=======
        # Debug: Ensure username is passed correctly
        print(f"Debug: Username entered = {username}")

        # Check if username is empty
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        if not username:
            QMessageBox.warning(self.current_window, "Error", "Please enter a username.")
            return

<<<<<<< HEAD
        user_exists = self.db_interface.get_user(username)
        print(f"Debug: User exists = {user_exists}")
=======
        # Simulate fetching user data (update this with real logic)
        user_exists = self.db_interface.get_user(username)
        print(f"Debug: User exists = {user_exists}")  # Debugging log
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72

        if not user_exists:
            QMessageBox.warning(self.current_window, "Error", "User not found in database.")
            return

<<<<<<< HEAD
        if self.compare_image_with_database(username):
            self.show_profile(username)
=======
        # Example image comparison logic for login
        if self.compare_image_with_database(username):
            self.show_profile(username)  # No `ui` parameter here!
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        else:
            QMessageBox.warning(self.current_window, "Error", "Face not recognized.")

    def compare_image_with_database(self, username):
<<<<<<< HEAD
        print("Start comparing")
        result = api.main(username)
        print(result)
        return result

    def handle_capture_login(self, ui):
        username = ui.username.text().strip()

=======
        #return True
        return api.main(username)

    def handle_capture_login(self, ui):
        # Lấy username từ giao diện
        username = ui.username.text().strip()

        # Kiểm tra nếu username trống
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        if not username:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập username trước khi chụp ảnh!")
            return

<<<<<<< HEAD
        folder_path = "captured"
        os.makedirs(folder_path, exist_ok=True)

        try:
            image_names = cam.start_cam_login(username)
=======
        # Tạo thư mục captured nếu chưa tồn tại
        folder_path = "captured"
        os.makedirs(folder_path, exist_ok=True)

        # Gọi hàm mở camera
        try:
            image_names = cam.start_cam_login(username)  # Sử dụng hàm từ cam_detection2 cho phần login
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
            QMessageBox.information(self.current_window, "Thành công", "Chụp ảnh thành công!")
        except Exception as e:
            QMessageBox.critical(self.current_window, "Lỗi", str(e))

    def show_create_account(self):
        if self.current_window:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = CreateAccountDialog()
        ui.setupUi(self.current_window)

<<<<<<< HEAD
        ui.login.clicked.connect(self.show_login)
        ui.capture.clicked.connect(lambda: self.handle_capture(ui))
        self.current_window.show()

    def handle_capture(self, ui):
=======
        # Kết nối các nút
        ui.login.clicked.connect(self.show_login)
        ui.capture.clicked.connect(lambda: self.handle_capture(ui))  # Kết nối hàm xử lý capture

        self.current_window.show()

    def handle_capture(self, ui):
        # Lấy username từ giao diện
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        username = ui.username.text().strip()
        email = ui.email.text().strip()
        name = ui.name.text().strip()

<<<<<<< HEAD
=======
        # Kiểm tra nếu username trống
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        if not username or not email or not name:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập đủ thông tin trước khi chụp ảnh!")
            return

<<<<<<< HEAD
        folder_path = os.path.join("database_images", username)
        os.makedirs(folder_path, exist_ok=True)

        try:
            image_names = cam.start_cam_create(username)
=======
        # Tạo thư mục mới trong database_images dựa trên username
        folder_path = os.path.join("database_images", username)
        os.makedirs(folder_path, exist_ok=True)

        # Gọi hàm mở camera
        try:
            image_names = cam.start_cam_create(username)  # Sử dụng hàm từ cam_detection cho phần create account
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
            self.save_to_database(username, email, name, image_names)
            QMessageBox.information(self.current_window, "Thành công", "Đăng ký và lưu thông tin thành công!")
        except Exception as e:
            QMessageBox.critical(self.current_window, "Lỗi", str(e))

    def save_to_database(self, username, email, name, image_names):
        self.db_interface.add_user(username, email, name, image_names)

    def show_profile(self, username):
<<<<<<< HEAD
=======
        # Check if username is empty
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
        if not username:
            QMessageBox.warning(self.current_window, "Lỗi", "Vui lòng nhập username trước khi đăng nhập!")
            return

<<<<<<< HEAD
        user_data = self.db_interface.get_user(username)
        print(f"Debug: Retrieved user data = {user_data}")

        if user_data:
            QMessageBox.information(self.current_window, "Thành công", "Đăng nhập thành công!")
            self.current_window.hide()

=======
        # Fetch user data from the database
        user_data = self.db_interface.get_user(username)
        print(f"Debug: Retrieved user data = {user_data}")  # Debugging log

        if user_data:
            QMessageBox.information(self.current_window, "Thành công", "Đăng nhập thành công!")
            self.current_window.hide()  # Hide instead of close, so it does not conflict

            # Open the profile window
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72
            self.current_window = QtWidgets.QDialog()
            profile_ui = ProfileDialog()
            profile_ui.setupUi(self.current_window)

<<<<<<< HEAD
            profile_ui.label_2.setText(user_data[0])
            profile_ui.label_3.setText(user_data[1])
            profile_ui.label_4.setText(user_data[2])
=======
            # Set user data in the profile labels
            # Ensure label names match the `.ui` file
            profile_ui.label_2.setText(user_data[0])  # Username
            profile_ui.label_3.setText(user_data[1])  # Email
            profile_ui.label_4.setText(user_data[2])  # Name
>>>>>>> 41edff552eb5ce190d5196e05d62a66a96ad9c72

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
