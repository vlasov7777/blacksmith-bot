# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  remote_ctrl_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_remote_control(type, source, body):
	confs = GROUPCHATS.keys()
	confs.sort()
	if body:
		args = body.split()
		if len(args) >= 3:
			item = args[0].strip().lower()
			if item in confs:
				conf = item
			elif check_number(item):
				number = int(item) - 1
				if number >= 0 and number <= len(confs):
					conf = confs[number]
				else:
					conf = False
			else:
				conf = False
			if conf:
				mtype = args[1].strip().lower()
				if mtype == u'чат':
					msgtype = 'public'
				elif mtype == u'приват':
					msgtype = 'private'
				else:
					msgtype = False
				if msgtype:
					command = args[2].strip().lower()
					if len(args) >= 4:
						Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
					else:
						Parameters = ''
					if len(Parameters) <= 96:
						if COMMANDS.has_key(command):
							call_command_handlers(command, msgtype, [source[0], conf, source[2]], Parameters, command)
						else:
							reply(type, source, u'нет такой команды')
					else:
						reply(type, source, u'слишком длинные параметры')
				else:
					reply(type, source, u'тип указан не корректно')
			else:
				reply(type, source, u'нет такой конференции')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		col, list = 0, ''
		for conf in confs:
			col = col + 1
			list += u'\n№ '+str(col)+'. - '+conf
		reply(type, source, list)

register_command_handler(handler_remote_control, 'ремоут', ['все','суперадмин'], 100, 'Выполняет заданную команду дистанционно, в зависимости от параметра [чат/приват] направляет ответ вам или в чат.\nБез параметра покажет пронумерованый список комнат.\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'ремоут [конференция/номер конфы в списке] [чат/приват] [команда] [параметры]', ['ремоут witcher@conference.jabber.ru приват хтобыл','ремоут','ремоут bot-castle@conference.jabber.ru','ремоут 12 чат тык ]{vich'])
