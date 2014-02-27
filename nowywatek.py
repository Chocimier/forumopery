# coding: utf8

import sqlite3
from narzedzia import szablon

class NowyWatek:
	def dzialy(self, nr_dzialu):
		zapytanie = 'SELECT nazwa_dzialu, nr_dzialu FROM dzialy'
		wynik = ""
		self.k.execute(zapytanie)
		for nazwa_dzialu, nr in self.k.fetchall():
			try:
				wynik += '<option value={nr_dzialu}{wybrany}>{nazwa_dzialu}</option>'.format(nazwa_dzialu=nazwa_dzialu.encode('utf8'), nr_dzialu=nr, wybrany=(' selected=selected' if int(nr)==int(nr_dzialu) else ''))
			except TypeError:
				print(dir(dane.items))
				raise TypeError
		return wynik
	def oHTMLowany(self, nr_dzialu):
		return self.szablon.format(dzialy=self.dzialy(nr_dzialu))

	def strona(self, nr_dzialu):
		return self.oHTMLowany(nr_dzialu)

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('nowy_wątek')
