from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(596, 691)
        Dialog.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 101, 31))
        self.label_2.setStyleSheet("font-size:15pt;color:rgb(225, 225, 225)")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 250, 111, 31))
        self.label_3.setStyleSheet("font-size:15pt; color:rgb(225, 225, 225)")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 330, 151, 31))
        self.label_4.setStyleSheet("font-size:15pt; color:rgb(225, 225, 225)")
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(230, 60, 171, 71))
        self.label.setStyleSheet("color:rgb(225, 225, 225); font-size:28pt;")
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(140, 480, 331, 151))
        self.widget.setStyleSheet("image: url(:/image/08f93276-ac5b-46bc-a82a-9887de18b4af.jpg);")
        self.widget.setObjectName("widget")
        self.logout = QtWidgets.QPushButton(Dialog)
        self.logout.setGeometry(QtCore.QRect(430, 20, 151, 31))
        self.logout.setStyleSheet("background-color: rgb(167, 168, 167); font-size:10pt; color:rgb(255, 255, 255)")
        self.logout.setObjectName("logout")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(240, 170, 231, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 250, 231, 51))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(240, 330, 231, 51))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Username"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.label_4.setText(_translate("Dialog", "Name"))
        self.label.setText(_translate("Dialog", "Profile"))
        self.logout.setText(_translate("Dialog", "Log out"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
