# coding: utf8

import sqlite3

class Szukaj:
	def szukaj(self, wyraz):
		zapytanie = 'SELECT wpisy.nr_watku, watki.tytul, watki.zamknieto FROM wpisy LEFT JOIN watki ON wpisy.nr_watku = watki.nr_watku WHERE wpisy.tresc MATCH ?;'
		zmienne = (wyraz,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchall()

	def oHTMLowany(self, wyraz):
		nazwa_dzialu = 'Wyniki wyszukiwania „{}”'.format(wyraz)
		watki = ""
		for nr_watku, tytul, zamknieto in self.szukaj(wyraz):
			oznaczenie_zamknieto = '[zamknięty] ' if zamknieto else ''
			watki += self.szablon_watku.format(nr=nr_watku, tytul=tytul.encode('utf8'), zamknieto=oznaczenie_zamknieto)
		return self.szablon.format(nazwa=nazwa_dzialu.encode('utf8'), watki=watki)

	def strona(self, wyraz):
		return self.oHTMLowany(wyraz)

	def brak(self):
		return szablon_brak

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = open('szablony/dział').read()
		self.szablon_watku = open('szablony/dział-wątek').read()
		self.szablon_brak = open('szablony/dział-brak').read()
		return None
