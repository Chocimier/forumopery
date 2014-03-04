# coding: utf8

import sqlite3
from narzedzia import szablon, format_czasu_w_bazie, odmienione_miesiace, odmienione_dni
from time import strptime, strftime

class Glowna:
	def najnowsze(self):
		zapytanie = 'SELECT nr_watku, tresc, autor, data_wyslania, nr_wpisu FROM wpisy ORDER BY data_wyslania DESC LIMIT 8;'
		self.k.execute(zapytanie)
		return self.k.fetchall()

	def dzialy(self):
		zapytanie = 'SELECT * FROM dzialy ORDER BY nr_dzialu ASC;'
		self.k.execute(zapytanie)
		return self.k.fetchall()

	def oHTMLowany(self):
		dzialy = ""
		for nr_dzialu, nazwa_dzialu, opis_dzialu in self.dzialy():
			dzialy += self.szablon_dzialu.format(nr=nr_dzialu, nazwa=nazwa_dzialu.encode('utf8'), opis=opis_dzialu.encode('utf8'))
		najnowsze = ""
		for nr_watku, tresc, autor, data_wyslania, nr_wpisu in self.najnowsze():
			czas_krotka = strptime(str(data_wyslania), format_czasu_w_bazie)
			czas_ladnie = strftime('{dzien[%w]} %d {miesiac[%m]} %Y o %H<sup class=minuta>%M</sup>', czas_krotka).format(miesiac=odmienione_miesiace, dzien=odmienione_dni)
			czas_iso = strftime('%Y-%m-%d %H:%M', czas_krotka)
			najnowsze += self.szablon_wpisu.format(autor=autor, czas_iso=czas_iso, czas_ladnie=czas_ladnie, tresc=tresc.encode('utf8'), nr_watku=nr_watku, nr_wpisu=nr_wpisu)
		return self.szablon.format(naglowek=szablon('nagłówek'), dzialy=dzialy, najnowsze=najnowsze)


	def strona(self):
		return self.oHTMLowany()

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('główna')
		self.szablon_dzialu = szablon('główna-dział')
		self.szablon_wpisu = szablon('główna-wpis')
