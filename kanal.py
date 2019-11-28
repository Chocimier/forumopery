#coding: utf8

import sqlite3
from narzedzia import zencjuj, szablon, format_czasu_w_bazie, format_czasu_iso
from time import strptime, strftime

class Kanal:
	def najnowsze(self):
		zapytanie = 'SELECT nr_watku, tresc, autor, data_wyslania, nr_wpisu FROM wpisy ORDER BY data_wyslania DESC LIMIT 20;'
		self.k.execute(zapytanie)
		return self.k.fetchall()

	def tytulWatku(self, nr_watku):
		zapytanie = 'SELECT tytul FROM watki WHERE nr_watku=?;'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchone()[0]

	def oHTMLowany(self, adres, pelny_adres):
		wpisy = ""
		for nr_watku, tresc, autor, data_wyslania, nr_wpisu in self.najnowsze():
			czas_krotka = strptime(str(data_wyslania), format_czasu_w_bazie)
			czas_iso = strftime(format_czasu_iso, czas_krotka)
			adres_wpisu = 'http://forumopery.pythonanywhere.com/w%C4%85tek/{}#{}'.format(nr_watku, nr_wpisu)
			tytul = self.tytulWatku(nr_watku).encode('utf8')
			wpisy += self.szablon_wpisu.format(**zencjuj(autor=autor, tytul='{} odpowiada w wątku „{}”'.format(autor, tytul), czas_iso=czas_iso, wyroznik=adres_wpisu, strona=adres_wpisu, tresc=tresc.encode('utf8')))
		return self.szablon.format(tytul='Polskie forum Opery', czas_iso=strftime(format_czasu_iso), adres=pelny_adres, wpisy=wpisy)

	def strona(self, adres, pelny_adres):
		return self.oHTMLowany(adres, pelny_adres)

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('kanał', 'atom')
		self.szablon_wpisu = szablon('kanał-wpis', 'atom')
