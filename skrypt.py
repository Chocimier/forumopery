#!/usr/bin/env python2
#coding: utf8

from bottle import default_app, route, request, post, response

from watek import Watek
from dzial import Dzial
from glowna import Glowna
from nowywpis import NowyWpis
from rejestracja import Rejestracja
from wnioski import Wnioski
from nowywatek import NowyWatek
from kanal import Kanal

def liczba(napis):
	try:
		return int(napis)
	except ValueError:
		return -1

@route('/')
def glowna():
	sciezka = request.environ.get('PATH_INFO')
	if sciezka == '/':
		return Glowna().strona()

@route('/<adres>')
def podstrona(adres):
	sciezka = request.environ.get('PATH_INFO')
	zapytanie = request.environ.get('QUERY_STRING')
	if sciezka == '/wątek.py':
		return Watek().strona(liczba(zapytanie))
	elif sciezka == '/dział.py':
		return Dzial().strona(liczba(zapytanie))
	elif sciezka == '/rejestracja.py':
		return Rejestracja().strona({})
	elif sciezka == '/wnioski':
		return Wnioski().strona()
	elif sciezka == '/nowy_wątek.py':
		return NowyWatek().strona(request.query.dzial)
	elif sciezka == '/wpisy.atom':
		response.content_type='application/atom+xml'
		return Kanal().strona(request.environ.get('PATH_INFO'))
	else:
		return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'

@post('/<adres>')
def post(adres):
	sciezka = request.environ.get('PATH_INFO')
	if sciezka == '/nowywpis.py':
		return NowyWpis().strona(request.forms)
	elif sciezka == '/rejestracja.py':
		return Rejestracja().strona(request.forms)
	else:
		return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'


application = default_app()
