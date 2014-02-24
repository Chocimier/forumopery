# coding: utf8

import sqlite3
from narzedzia import szablon, wiarygodny, dodajWpis
from watek import Watek
from bottle import redirect

class NowyWpis:
	def strona(self, dane):
		uzytkownik = dane['ksywka'].decode('utf8')
		haslo = dane['hasło'].decode('utf8')
		tresc = dane['treść'].decode('utf8')
		nr_watku = int(dane['wątek'])

		swoj, dlaczego_wrog = wiarygodny(uzytkownik, haslo)
		if swoj:
			dodajWpis(uzytkownik, tresc, nr_watku)
			redirect('/wątek.py?{}'.format(nr_watku))
		else:
			return dlaczego_wrog


	def brak(self):
		return self.szablon_brak

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('dział')
		self.szablon_watku = szablon('dział-wątek')
		self.szablon_brak = szablon('dział-brak')