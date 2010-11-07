# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  botstatus_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

DEF_STATUS = {'message': u'пиши "хелп", чтобы понять как со мной работать', 'status': 'chat'}
STATUS_LIST = {u'ушел': 'away', u'нет': 'xa', u'занят': 'dnd', u'чат': 'chat'}

def handler_set_bot_status(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 3:
			item = args[1].strip().lower()
			if item in STATUS_LIST:
				target = args[0].strip().lower()
				status = STATUS_LIST[item]
				message = body[((body.lower()).find(item) + (len(item) + 1)):].strip()
				if target == u'везде':
					for conf in GROUPCHATS.keys():
						change_status_work(conf, message, status)
				elif target == u'здесь':
					if source[1] in GROUPCHATS:
						change_status_work(source[1], message, status)
					else:
						reply(type, source, u'"здесь" вовсе и не чат!')
				elif target in GROUPCHATS:
					change_status_work(target, message, status)
				else:
					reply(type, source, u'В "%s" меня нет' % (target))
			else:
				reply(type, source, u'Статус "%s" мне неизвестен' % (item))
		else:
			reply(type, source, u'Чего-то определённо нехватает!')
	else:
		reply(type, source, u'Может чёнить самому придумать?')

def change_status_work(conf, message, status):
	STATUS[conf] = {'message': message, 'status': status}
	change_bot_status(conf, message, status)
	write_file('dynamic/'+conf+'/status.txt', str(STATUS[conf]))

def load_conf_status(conf):
	if check_file(conf, 'status.txt', str(DEF_STATUS)):
		STATUS[conf] = eval(read_file('dynamic/'+conf+'/status.txt'))
	else:
		delivery(u'Внимание! Не удалось создать status.txt для "%s"!' % (conf))

register_command_handler(handler_set_bot_status, 'ботстат', ['суперадмин','все'], 100, 'Установка постоянного статуса в конференции. Статусы: ушел (отсутствую) , нет (недоступен), занят (не беспокоить), чат (готов поболтать). Параметры: "везде" - установка статуса для всех комнат, "здесь" - установка статуса для данной конференции, также как параметр можно использовать конкретную конфу', 'ботстат [везде/здесь/конференция] [чат/ушел/нет/занят] [статусное сообщение]', ['ботстат везде чат пишите "хелп"...','ботстат witcher@conference.jabber.ru нет флудеры достали'])

register_stage1_init(load_conf_status)
