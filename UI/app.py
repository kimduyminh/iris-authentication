from PyQt5 import QtWidgets
from createacc import Ui_Dialog as CreateAccountDialog
from login import Ui_Dialog as LoginDialog
import cam_detection as cd

class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.current_window = None

    def show_login(self):
        self.current_window = QtWidgets.QDialog()
        ui = LoginDialog()
        ui.setupUi(self.current_window)

        # Kết nối các nút
        ui.createaccbutton.clicked.connect(self.show_create_account)
        ui.capture.clicked.connect(self.open_camera)

        self.current_window.show()

    def show_create_account(self):
        if self.current_window:
            self.current_window.close()

        self.current_window = QtWidgets.QDialog()
        ui = CreateAccountDialog()
        ui.setupUi(self.current_window)

        # Kết nối các nút
        ui.login.clicked.connect(self.show_login)
        ui.capture.clicked.connect(self.open_camera)

        self.current_window.show()

    def open_camera(self):
        cd.start_cam()

    def run(self):
        self.show_login()
        self.app.exec_()


if __name__ == "__main__":
    app = MainApp()
    app.run()
