#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  idle_plugin.py

#  Initial Copyright © 2007 Als [Als@exploit.in]

IDS_UPTIME = []

def handler_uptime_server(type, source, server):
	if not server:
		server = SERVER
	idle_iq = xmpp.Iq(to = server, typ = 'get')
	INFA['outiq'] += 1
	ID = 'lytic_'+str(INFA['outiq'])
	IDS_UPTIME.append(ID)
	idle_iq.addChild('query', {}, [], xmpp.NS_LAST)
	idle_iq.setID(ID)
	JCON.SendAndCallForResponse(idle_iq, uptime_server_answer, {'type': type, 'source': source, 'server': server})

def uptime_server_answer(coze, stanza, type, source, server):
	ID = stanza.getID()
	if ID in IDS_UPTIME:
		IDS_UPTIME.remove(ID)
		if stanza:
			repl = u'Там нет джаббер сервера, либо он упал, хотя может просто его инфа закрыта...'
			if stanza.getType() == 'result':
				Props = stanza.getPayload()
				if Props:
					for Pr in Props:
						sec = Pr.getAttrs()['seconds']
						if sec and sec != '0':
							repl = server+'`s uptime is '+timeElapsed(int(sec))
			reply(type, source, repl)

def handler_userinfo_idle(type, source, nick):
	if source[1] in GROUPCHATS:
		if nick:
			if nick != source[2]:
				if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
					idletime = int(time.time() - GROUPCHATS[source[1]][nick]['idle'])
					reply(type, source, u'%s поступил в морг %s назад...' % (nick, timeElapsed(idletime)))
				else:
					reply(type, source, u'нету его')
			else:
				reply(type, source, u'и что я должен сказать? ;)')
		else:
			reply(type, source, u'я никак не пойму чего ты хочеш')
	else:
		reply(type, source, u'ты определённо тупиш')

register_command_handler(handler_uptime_server, 'аптайм', ['инфо','все'], 10, 'Показывает аптайм определённого сервера.', 'аптайм [сервер]', ['аптайм jabber.aq'])
register_command_handler(handler_userinfo_idle, 'жив', ['инфо','все'], 10, 'Показывает сколько времени неактивен юзер.', 'жив [ник]', ['жив mr.chuvac'])
