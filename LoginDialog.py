from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.confirm = QtWidgets.QDialogButtonBox(Dialog)
        self.confirm.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.confirm.setOrientation(QtCore.Qt.Horizontal)
        self.confirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm.setObjectName("confirm")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 31))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 171, 31))
        self.label_2.setObjectName("label_2")

        self.login = QtWidgets.QLineEdit(Dialog)
        self.login.setGeometry(QtCore.QRect(20, 60, 351, 22))
        self.login.setObjectName("login")

        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(20, 130, 351, 22))
        self.password.setObjectName("password")

        self.errors = QtWidgets.QLabel(Dialog)
        self.errors.setGeometry(QtCore.QRect(20, 170, 331, 51))
        self.errors.setObjectName("errors")

        self.retranslateUi(Dialog)
        self.confirm.accepted.connect(Dialog.accept)
        self.confirm.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Input yor name:</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Input your password:</span></p></body></html>"))
        self.errors.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
