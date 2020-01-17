from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import statistic_db
import sys, random
import winsound
import datetime
import sqlite3

# Код взят с PythonWorld.com
# All copyrights reserved by Oleg production
# Product made in association with LN inc.
# (внесены косметические изменения, использован в целях сбора статистики)

start_time = datetime.datetime.now().strftime("%H:%M:%S")
set_score = 0


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.tboard = Board(self) # Подключение поля
        self.setCentralWidget(self.tboard) # Задание поля как основы

        self.statusbar = self.statusBar() # Создание счетчика очков
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage) # Передача значения для статусбара
        # из initUI в Board (Между классами)
        # (Событие определяет данные)

        self.tboard.start() # Запуск основы (включение приложения)

        self.resize(180, 380) # Задание пропорций
        self.center() # Перемещение на середину экрана
        self.setWindowTitle('Tetris') # Название окна
        self.show() # Начало работы приложения

        winsound.PlaySound("tetris.wav", winsound.SND_ASYNC) # Врубай музычку, туц-туц-туц


    def center(self):
        screen = QDesktopWidget().screenGeometry() # Возвращение параметров экрана (разрешение в пикселах)
        size = self.geometry() # Возвращение параметров окна (размер в пикселах)
        self.move((screen.width()-size.width())/2, # перемещение на центр по вертикали
            (screen.height()-size.height())/2) # Перемещение на центр по горизонтали


class Board(QFrame): # Класс создания поля
    msg2Statusbar = pyqtSignal(str) # Сигнал изменения, нужен для передачи данных из Tetris в Board

    BoardWidth = 10 # Ширина доски
    BoardHeight = 22 # Высота доски
    Speed = 300 # Скорость повторения цикла игры

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()


    def initBoard(self):
        self.timer = QBasicTimer() # Таймер цикла падения тетрамино (спавнит фигурки со скоростью speed)
        self.isWaitingAfterLine = False # Ожидание падения

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0 # Счетчик очков
        # Очки в этой игре равны кол-ву удаленных линий
        self.board = [] # Фигурки лежащие на доске

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False # Индикатор начала игры
        self.isPaused = False # Индикатор паузы
        self.clearBoard() # Очистка доски


    def shapeAt(self, x, y): # Вывод фигуры для данного положения
        return self.board[(y * Board.BoardWidth) + x]


    def setShapeAt(self, x, y, shape): # Задание позиции фигуре для отображения ее статичной формы на экране
        self.board[(y * Board.BoardWidth) + x] = shape


    def squareWidth(self): # Ширина квадратика (секции тетрамино)
        return self.contentsRect().width() // Board.BoardWidth


    def squareHeight(self): # Высота -||-
        return self.contentsRect().height() // Board.BoardHeight


    def start(self): # Запуск игры
        if self.isPaused: # Заглушка на паузу
            return

        self.isStarted = True # Изменяем индикатор игры на TRUE
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0 # Обнуляем Счетчик
        self.clearBoard() # Чистим доску

        self.msg2Statusbar.emit(str(self.numLinesRemoved)) # Выводим значение счетчика в строку индикатора очков

        self.newPiece() # Генерация первой фигурки
        self.timer.start(Board.Speed, self) # Запускаем таймер цикла (описан ниже)


    def pause(self): # Пауза
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused # Switcher для вызова по кнопке "P"

        if self.isPaused:
            self.timer.stop() # Приостанавливаем таймер
            self.msg2Statusbar.emit("paused") # В строке счета пишем значение паузы

        else:
            self.timer.start(Board.Speed, self) # Запускаем счетчик
            self.msg2Statusbar.emit(str(self.numLinesRemoved)) # Возвращаем счет на свое место

        self.update() # Обновляем окно


    def paintEvent(self, event): # А вот тут начинаются рисовалки)))))) Каждый раз зарисовываем поле заново
        painter = QPainter(self)
        rect = self.contentsRect() # Возвращаем рабочую область внутри окна

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight() # Определяем пространство
        # нижнего колонтитула

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1) # Проверяем, есть ли здесь тетрамино

                if shape != Tetrominoe.NoShape: # Если в клетке есть тетрамино
                    self.drawSquare(painter, # Рисуем прямоугольничег
                        rect.left() + j * self.squareWidth(), # Оступ слева
                        boardTop + i * self.squareHeight(), # Отступ снизу
                        shape) # Передаем вид тетраминошки

        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(4): # В любой из наших тетрамино 4 квадратика

                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())


    def keyPressEvent(self, event): # Работаем с горячими клавишами программы
        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            # Проверка, запущена ли программа и не стоит ли она на паузе
            super(Board, self).keyPressEvent(event)
            return

        key = event.key() # Что мы нажали

        if key == Qt.Key_P: # Пауза
            self.pause()
            return

        if self.isPaused: # Анблок паузы
            return

        elif key == Qt.Key_Left: # Сдвиг по X влево
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right: # Вправо
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down: # поворот вокруг центральной (главной) тетрамино
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up: # Влево
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space: # Мгновенное падение
            self.dropDown()

        elif key == Qt.Key_D: # Ускоренное падение
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event) # повторяем действия


    def timerEvent(self, event): # Сопсна, ранее многоупоминаемый ЦИКЛ ИГРЫ
        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine: # Если тетрамино остановилась
                self.isWaitingAfterLine = False
                self.newPiece() # Спавним еще одну тетрамино
            else:
                self.oneLineDown() # Опускаем на линию вниз

        else:
            super(Board, self).timerEvent(event) # повторяем цикл игры


    def clearBoard(self):
        for i in range(Board.BoardHeight * Board.BoardWidth): # проходится по всем позициям
            # К сведению: доска представлена одномерным масивом, где все позиции пронумерованы
            # слева на право снизу вверх
            self.board.append(Tetrominoe.NoShape) # Обнуляет позицию [i] (опустошает)


    def dropDown(self): # Высчет окончания падения в случае space_key
        newY = self.curY # Берем положение на данный момент

        while newY > 0: # Цикл ускоренного падения (исключаем анимацию падения и задержку)

            if not self.tryMove(self.curPiece, self.curX, newY - 1): # Проверяем, можем ли опустить еще ниже
                break

            newY -= 1 # Если можем - спускаем на 1 клетку

        self.pieceDropped() # Констатируем остановку если не можем еще опустить


    def oneLineDown(self): # Спуск на одну строку вниз, нужен для вставки между задержкой в падении
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()


    def pieceDropped(self): # Место остановки тетрамино
        for i in range(4): # Проходимся по частям тетрамино и сохраняем в Tetris.board их положение

            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines() # Проверяем на занятость линий

        if not self.isWaitingAfterLine: # Если ничего не падает,
            self.newPiece() # спавним новую фигурку


    def removeFullLines(self):
        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight): # Считаем кол-во квадратиков в каждой строчке

            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape: # Кол-во квадратиков для этой строчки
                    n = n + 1

            if n == 10: # Длинна строки тетриса равна 10, => n == 10 начит вся строка полная
                rowsToRemove.append(i) # запоминаем для удаления

            # Удаляю не сразу т.к. потом придется еще двигать все остальные тетрамино вниз

        rowsToRemove.reverse() # Если в прямом порядке, то при удалении сразу нескольких строк
        # удаляется нижняя, все сдвигается вниз, а значит и номера каждой строки становятся меньше на 1 ¯\_(ツ)_/¯
        # Ниже можно увидеть, что все двигается вниз на одну клетку, и если мы сдвинем не в порядке сверху вниз
        # Может возникнуть эта ошибка


        for m in rowsToRemove: # Начинаем удалять
            for k in range(m, Board.BoardHeight): # Все что выше этой линии двигаем вниз
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1)) # двигаем вниз

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:

            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()


    def newPiece(self):
        self.curPiece = Shape()
        self.curPiece.setRandomShape() # Выбираем рандомом одну из тетрамино
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()
        # Для обеих строк: выбираем точку для спавна тетрамино

        if not self.tryMove(self.curPiece, self.curX, self.curY): # Если заспавнить тетрамино нельзя - бан

            self.curPiece.setShape(Tetrominoe.NoShape) # Говорим о не создании тетрамино
            self.timer.stop() # Останавливаем таймер
            self.isStarted = False # Останавливаем игру (отключаем клавиши взаимодействия)
            self.msg2Statusbar.emit("Game over") # Сигнализируем об окончании игры
            global set_score
            set_score = self.numLinesRemoved



    def tryMove(self, newPiece, newX, newY): # Проверка возможности хода
        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                # Остановка, если достигли края доски
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                # Остановка, если преградой выступают уже стоящие фигуры
                return False

        self.curPiece = newPiece # Изменяем место согласно запросу (так же и две следующие строки кода)
        self.curX = newX
        self.curY = newY
        self.update() # Обновляем окно

        return True


    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00] # Тупо цвета

        color = QColor(colorTable[shape]) # сolor - экземпляр объекта, с помощью которого мы будем красить
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
            self.squareHeight() - 2, color) # Красим область квадратика

        painter.setPen(color.lighter()) # 1
        painter.drawLine(x, y + self.squareHeight() - 1, x, y) # 2
        painter.drawLine(x, y, x + self.squareWidth() - 1, y) # 3
        # К 1,2,3 строкам: верхнюю и левую сторону высвечиваем

        painter.setPen(color.darker()) #4
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1) # 5
        painter.drawLine(x + self.squareWidth() - 1,
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1) # 6
        # К 4,5,6 строкам: нижнюю и левую затемняем
        # Ко всем 6 строкам: так мы создаем эфект света с левого верхнего угла, что дает нам ощущение объема
        # и зрительно разделяет члены фигур


class Tetrominoe(object): # Тупа пронумеровали тетрамино
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    ) # Положения квадратиков в фигурках, где (0, 0) - главный сектор (от него мы считаем координаты
      # фигуры на поле)

    def __init__(self):

        self.coords = [[0,0] for i in range(4)] # Объявляем новую фигурку (пока все координаты пустые)
        self.pieceShape = Tetrominoe.NoShape # Фигурка не имеет позиции

        self.setShape(Tetrominoe.NoShape) # Фигурка не имеет типа


    def shape(self):
        return self.pieceShape # Возвращает положение фигурки на доске


    def setShape(self, shape): # Дает фигурке позицию на доске
        table = Shape.coordsTable[shape] # -||-

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j] # Передаем каждому сегменту его положение на доске

        self.pieceShape = shape


    def setRandomShape(self): # Случайным образом даем фигурке ее тип
        self.setShape(random.randint(1, 7))


    def x(self, index): # Возвращает фактическое положение по X
        return self.coords[index][0]


    def y(self, index): # Возвращает фактическое положение по Y
        return self.coords[index][1]


    def setX(self, index, x): # Задает фактическое положение по X
        self.coords[index][0] = x


    def setY(self, index, y): # Задает фактическое положение по Y
        self.coords[index][1] = y


    def minX(self): # Возвращает крайнюю левую точку по X
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m


    def maxX(self): # Возвращает крайнюю правую точку по X
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m


    def minY(self): # Возвращает крайнюю верхнюю точку по Y
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m


    def maxY(self): # Возвращает крайнюю нижнюю точку по Y
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m


    def rotateLeft(self):
        if self.pieceShape == Tetrominoe.SquareShape: # Зачем ее вращать, если она квадратная?
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4): # Для каждого из 4 сегментов

            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result


    def rotateRight(self):
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):

            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    app.exec()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    # Время на момент завершения программы
    subject = "Tetris"
    statistic_db.times(start_time, set_score, now, subject)