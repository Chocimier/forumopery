#coding: utf8

import sqlite3, bbcode

odmienione_miesiace = ('',
		'stycznia', 'lutego', 'marca',
		'kwietnia', 'maja', 'czerwca',
		'lipca', 'sierpnia', 'września',
		'października', 'listopada', 'grudnia')
odmienione_dni = ('w niedzielę', 'w poniedziałek', 'we wtorek', 'w środę', 'we czwartek', 'w piątek', 'w sobotę')
katalogSzablonow = '/home/forumopery/forumopery/szablony/'
format_czasu_w_bazie = '%Y%m%d%H%M%S'
format_czasu_iso = '%Y-%m-%dT%H:%M:%SZ'

def szablon(nazwa, rozszerzenie='html'):
	return open(katalogSzablonow + nazwa + '.' + rozszerzenie).read()

def wiarygodny(uzytkownik, skrot_hasla):
	baza = sqlite3.connect('/home/forumopery/forowicze.sqlite')
	k = baza.cursor()

	zapytanie = 'SELECT ksywka, haslo FROM uzytkownicy WHERE ksywka = ?'
	zmienne = (uzytkownik,)
	k.execute(zapytanie, zmienne)
	odpowiedz = k.fetchone()

	if odpowiedz == None or not odpowiedz[1]:
		return (False, 'Nie zarejestrowałeś się, {}'.format(uzytkownik))
	elif odpowiedz[1] != skrot_hasla:
		return (False, 'Niepoprawne hasło')
	else:
		return (True, '')

def oprawWpis(tresc):
	def prosty(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if wnętrze:
			return '<{znacznik}>{wnętrze}</{znacznik}>'.format(**locals())
		else:
			return ''

	def barwa(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty and wnętrze:
			return '<span style="color:{argumenty[znacznik]};">{wnętrze}</span>'.format(**locals())
		else:
			return wnętrze

	def łącze(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty:
			adres = argumenty[znacznik]
			wnętrze = wnętrze or adres
			return '<a href="{adres}">{wnętrze}</a>'.format(**locals())
		else:
			return wnętrze

	def obraz(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty and wnętrze:
			adres = argumenty[znacznik]
			return '<img src="{adres}" alt="{wnętrze}" />'.format(**locals())
		else:
			return wnętrze

	def cytat(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty:
			autor = argumenty[znacznik]
			wynik = '<p>{autor} napisał(a):</p><blockquote>{wnętrze}</blockquote>'
		elif wnętrze:
			wynik = '<blockquote>{wnętrze}</blockquote>'
		else:
			wynik = ''
		return wynik.format(**locals())

	def kod(znacznik, wnętrze, argumenty, rodzic, otoczenie):
		if wnętrze:
			return '<pre>{wnętrze}</pre>'.format(**locals())
		else:
			return ''

	a = bbcode.Parser(install_defaults=False, replace_cosmetic=False)
	a.add_formatter('b', prosty)
	a.add_formatter('i', prosty)
	a.add_formatter('u', prosty)
	a.add_formatter('s', prosty)
	a.add_formatter('color', barwa)
	a.add_formatter('url', łącze)
	a.add_formatter('img', obraz)
	a.add_formatter('quote', cytat)
	a.add_formatter('code', kod)

	return (a.format(tresc))

def wolnaKsywka(uzytkownik):
	baza = sqlite3.connect('/home/forumopery/forowicze.sqlite')
	k = baza.cursor()

	zapytanie = 'SELECT ksywka FROM uzytkownicy WHERE ksywka = ?'
	zmienne = (uzytkownik,)
	k.execute(zapytanie, zmienne)
	odpowiedz = k.fetchone()

	return odpowiedz == None

def niezarejestrowany(uzytkownik):
	baza = sqlite3.connect('/home/forumopery/forowicze.sqlite')
	k = baza.cursor()

	zapytanie = 'SELECT zarejestrowany FROM uzytkownicy WHERE ksywka = ?'
	zmienne = (uzytkownik,)
	k.execute(zapytanie, zmienne)
	odpowiedz = k.fetchone()

	return False if odpowiedz==None else not odpowiedz[0]
