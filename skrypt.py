#!/usr/bin/env python2
#coding: utf8

from bottle import default_app, route, request

from watek import Watek
from dzial import Dzial
from glowna import Glowna

def liczba(napis):
	try:
		return int(napis)
	except ValueError:
		return -1

@route('/')
def glowna():
	sciezka = request.environ.get('PATH_INFO')
	zapytanie = request.environ.get('QUERY_STRING')
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
	else:
		return '<!DOCTYPE HTML>\nPodstrona ' + sciezka + ' nie istnieje. W zamian zapraszam na <a href=/>stronę główną</a>.'

application = default_app()
