# coding: utf8

import sqlite3
from narzedzia import szablon
from bottle import redirect

class Wpis:
	def strona(self, nr_wpisu):
		zapytanie = 'SELECT nr_watku FROM wpisy WHERE nr_wpisu=?;'
		zmienne = (nr_wpisu,)
		watek = self.k.execute(zapytanie, zmienne).fetchone()
		if watek:
			redirect('/wątek/{}#{}'.format(watek[0], nr_wpisu))
		else:
			return self.brak()

	def brak(self):
		return self.szablon_brak

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon_brak = szablon('wpis-brak')
