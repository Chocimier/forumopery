# coding: utf8

import sqlite3, time

odmienione_miesiace = ('',
		'stycznia', 'lutego', 'marca',
		'kwietnia', 'maja', 'czerwca',
		'lipca', 'sierpnia', 'września',
		'października', 'listopada', 'grudnia')
odmienione_dni = ('w niedzielę', 'w poniedziałek', 'we wtorek', 'w środę', 'we czwartek', 'w piątek', 'w sobotę')
katalogSzablonow = '/home/forumopery/szablony/'
format_czasu_w_bazie = '%Y%m%d%H%M%S'

def szablon(nazwa):
	return open(katalogSzablonow + nazwa + '.html').read()

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

def dodajWpis(uzytkownik, tresc, nr_watku):
	# tu się powinno sprawdzać hasło, chyba
	baza = sqlite3.connect('/home/forumopery/forum.sqlite')
	k = baza.cursor()
	zapytanie = 'INSERT INTO wpisy(autor, tresc, nr_watku, data_wyslania) VALUES (?, ?, ?, ?);'
	zmienne = (uzytkownik, tresc, nr_watku, int(time.strftime(format_czasu_w_bazie)))

	print(zapytanie, zmienne)

	k.execute(zapytanie, zmienne)
	baza.commit()

def oprawWpis(tresc):
	return tresc.replace('<', '&lt;').replace('>', '&gt;')

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
