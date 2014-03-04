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
from szukaj import Szukaj

@route('/')
def glowna():
	return Glowna().strona()

@route('/forum/<id_:int>/')
@route('/forum/<id_:int>')
def forum(id_):
	return Dzial().strona(id_)

@route('/temat/<id_:int>/')
@route('/temat/<id_:int>')
def temat(id_):
	return Watek().strona(id_)

#nowy wątek
@route('/forum/<id_dzialu:int>/nowy/')
@route('/forum/<id_dzialu:int>/nowy')
def nowy_temat(id_dzialu):
	return NowyWatek().strona(id_dzialu)

#nowa odpowiedź
@post('/forum/<id_watku:int>/nowy/')
@post('/forum/<id_watku:int>/nowy')
def nowa_odpowiedz_post():
	return NowyWpis().strona(request.forms)

@route('/szukaj/')
@route('/szukaj')
def rejestracja():
	return Szukaj().strona({})

@route('/rejestracja/')
@route('/rejestracja')
def rejestracja():
	return Rejestracja().strona({})

#post
@post('/rejestracja/')
@post('/rejestracja')
def rejestracja():
	return Rejestracja().strona(request.forms)

@route('/wpisy.atom')
def rss_atom():
	response.content_type='application/atom+xml'
	return Kanal().strona(request.environ.get('PATH_INFO'))

@route('/wnioski/')
@route('/wnioski')
def wnioski():
	return Wnioski().strona()

@route('/<adres:path>')
def blad_404(adres):
	sciezka = request.environ.get('PATH_INFO')
	#TODO: użyć szablonu 404.html
	return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'

@post('/<adres:path>')
def blad_404_post(adres):
	sciezka = request.environ.get('PATH_INFO')
	#TODO: użyć szablonu 404.html
	return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'


application = default_app()
