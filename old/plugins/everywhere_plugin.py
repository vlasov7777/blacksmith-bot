# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  everywhere_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_everywhere(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			mtype = args[0].strip().lower()
			if mtype == u'чат':
				msgtype = 'public'
			elif mtype == u'приват':
				msgtype = 'private'
			else:
				msgtype = False
			if msgtype:
				command = args[1].strip().lower()
				if len(args) >= 3:
					Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
				else:
					Parameters = ''
				if len(Parameters) <= 96:
					if COMMANDS.has_key(command):
						for conf in GROUPCHATS.keys():
							call_command_handlers(command, msgtype, [source[0], conf, source[2]], Parameters, command)
					else:
						reply(type, source, u'нет такой команды')
				else:
					reply(type, source, u'слишком длинные параметры')
			else:
				reply(type, source, u'тип указан не корректно')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		reply(type, source, u'я не умею читать мысли')

register_command_handler(handler_everywhere, 'везде', ['все','суперадмин'], 100, 'Выполняет заданную команду во всех конференциях которые обслуживает\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'везде [чат/приват] [команда] [параметры]', ['везде чат чисть','везде приват кик Лузер неудачник!'])
