from PyQt5 import QtCore, QtGui, QtWidgets
from db.models import add_user  # Import hàm thêm người dùng vào database
from camera_ui import Ui_MainWindow as CameraWindow  # Import giao diện camera

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 620)
        Dialog.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(160, 10, 171, 71))
        self.label.setStyleSheet("color:rgb(225, 225, 225); font-size:28pt;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 101, 31))
        self.label_2.setStyleSheet("font-size:15pt;color:rgb(225, 225, 225)")
        self.label_2.setObjectName("label_2")
        self.username = QtWidgets.QLineEdit(Dialog)
        self.username.setGeometry(QtCore.QRect(190, 110, 211, 51))
        self.username.setStyleSheet("font-size:14pt; color:rgb(243, 243, 243)")
        self.username.setObjectName("username")
        self.email = QtWidgets.QLineEdit(Dialog)
        self.email.setGeometry(QtCore.QRect(190, 200, 211, 51))
        self.email.setStyleSheet("font-size:14pt; color:rgb(243, 243, 243)")
        self.email.setText("")
        self.email.setObjectName("email")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 210, 111, 31))
        self.label_3.setStyleSheet("font-size:15pt; color:rgb(225, 225, 225)")
        self.label_3.setObjectName("label_3")
        self.signupbutton = QtWidgets.QPushButton(Dialog)
        self.signupbutton.setGeometry(QtCore.QRect(270, 450, 171, 41))
        self.signupbutton.setStyleSheet("background-color: rgb(167, 168, 167); font-size:14pt; color:rgb(255, 255, 255)")
        self.signupbutton.setObjectName("signupbutton")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setGeometry(QtCore.QRect(190, 290, 211, 51))
        self.name.setStyleSheet("font-size:14pt; color:rgb(243, 243, 243)")
        self.name.setText("")
        self.name.setObjectName("name")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 300, 151, 31))
        self.label_4.setStyleSheet("font-size:15pt; color:rgb(225, 225, 225)")
        self.label_4.setObjectName("label_4")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 470, 211, 111))
        self.widget.setStyleSheet("image: url(:/image/08f93276-ac5b-46bc-a82a-9887de18b4af.jpg);")
        self.widget.setObjectName("widget")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(290, 510, 151, 20))
        self.label_5.setStyleSheet("color:rgb(255, 255, 255)")
        self.label_5.setObjectName("label_5")
        self.login = QtWidgets.QPushButton(Dialog)
        self.login.setGeometry(QtCore.QRect(310, 550, 93, 31))
        self.login.setStyleSheet("color:rgb(255, 255, 255)")
        self.login.setObjectName("login")
        self.capture = QtWidgets.QPushButton(Dialog)
        self.capture.setGeometry(QtCore.QRect(170, 380, 151, 31))
        self.capture.setStyleSheet("background-color: rgb(167, 168, 167); font-size:10pt; color:rgb(255, 255, 255)")
        self.capture.setObjectName("capture")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Sign up"))
        self.label_2.setText(_translate("Dialog", "Username"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.signupbutton.setText(_translate("Dialog", "Sign up"))
        self.label_4.setText(_translate("Dialog", "Name"))
        self.label_5.setText(_translate("Dialog", "Already have an account?"))
        self.login.setText(_translate("Dialog", "Login"))
        self.capture.setText(_translate("Dialog", "Capture"))

    def save_user(self):
        username = self.username.text()
        email = self.email.text()
        name = self.name.text()
        iris_image = f"{username}_iris.jpg"  # Giả định tên file ảnh

        # Lưu thông tin vào database
        if add_user(username, email, name, iris_image):
            print("Đăng ký thành công!")
        else:
            print("Đăng ký thất bại!")

    def open_camera(self):
        self.camera_window = QtWidgets.QMainWindow()
        self.ui = CameraWindow()
        self.ui.setupUi(self.camera_window)
        self.camera_window.show()


import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
