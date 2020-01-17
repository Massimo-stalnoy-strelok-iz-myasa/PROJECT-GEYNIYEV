from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QComboBox, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget
from PyQt5.QtGui import QPixmap
from random import randint
from time import sleep
from PyQt5 import uic
from PIL import Image
import statistic_db
import LoginDialog
import sqlite3
import Tetris
from login import logged
import sys
import csv
from flappybird import FlappyBird


class MainWindow(QMainWindow,):
	def __init__(self):
		super().__init__()
		uic.loadUi('MainWindow.ui',self)
		self.login = Login()
		self.k = 0

		self.setWindowTitle('Epic Fails Launcher')

		self.window.setMinimumWidth(100000)

		self.Tetris_start.clicked.connect(self.tetris_game)
		self.Tetris_statistic.clicked.connect(self.tetris_stat)
		self.Flappy_start.clicked.connect(self.flappy_game)

		self.user = QLabel(self)
		self.user_text = QLabel(self)

		self.score = QLabel(self)
		self.score.setMinimumWidth(1000)
		self.score_text = QLabel(self)

		self.time = QLabel(self)
		self.time.setMinimumWidth(1000)
		self.time_text = QLabel(self)

		self.winRate = QLabel(self)
		self.WinRate_text = QLabel(self)

		self.history = QLabel(self)
		self.history_text = QLabel(self)

		self.ret = QPushButton(self)
		self.ret.setText("return")
		self.ret.move(10000, 10000)

		self.Flappy_start.move(10000, 10000)
		self.None_statistic.move(10000, 10000)
		self.Tetris_start.move(10000, 10000)
		self.Tetris_statistic.move(10000, 10000)
		self.ac.move(10000, 10000)
		self.dc.move(10000, 10000)
		self.load_statistic.move(10000, 10000)
		self.save_statistic.move(10000, 10000)

		self.to_login.clicked.connect(self.loginning)

		self.load_statistic.clicked.connect(self.load_stas)


	def tetris_game(self):
		self.tetris = Tetris.Tetris()
		self.tetris.show()

	def flappy_game(self):
		game = FlappyBird()
		game.run()


	def tetris_stat(self):
		subject = "Tetris"
		self.stats, self.usver = statistic_db.return_status(subject)
		self.Flappy_start.move(10000, 10000)
		self.None_statistic.move(10000, 10000)
		self.Tetris_start.move(10000, 10000)
		self.Tetris_statistic.move(10000, 10000)
		self.ac.move(10000, 10000)
		self.dc.move(10000, 10000)
		self.ret.move(400, 400)
		self.ret.clicked.connect(self.main)

		if len(self.stats):
			print(self.stats)
			self.window.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:20pt; font-weight:600;"'
								'>Статистика:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			print(6)
			self.user.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:12pt; font-weight:600;"'
								'>User id:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			self.user.move(100, 100)
			print(7)
			self.user_text.setText(str(self.stats[0][0]))
			print(8)
			self.user_text.move(400, 100)
			print(0)
			self.score.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:12pt; font-weight:600;"'
								'>Max score:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			self.score.move(70, 150)
			self.score_text.setText(str(self.stats[0][3]))
			self.score_text.move(400, 150)
			print(1)
			self.time.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:12pt; font-weight:600;"'
								'>In game time:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			self.time.move(35, 200)
			self.time_text.setText(str(self.stats[0][2]))
			self.time_text.move(400, 200)
			print(2)
			self.winRate.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:12pt; font-weight:600;"'
								'>Win rate:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			self.winRate.move(83, 250)
			self.WinRate_text.setText(str(self.stats[0][4]))
			self.WinRate_text.move(400, 250)
			print(3)
			self.history.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:12pt; font-weight:600;"'
								'>History:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')
			self.history.move(97, 300)
			self.history_text.setText(self.stats[0][5])
			self.history_text.move(400, 300)

			self.update()
		else:
			self.window.setText('<html>'
								'<head/><'
								'body>'
								'<p>'
								'<span style=" font-size:20pt; font-weight:600;"'
								'>Статистики пока нет(:<'
								'/span>'
								'</p>'
								'</body>'
								'</html>')

	def main(self):
		self.Flappy_start.move(370, 90)
		self.None_statistic.move(370, 310)
		self.Tetris_start.move(160, 90)
		self.Tetris_statistic.move(160, 310)
		self.ac.move(590, 90)
		self.dc.move(590, 310)
		self.load_statistic.move(632, 20)
		self.save_statistic.move(632, 50)

		self.load_statistic.clicked.connect(self.load_stas)
		self.save_statistic.clicked.connect(self.save_stas)

		self.user.move(10000, 10000)

		self.user_text.move(10000, 10000)

		self.score.move(10000, 10000)

		self.score_text.move(10000, 10000)

		self.time.move(10000, 10000)

		self.time_text.move(10000, 10000)

		self.winRate.move(10000, 10000)

		self.WinRate_text.move(10000, 10000)

		self.history.move(10000, 10000)

		self.history_text.move(10000, 10000)

		self.ret.move(10000, 10000)

		self.window.setText('<html>'
							'<head/><'
							'body>'
							'<p>'
							'<span style=" font-size:20pt; font-weight:600;"'
							'>Ваша библиотека:<'
							'/span>'
							'</p>'
							'</body>'
							'</html>')

	def loginning(self):
		if not self.k:
			self.k = 1
			self.login.show()
		else:
			self.k = 0
			self.log, self.pas = self.login.returning()
			a = logged(self.log, self.pas)
			print(a)
			if not a:
				k = 0
				self.main()
			else:
				k = 0
				self.login.show()
				self.login.errored()

	def load_stas(self):
		statistic_db.csv_return()

	def save_stas(self):
		stat = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                    '', "(*.csv)")[0]
		if stat:
			statistic_db.csv_load(stat)


class Login(QWidget):
	def __init__(self, error=0):
		super().__init__()
		uic.loadUi('LoginDialog.ui', self)
		self.setWindowTitle("EFL login")
		self.status = 0
		self.confirm.accepted.connect(self.accept)
		self.confirm.rejected.connect(self.reject)

	def accept(self):
		self.status = 1
		self.close()

	def reject(self):
		self.status = -1
		self.close()

	def returning(self):
		return self.login.text(), self.password.text()

	def errored(self):
		self.error.setText("Неверный пароль")



app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec())