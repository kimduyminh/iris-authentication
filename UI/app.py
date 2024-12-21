from PyQt5 import QtWidgets
from createacc import Ui_Dialog as CreateAccountDialog
from login import Ui_Dialog as LoginDialog

class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.current_window = None

    def show_login(self):
        self.current_window = QtWidgets.QDialog()
        ui = LoginDialog()
        ui.setupUi(self.current_window)

        # Kết nối nút "Create Account" với giao diện đăng ký
        ui.createaccbutton.clicked.connect(self.show_create_account)

        # Kết nối nút "Capture" để mở camera (tùy chỉnh thêm logic tại đây)
        ui.capture.clicked.connect(self.show_camera)

        self.current_window.show()

    def show_create_account(self):
        if self.current_window is not None:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = CreateAccountDialog()
        ui.setupUi(self.current_window)

        # Kết nối nút "Login" với giao diện đăng nhập
        ui.login.clicked.connect(self.show_login)

        self.current_window.show()

    def show_camera(self):
        # Placeholder cho giao diện camera (nếu có)
        print("Camera functionality goes here")

    def run(self):
        self.show_login()  # Mặc định bắt đầu với giao diện Login
        self.app.exec_()

if __name__ == "__main__":
    app = MainApp()
    app.run()
