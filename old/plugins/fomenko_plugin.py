# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  fomenko_plugin.py

# Coded by: Evgеn [email: meb81@mail.ru]
# http://witcher-team.ucoz.ru/

def handler_fomenko(type, source, body):
	try:
		radky = read_link('http://www.fomenko.ru/foma/lenta/text.html').splitlines()
		if len(radky) >= 16:
			radky = radky[15].decode('windows-1251')
			if radky.count('<b>') >= 1:
				radky = radky.split('<b>')[1]
			else:
				radky = u'что-то левое с разметкой'
		else:
			radky = u'что-то левое с разметкой'
	except:
		radky = u'не могу пропарсить сайт'
	reply(type, source, radky)

register_command_handler(handler_fomenko, 'фоменко', ['фан','все'], 10, 'Аналог приколов Фоменко на Эндлессе', 'фоменко', ['фоменко'])
