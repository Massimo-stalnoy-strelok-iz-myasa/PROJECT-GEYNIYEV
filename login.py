from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QComboBox, QTableWidgetItem, QDialog
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from random import randint
from PyQt5 import uic
from PIL import Image
import datetime
import sqlite3
import Tetris
import rsa
import sys

def center(self):
	screen = QDesktopWidget().screenGeometry()
	print(screen)
	size = self.geometry()
	self.move((screen.width() - size.width()) / 2,
			  (screen.height() - size.height()) / 2)


def logged(login, password):
	now = datetime.datetime.now()
	statistic = sqlite3.connect('users_statistic.db')
	cur = statistic.cursor()

	logins = cur.execute("""SELECT * FROM users
				WHERE id > 0 """).fetchall()

	k = 0
	hashed = password

	for i in range(len(logins)):
		if str(logins[i][1]) == str(login):
			k = 1
			n = i

	if not k:
		cur.execute("""INSERT INTO users(id, login, hash, date)
					VALUES(@a, @b, @c, @d)""",
					(len(logins) + 1, str(login), str(hashed), now.strftime("%d-%m-%Y %H:%M")))
	else:
		if hashed != str(logins[n][2]):
			print("Неверный пароль!")
			return 1

		else:
			cur.execute("""UPDATE users
							SET login = @sub
							WHERE (id = 0) """, (login,))


	statistic.commit()
	cur.close()
	statistic.close()

	return 0