# coding: utf8

import sqlite3
from narzedzia import wolnaKsywka, niezarejestrowany, szablon
from bottle import redirect
from hashlib import sha384

class Rejestracja:
	def rejestruj(uzytkownik, skrot_hasla):
		zapytanie = 'INSERT INTO uzytkownicy(ksywka, haslo, zarejestrowany) VALUES (?, ?, ?);'
		zmienne = (uzytkownik, skrot_hasla, 1)
		self.k.execute(zapytanie, zmienne)
		self.baza.commit()

	def strona(self, dane):
		try:
			uzytkownik = dane['ksywka'].decode('utf8')
		except KeyError:
			return self.szablon.format(ksywka='', wiadomosc='Miło, że tu przybyłeś.')
		try:
			haslo = dane['hasło'].decode('utf8')
			skrot_hasla = sha384(haslo).hexdigest()
		except KeyError:
			return self.szablon.format(ksywka=uzytkownik, wiadomosc='Nie podałeś hasła')

		if uzytkownik == '': return self.szablon.format(ksywka='', wiadomosc='Miło, że tu przybyłeś.')
		if haslo == '': return self.szablon.format(ksywka=uzytkownik, wiadomosc='Nie podałeś hasła')
		del haslo

		if wolnaKsywka(uzytkownik):
			self.rejestruj(uzytkownik, skrot_hasla)
			return self.szablon.format(ksywka=uzytkownik, wiadomosc='Zarejestrowałeś się jako {}. Zapraszam <a href=/>do dyskusji</a>.'.format(uzytkownik))
		elif niezarejestrowany(uzytkownik):
			return self.szablon.format(ksywka=uzytkownik, wiadomosc='Rejestracja pod ksywkami z forum My Opera nie jest obecnie możliwa.')
		else:
			return self.szablon.format(ksywka=uzytkownik, wiadomosc='Ksywka {} jest już zajęta.'.format(uzytkownik))

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forowicze.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('rejestracja')
