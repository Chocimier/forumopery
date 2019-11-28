#coding: utf8

import sqlite3, bbcode, cgi

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
	def prosty(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if wnetrze:
			return '<{znacznik}>{wnetrze}</{znacznik}>'.format(**locals())
		else:
			return ''

	def barwa(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty and wnetrze:
			return '<span style="color:{argumenty[znacznik]};">{wnetrze}</span>'.format(**locals())
		else:
			return wnetrze

	def lacze(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty:
			adres = argumenty[znacznik]
			wnetrze = wnetrze or adres
			return '<a href="{adres}">{wnetrze}</a>'.format(**locals())
		else:
			return wnetrze

	def obraz(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty and wnetrze:
			adres = argumenty[znacznik]
			return '<img src="{adres}" alt="{wnetrze}" />'.format(**locals())
		else:
			return wnetrze

	def cytat(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if znacznik in argumenty:
			autor = argumenty[znacznik]
			wynik = '<p>{autor} napisał(a):</p><blockquote>{wnetrze}</blockquote>'
		elif wnetrze:
			wynik = '<blockquote>{wnetrze}</blockquote>'
		else:
			wynik = ''
		return wynik.format(**locals())

	def kod(znacznik, wnetrze, argumenty, rodzic, otoczenie):
		if wnetrze:
			return '<pre>{wnetrze}</pre>'.format(**locals())
		else:
			return ''

	a = bbcode.Parser(install_defaults=False, replace_cosmetic=False)
	a.add_formatter('b', prosty)
	a.add_formatter('i', prosty)
	a.add_formatter('u', prosty)
	a.add_formatter('s', prosty)
	a.add_formatter('color', barwa)
	a.add_formatter('url', lacze)
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

def zencjuj(**kwargs):
	return { k: cgi.escape(v) for k, v in kwargs.items() }
