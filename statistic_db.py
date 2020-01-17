import sqlite3
import shutil
import csv


def times(start_time, set_score, now, subject):

	now = hms_to_sec(now) # Перевод в секунды
	start_time = hms_to_sec(start_time)

	InGameTime = now - start_time # Время проведенное в игре
	InGameTime = sec_to_hms(InGameTime) # Перевод из секунд в часы/минуты/секунды


	con = sqlite3.connect("users_statistic.db")
	cur = con.cursor()

	user = cur.execute("""SELECT * FROM users
						WHERE id = 0 """).fetchall()[0][1]

	score = return_status(subject)[0]
	# Сущесчтвует ли статистика по этому пользователю в этой игре
	# Возвращение существующих статистических данных

	if not score:
		if set_score > 5:
			wl = 'w'
		else:
			wl = 'l'

		cur.execute("""INSERT INTO statistic(user, game, InGameTime, score, WLS, history)
					VALUES(@a, @game, @b, @c, @d, @e)""", (user, subject, InGameTime, set_score, 0.0, wl))
		# Если статистики не было, создается новая строка статистики в БД
	else:
		lastGameTime = hms_to_sec(score[0][2])
		InGameTime = now - start_time + lastGameTime
		InGameTime = sec_to_hms(InGameTime)
		
		
		wl = str(list(score[0])[5])


		if set_score >= 5:
			wl += 'w'
		else:
			wl += 'l'


		if 'w' in wl and 'l' in wl:
			wr = wl.count('w') / wl.count('l')
		else:
			wr = 0.0


		cur.execute("""UPDATE statistic
						SET InGameTime = @subject
						WHERE (user = @name) and (game = @game) """, (InGameTime, user, subject))

		cur.execute("""UPDATE statistic
						SET WLS = @subject
						WHERE (user = @name) and (game = @game) """, (wr, user, subject))

		cur.execute("""UPDATE statistic
						SET history = @subject
						WHERE (user = @name) and (game = @game) """, (wl, user, subject))
		print(wl)

		if set_score > score[0][3]:
			cur.execute("""UPDATE statistic
							SET score = @subject
							WHERE (user = @name) and (game = @game) """, (set_score, user, subject))

	con.commit()
	cur.close()
	con.close()


def update(object, subject, user):
	cur.execute("""UPDATE statistic
				SET @object = @subject
				WHERE (user = @name) and (game = "Tetris") """, (object, subject, user))


def hms_to_sec(object): # Перевод из Hours Minutes Seconds в Seconds
	formated = [int(i) for i in object.split(':')]
	result = formated[0] * 60 * 60 + formated[1] * 60 + formated[2]
	return result


def sec_to_hms(object): # Перевод из Seconds в Hours Minutes Seconds
	result = ':'.join([str(object // 3600),
						   str(object % 3600 // 60),
						   str(object % 60)])
	return result

def return_status(subject): # Возвращает текущего пользователя и всю информацию о нем
	con = sqlite3.connect("users_statistic.db")
	cur = con.cursor()
	print(1)
	user = cur.execute("""SELECT * FROM users
						WHERE id = 0 """).fetchall()[0][1]
	print(user)
	log = cur.execute("""SELECT * FROM statistic
							WHERE (user = @a) and (game = @b )""", (user, subject)).fetchall()
	print(3)
	return log, user


def csv_return():
	con = sqlite3.connect("users_statistic.db")
	cur = con.cursor()

	user = cur.execute("""SELECT * FROM users
						WHERE id = 0 """).fetchall()[0][1]

	data = cur.execute("""SELECT * FROM statistic
							WHERE user = @a""", (user,)).fetchall()

	shutil.copyfile("original.csv", "{}_statistic.csv".format(user))
	path = "{}_statistic.csv".format(user)

	with open(path, "w", newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter=';')
		writer.writerow(["Ваши игры:", "Время, проведенное в игре:", "Счет:", "Win Rate:", "История побед:"])
		for line in data:
			writer.writerow(line[1:])


def csv_load(name):
	con = sqlite3.connect("users_statistic.db")
	cur = con.cursor()

	user = cur.execute("""SELECT * FROM users
						WHERE id = 0 """).fetchall()[0][1]
	print(user)


	k = 0

	with open('{}'.format(name), encoding="windows-1251") as csvfile:
		reader = csv.reader(csvfile, delimiter=';', quotechar='"')

		for index, row in enumerate(reader):
			if index > 10:
				break
			if index == 0:
				continue
			subject = row[0]
			InGameTime = row[1]
			set_score = row[2]
			wr = row[3]
			wl = row[4]

			con = sqlite3.connect("users_statistic.db")
			cur = con.cursor()

			data = cur.execute("""SELECT * FROM statistic
									WHERE (user = @a) and (game = @b)""", (user, subject)).fetchall()
			if not data:
				cur.execute("""INSERT INTO statistic(user, game, InGameTime, score, WLS, history)
									VALUES(@a, @game, @b, @c, @d, @e)""",
							(user, subject, InGameTime, set_score, 0.0, wl))

			cur.execute("""UPDATE statistic
							SET InGameTime = @subject
							WHERE (user = @name) and (game = @game) """, (InGameTime, user, subject))

			cur.execute("""UPDATE statistic
							SET WLS = @subject
							WHERE (user = @name) and (game = @game) """, (wr, user, subject))

			cur.execute("""UPDATE statistic
							SET history = @subject
							WHERE (user = @name) and (game = @game) """, (wl, user, subject))

			cur.execute("""UPDATE statistic
							SET score = @subject
							WHERE (user = @name) and (game = @game) """, (set_score, user, subject))

			con.commit()
			cur.close()
			con.close()