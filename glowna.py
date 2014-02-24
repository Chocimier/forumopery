# coding: utf8

import sqlite3
from narzedzia import szablon

class Glowna:
	def dzialy(self):
		zapytanie = 'SELECT * FROM dzialy ORDER BY nr_dzialu ASC;'
		self.k.execute(zapytanie)
		return self.k.fetchall()

	def oHTMLowany(self):
		dzialy = ""
		for nr_dzialu, nazwa_dzialu, opis_dzialu in self.dzialy():
			dzialy += self.szablon_dzialu.format(nr=nr_dzialu, nazwa=nazwa_dzialu.encode('utf8'), opis=opis_dzialu.encode('utf8'))
		return self.szablon.format(dzialy=dzialy)


	def strona(self):
		return self.oHTMLowany()

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('główna')
		self.szablon_dzialu = szablon('główna-dział')