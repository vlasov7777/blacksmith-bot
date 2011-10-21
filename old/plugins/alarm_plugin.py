# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  alarm_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

ALARM_FILE = 'dynamic/alarm.txt'

ALARM_LIST = {}

def handler_alarm(type, source,  body):
	jid = handler_jid(source[0])
	if body:
		if len(body) <= 128:
			args = body.split()
			check = args[0].strip()
			if check.lower() in [u'ненада', 'del_all']:
				if jid in ALARM_LIST:
					alarm_data_save(jid, 'del_all')
					reply(type, source, u'по моему я что-то кому-то должен был напомнить, а чёрт забыл!')
				else:
					reply(type, source, u'Ты не заполнял напоминалку!')
			elif check == '+':
				if len(args) >= 2:
					text = ALARM_LIST[jid]
					if len(text) <= 512:
						text2 = body[(body.find(' ') + 1):].strip()
						data = u'\nИ ещё: '+text2
						alarm_data_save(jid, text+data)
						reply(type, source, u'И это тоже напомню...')
					else:
						reply(type, source, u'У тебя итак напоминалка переполнена! (предел 512 символов)')
				else:
					reply(type, source, u'Ты определённо что-то забыл!')
			else:
				alarm_data_save(jid, body)
				reply(type, source, u'буду напоминать тебе при каждом входе, или когда сам попросишь')
		else:
			reply(type, source, u'Слишком много текста! (предел 128 символов)')
	elif jid in ALARM_LIST:
		data = ALARM_LIST[jid]
		reply(type, source, u'Напоминаю: '+data)
	else:
		reply(type, source, u'ты не заполнял напоминалку')

def alarm_data_save(jid, data):
	if data == 'del_all':
		del ALARM_LIST[jid]
	else:
		ALARM_LIST[jid] = data
	write_file(ALARM_FILE, str(ALARM_LIST))

def handler_alarm_work(conf, nick, afl, role):
	jid = handler_jid(conf+'/'+nick)
	if jid in ALARM_LIST:
		msg(conf+'/'+nick, u'!Напоминаю: '+ALARM_LIST[jid])

def alarm_file_init():
	if initialize_file(ALARM_FILE):
		globals()['ALARM_LIST'] = eval(read_file(ALARM_FILE))
	else:
		Print('\n\nError: can`t create alarm.txt!', color2)

register_join_handler(handler_alarm_work)
register_command_handler(handler_alarm, 'напомнить', ['все','разное'], 10, 'Личная напоминалка закреплённая за вашим жидом, с любым параметром будет напоминать то что в парметре при каждом входе, с параметром "ненада" отключает напоминалку, без параметра напомнит, то что нужно было напомнить', 'напомнить [параметры]', ['напомнить','напомнить ненада','напомнить нада зайти на http://witcher-team.ucoz.ru/','напомнить + сюда тоже зайди Witcher@conference.jabber.ru'])
register_stage0_init(alarm_file_init)
