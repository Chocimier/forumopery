#coding: utf8

import sqlite3, json

class Wnioski:
	def strona(self):
		zapytanie = 'SELECT ksywka, kod FROM odzyskiwanie;'
		self.k.execute(zapytanie)
		return str(json.dumps(self.k.fetchall()))

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forowicze.sqlite')
		self.k = self.baza.cursor()
