# coding: utf8

import sqlite3
from time import strftime, strptime
from narzedzia import szablon, odmienione_miesiace, odmienione_dni, format_czasu_w_bazie, format_czasu_iso

class Watek:
	def wpisy(self, nr_watku):
		zapytanie = 'SELECT autor, tresc, data_wyslania, nr_wpisu FROM wpisy WHERE nr_watku=? ORDER BY data_wyslania ASC;'
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
		for autor, tresc, czas_wyslania, nr_wpisu in self.wpisy(nr_watku):
			czas_krotka = strptime(str(czas_wyslania), format_czasu_w_bazie)
			czas_ladnie = strftime('{dzien[%w]} %d {miesiac[%m]} %Y o %H<sup class=minuta>%M</sup>', czas_krotka).format(miesiac=odmienione_miesiace, dzien=odmienione_dni)
			czas_iso = strftime(format_czasu_iso, czas_krotka)
			wpisy += self.szablon_wpisu.format(autor=autor.encode('utf8'), tresc=tresc.encode('utf8'), czas_iso=czas_iso, czas_ladnie=czas_ladnie, nr_wpisu=nr_wpisu)
		return self.szablon.format(tytul=tytul.encode('utf8'), nazwa_dzialu=nazwa_dzialu.encode('utf8'), nr_dzialu=nr_dzialu, wpisy=wpisy, zamkniety=oZamknieciu, nr_watku=nr_watku)

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
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('wątek')
		self.szablon_wpisu = szablon('wątek-wpis')
		self.szablon_zamkniety = szablon('wątek-zamknięty')
		self.szablon_brak = szablon('wątek-brak')
