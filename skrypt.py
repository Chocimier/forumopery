#!/usr/bin/env python2
#coding: utf8

from bottle import default_app, route, request, post, response, abort

from watek import Watek
from dzial import Dzial
from glowna import Glowna
from nowywpis import NowyWpis
from rejestracja import Rejestracja
from nowywatek import NowyWatek
from kanal import Kanal
from szukaj import Szukaj
from wpis import Wpis

@route('/')
def glowna():
	return Glowna().strona()

@route('/<adres>')
@route('/<adres>/<nr:int>')
def podstrona(adres, nr=0):
	sciezka = request.environ.get('PATH_INFO')
	pelny_adres = request.url
	if sciezka.startswith('/wątek/'):
		return Watek().strona(nr)
	elif sciezka.startswith('/dział/'):
		return Dzial().strona(nr)
	elif sciezka.startswith('/wpis/'):
		return Wpis().strona(nr)
	elif sciezka == '/rejestracja':
		return Rejestracja().strona({})
	elif sciezka == '/nowy_wątek':
		return NowyWatek().strona(request.query.dzial)
	elif sciezka == '/szukaj':
		return Szukaj().strona(request.query.q)
	elif sciezka == '/wpisy.atom':
		response.content_type='application/atom+xml; charset=utf-8'
		return Kanal().strona(sciezka, pelny_adres)
	else:
		abort(404, 'Nie ma takiej strony')
		return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'

@route('/zasoby/<adres>')
def zasoby(adres):
	return static_file(adres, root='/home/forumopery/forumopery/zasoby/')

@post('/<adres>')
def post(adres):
	sciezka = request.environ.get('PATH_INFO')
	if sciezka == '/nowywpis':
		return NowyWpis().strona(request.forms)
	elif sciezka == '/rejestracja':
		return Rejestracja().strona(request.forms)
	else:
		abort(404, 'Nie ma takiej strony')
		return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'


application = default_app()
