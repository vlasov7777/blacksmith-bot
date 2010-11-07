# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  antireklama_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_reklama_check(body):
	body = body.lower()
	for reklama in ['@conf','http://']:
		if body.count(reklama):
			return True
	return False

def handler_antireklama(raw, type, source, body):
	if type == 'public' and source[2] != '':
		if user_level(source[0], source[1]) < 11:
			if handler_reklama_check(body):
				handler_kick(source[1], source[2], u'Рекламить ЗАПРЕЩЕНО!!!')

register_message_handler(handler_antireklama)
