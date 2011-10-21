# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  servres_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

SERVSTAT = {}
RESSTAT = {}

def handler_servres_stat(conf, nick, afl, role):
	instance = GROUPCHATS[conf][nick]
	if instance.has_key('full_jid'):
		jid = instance['full_jid']
		if jid.count('/'):
			list = jid.split('/')
			stripped_jid = list[0]
			server = stripped_jid.split('@')[1]
			resourse = list[1]
			if server not in SERVSTAT:
				SERVSTAT[server] = []
			if stripped_jid not in SERVSTAT[server]:
				SERVSTAT[server].append(stripped_jid)
			if resourse not in RESSTAT:
				RESSTAT[resourse] = []
			if stripped_jid not in RESSTAT[resourse]:
				RESSTAT[resourse].append(stripped_jid)

def handler_check_servstat(type, source, body):
	stat = []
	for server in SERVSTAT:
		stat.append([len(SERVSTAT[server]), server])
	stat.sort()
	stat.reverse()
	list = ''
	col = 0
	for item in stat:
		col = col + 1
		if col <= 20:
			list += '\n'+str(col)+'. '+item[1]+' - '+str(item[0])
	reply(type, source, u'Всего серверов '+str(col)+' :'+list)

def handler_check_resstat(type, source, body):
	stat = []
	for resourse in RESSTAT:
		stat.append([len(RESSTAT[resourse]), resourse])
	stat.sort()
	stat.reverse()
	list = ''
	col = 0
	for item in stat:
		col = col + 1
		if col <= 20:
			list += '\n'+str(col)+'. '+item[1]+' - '+str(item[0])
	reply(type, source, u'Всего ресурсов '+str(col)+' :'+list)

register_join_handler(handler_servres_stat)
register_command_handler(handler_check_servstat, 'сервера', ['все','инфо'], 10, 'Выдаёт топ 20 серверов, зафиксированных за рабочую сессию, с которых юзеры входили в конференции, а также колличество использований каждого\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'сервера', ['сервера'])
register_command_handler(handler_check_resstat, 'ресурсы', ['все','инфо'], 10, 'Выдаёт топ 20 ресурсов, зафиксированных за рабочую сессию, с которыми юзеры входили в конференции, а также колличество использований каждого\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'ресурсы', ['ресурсы'])
