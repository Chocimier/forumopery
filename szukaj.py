#coding: utf8

import sqlite3
import six
from narzedzia import szablon

# baza sqlite z wyszukiwaniem pełnotekstowym, kluczem głownym i obcym wg pomysłu Žarko Gajicia:
# http://zarko-gajic.iz.hr/sqlite-referential-integrity-with-full-text-search-virtual-tables-used-in-a-delphi-application/

class Szukaj:
	def szukaj(self, wyraz):
		zapytanie = 'SELECT wpisy.nr_wpisu, wpisy.nr_watku, watki.tytul, watki.zamknieto, watki.wyswietlen FROM wpisy JOIN watki ON wpisy.nr_watku = watki.nr_watku WHERE wpisy.tresc MATCH ?;'
		zmienne = (wyraz,)
		self.k.execute(zapytanie, zmienne)
		return self.k.fetchall()

	def oHTMLowany(self, wyraz):
		nazwa = 'Wyniki wyszukiwania „{}”'.format(wyraz)
		watki = ''
		for nr_wpisu, nr_watku, tytul, zamknieto, wyswietlen in self.szukaj(wyraz):
			zamknieto = '[zamknięty] ' if zamknieto else ''
			nr='{}#{}'.format(nr_watku, nr_wpisu)
			tytul=six.ensure_str(tytul)
			watki += self.szablon_watku.format(**locals())
		nr_dzialu=0
		return self.szablon.format(**locals())

	def strona(self, wyraz):
		return self.oHTMLowany(wyraz)

	def __init__(self):
		self.baza = sqlite3.connect('/home/forumopery/forum.sqlite')
		self.k = self.baza.cursor()
		self.szablon = szablon('dział')
		self.szablon_watku = szablon('dział-wątek')
