# coding: utf8

import sqlite3
from narzedzia import szablon

class Dzial:
	def nazwaDzialu(self, nr_dzialu):
		zapytanie = 'SELECT nazwa_dzialu FROM dzialy WHERE nr_dzialu=?'
		zmienne = (nr_dzialu,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchone()[0]

	def watki(self, nr_dzialu):
		zapytanie = 'SELECT nr_watku, tytul, zamknieto, wyswietlen FROM watki WHERE nr_dzialu=? ORDER BY nr_watku DESC;'
		zmienne = (nr_dzialu,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchall()

	def oHTMLowany(self, nr_dzialu):
		nazwa_dzialu = self.nazwaDzialu(nr_dzialu)
		watki = ""
		for nr_watku, tytul, zamknieto, wyswietlen in self.watki(nr_dzialu):
			oznaczenie_zamknieto = '[zamknięty] ' if zamknieto else ''
			watki += self.szablon_watku.format(nr=nr_watku, tytul=tytul.encode('utf8'), zamknieto=oznaczenie_zamknieto, wyswietlen=wyswietlen)
		return self.szablon.format(nazwa=nazwa_dzialu.encode('utf8'), watki=watki, nr_dzialu=nr_dzialu)

	def strona(self, nr_dzialu):
		zapytanie = 'SELECT nr_dzialu FROM dzialy WHERE nr_dzialu=?;'
		zmienne = (nr_dzialu,)
		self.k.execute(zapytanie, zmienne)
		if self.k.fetchone() != None:
			return self.oHTMLowany(nr_dzialu)
		else:
			return self.brak()

	def brak(self):
		return self.szablon_brak

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('dział')
		self.szablon_watku = szablon('dział-wątek')
		self.szablon_brak = szablon('dział-brak')
