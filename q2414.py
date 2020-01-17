from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QComboBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PIL import Image
import sqlite3
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('123.ui', self)

        self.b = sqlite3.connect("Biblia.db")
        self.cur = self.b.cursor()
        self.comboBox.addItems(['По автору', 'По названию'])
        self.pushButton.clicked.connect(self.search)

    def search(self):
        self.cur.execute('''UPDATE Biblia
                            SET Picture = '1.jpg'
                            WHERE Picture = '' ''').fetchall()
        self.b.commit()
        if self.comboBox.currentText() == 'По названию':
            self.request1 = self.lineEdit.text()
            self.result = self.cur.execute("""SELECT * FROM Biblia
                WHERE name = @y """, (self.request1,)).fetchall()
            self.photo = self.cur.execute('''SELECT Picture FROM Biblia
                                            WHERE name = @g ''', (self.request1,)).fetchall()
            if len(self.photo) != 0:
                self.photo = self.photo[0][0]

        if self.comboBox.currentText() == 'По автору':
            self.request = self.lineEdit.text()
            self.result = self.cur.execute("""SELECT * FROM Biblia
                WHERE a = @x """, (self.request,)).fetchall()
            self.photo = self.cur.execute('''SELECT Picture FROM Biblia
                                            WHERE a = @z ''', (self.request,)).fetchall()
            if len(self.photo) != 0:
                self.photo = self.photo[0][0]

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(['name', 'genre', 'year', 'author', 'Picture'])

        for i in range(len(self.result)):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))

        if self.result:
            im = Image.open(self.photo)
            im.save(self.photo)
            self.pixels = im.load()
            self.label.resize(1000, 800)
            self.pixmap = QPixmap(self.photo)
            self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
