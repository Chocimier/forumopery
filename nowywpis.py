# coding: utf8

import sqlite3, time
from narzedzia import szablon, wiarygodny, oprawWpis
from watek import Watek
from bottle import redirect
from hashlib import sha384

class NowyWpis:
	def dodajWpis(self, uzytkownik, tresc, nr_watku):
		zapytanie = 'SELECT zamknieto FROM watki WHERE nr_watku = ? ;'
		zmienne = (nr_watku,)
		self.k.execute(zapytanie, zmienne)
		odpowiedz = self.k.fetchone()
		if odpowiedz == None:
			wynik = (False, 'nie ma takiego wątku')
		elif odpowiedz[0] == 1:
			wynik = (False, 'wątek jest zamknięty')
		else:
			zapytanie = 'INSERT INTO wpisy(autor, tresc, nr_watku, data_wyslania) VALUES (?, ?, ?, ?);'
			zmienne = (uzytkownik, tresc, nr_watku, int(time.strftime(format_czasu_w_bazie)))

			print(zapytanie, zmienne)

			k.execute(zapytanie, zmienne)
			baza.commit()
			wynik = (True, 'dodano wpis')
		return wynik

	def strona(self, dane):
		uzytkownik = dane['ksywka'].decode('utf8')
		skrot_hasla = sha384(dane['hasło'].decode('utf8')).hexdigest()

		swoj, dlaczego_wrog = wiarygodny(uzytkownik, skrot_hasla)
		if swoj:
			tresc = oprawWpis(dane['treść'].decode('utf8'))
			nr_watku = int(dane['wątek'])
			dodano, dlaczego_nie_dodano = self.dodajWpis(uzytkownik, tresc, nr_watku)
			if dodano:
				redirect('/wątek.py?{}'.format(nr_watku))
			else:
				return dlaczego_nie_dodano
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
