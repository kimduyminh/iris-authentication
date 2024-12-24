from PyQt5 import QtCore, QtGui, QtWidgets
from db.models import find_user_by_username  # Import hàm tìm kiếm người dùng

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 620)
        Dialog.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(190, 50, 121, 71))
        self.label.setStyleSheet("color:rgb(225, 225, 225); font-size:28pt;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 111, 31))
        self.label_2.setStyleSheet("font-size:15pt; color:rgb(225, 225, 225)")
        self.label_2.setObjectName("label_2")
        self.username = QtWidgets.QLineEdit(Dialog)
        self.username.setGeometry(QtCore.QRect(170, 150, 241, 51))
        self.username.setStyleSheet("font-size:14pt; color:rgb(243, 243, 243)")
        self.username.setObjectName("username")
        self.loginbutton = QtWidgets.QPushButton(Dialog)
        self.loginbutton.setGeometry(QtCore.QRect(270, 290, 141, 41))
        self.loginbutton.setStyleSheet("background-color: rgb(167, 168, 167); font-size:14pt; color:rgb(255, 255, 255)")
        self.loginbutton.setObjectName("loginbutton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(120, 360, 131, 16))
        self.label_4.setStyleSheet("color:rgb(255, 255, 255)")
        self.label_4.setObjectName("label_4")
        self.createaccbutton = QtWidgets.QPushButton(Dialog)
        self.createaccbutton.setGeometry(QtCore.QRect(280, 350, 93, 31))
        self.createaccbutton.setStyleSheet("color:rgb(255, 255, 255)")
        self.createaccbutton.setObjectName("createaccbutton")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(70, 410, 331, 131))
        self.widget.setStyleSheet("image: url(:/image/08f93276-ac5b-46bc-a82a-9887de18b4af.jpg);")
        self.widget.setObjectName("widget")
        self.capture = QtWidgets.QPushButton(Dialog)
        self.capture.setGeometry(QtCore.QRect(170, 230, 141, 31))
        self.capture.setStyleSheet("background-color: rgb(167, 168, 167); font-size:10pt; color:rgb(255, 255, 255)")
        self.capture.setObjectName("capture")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Username"))
        self.loginbutton.setText(_translate("Dialog", "Log in"))
        self.label_4.setText(_translate("Dialog", "Don\'t have an account?"))
        self.createaccbutton.setText(_translate("Dialog", "Create Account"))
        self.capture.setText(_translate("Dialog", "Capture"))

    def login_user(self):
        username = self.username.text()
        user = find_user_by_username(username)
        if user:
            print("Đăng nhập thành công!")
            print(f"Thông tin người dùng: {user}")
        else:
            print("Không tìm thấy người dùng với username:", username)
import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
