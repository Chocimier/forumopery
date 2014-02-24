# coding: utf8

import sqlite3, narzedzia
from time import strftime, strptime

class Watek:
	def wpisy(self, nr_watku):
		zapytanie = 'SELECT autor, tresc, data_wyslania FROM wpisy WHERE nr_watku=? ORDER BY data_wyslania ASC;'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchall()

	def oWatku(self, nr_watku):
		zapytanie = 'SELECT tytul, zamknieto, powod_zamkniecia FROM watki WHERE nr_watku=?'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchone()

	def oDzialeWatku(self, nr_watku):
		zapytanie = 'SELECT watki.nr_dzialu, dzialy.nazwa_dzialu FROM watki LEFT JOIN dzialy ON watki.nr_dzialu = dzialy.nr_dzialu WHERE watki.nr_watku = ?;'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchone()

	def oHTMLowany(self, nr_watku):
		tytul, zamknieto, powod_zamkniecia = self.oWatku(nr_watku)
		nr_dzialu, nazwa_dzialu = self.oDzialeWatku(nr_watku)
		oZamknieciu = '' if not zamknieto else self.szablon_zamkniety.format(powod=powod_zamkniecia)
		wpisy = ""
		for autor, tresc, czas_wyslania in self.wpisy(nr_watku):
			czas_krotka = strptime(str(czas_wyslania), "%Y%m%d%H%M%S")
			czas_ladnie = strftime('{dzien[%w]} %d {miesiac[%m]} %Y o %H<sup class=minuta>%M</sup>', czas_krotka).format(miesiac=narzedzia.odmienione_miesiace, dzien=narzedzia.odmienione_dni)
			czas_iso = strftime('%Y-%m-%d %H:%M', czas_krotka)
			wpisy += self.szablon_wpisu.format(autor=autor.encode('utf8'), tresc=tresc.encode('utf8'), czas_iso=czas_iso, czas_ladnie=czas_ladnie)
		return self.szablon.format(tytul=tytul.encode('utf8'), nazwa_dzialu=nazwa_dzialu.encode('utf8'), nr_dzialu=nr_dzialu, wpisy=wpisy, zamkniety=oZamknieciu)

	def strona(self, nr_watku):
		zapytanie = 'SELECT nr_watku FROM watki WHERE nr_watku=?;'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		if self.k.fetchone() != None:
			return self.oHTMLowany(nr_watku)
		else:
			return self.brak()

	def brak(self):
		return self.szablon_brak

	def __init__(self):
		self.baza = sqlite3.connect('forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = open('szablony/wątek.html').read()
		self.szablon_wpisu = open('szablony/wątek-wpis.html').read()
		self.szablon_zamkniety = open('szablony/wątek-zamknięty.html').read()
		self.szablon_brak = open('szablony/wątek-brak.html').read()
