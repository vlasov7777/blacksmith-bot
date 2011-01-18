# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Endless / BlackSmith plugin
#  antivipe_plugin.py

# Ported from AntiVipe bot: by Avinar (avinar@xmpp.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

TRUSTED_SERVERS = ['jabber.ru','xmpp.ru','jabbers.ru','xmpps.ru','talkonaut.com','jabber.org','gtalk.com','gmail.com','jabberon.ru','jabbrik.ru']

AVIPES = {}

def findServer(jid):
	if jid.count('@'):
		jid = jid.split('@')[1]
	if jid.count('/'):
		jid = jid.split('/')[0]
	return jid

def handler_antivipe_presence(Prs):
	status, type = Prs.getStatusCode(), Prs.getType()
	if type == 'unavailable' and status == '303':
		conf = (Prs.getFrom()).getStripped()
		nick = Prs.getNick()
		afl = Prs.getAffiliation()
		role = Prs.getRole()
		handler_antivipe_join(conf, nick, afl, role)

def handler_antivipe_join(conf, nick, afl, role):
	if conf not in UNAVALABLE:
		now_time = time.time()
		jid = handler_jid(conf+'/'+nick)
		if (now_time - INFO['start']) >= 60 and jid not in ADLIST and conf in AVIPES and afl == 'none':
			if now_time - AVIPES[conf]['ltime'] <= 15:
				AVIPES[conf]['jids'].append(jid)
				joined = AVIPES[conf]['jids']
				col = len(joined)
				if col >= 3:
					AVIPES[conf]['ltime'] = now_time
					botnick, server = handler_botnick(conf), findServer(jid)
					if findServer(joined[col - 2]) == server and findServer(joined[col - 3]) == server:
						if server not in TRUSTED_SERVERS:
							handler_banjid(conf, server, u'%s (Подозрение на вайп атаку!)' % (botnick))
							for usr in GROUPCHATS[conf]:
								if user_level(conf+'/'+usr, conf) >= 20 and GROUPCHATS[conf][usr]['ishere']:
									msg(conf+'/'+nick, u'Внимание! Сервер %s занесен в бан лист!' % (server))
						else:
							for usr in GROUPCHATS[conf]:
								usr_jid = handler_jid(conf+'/'+usr)
								if findServer(usr_jid) == server and GROUPCHATS[conf][usr]['ishere']:
									handler_kick(conf, usr, u'%s (Подозрение на вайп атаку!)' % (botnick))
					else:
						handler_banjid(conf, jid, u'%s: шестиминутный бан... (Подозрение на вайп атаку!)' % (botnick))
						try:
							threading.Timer(360, handler_unban,(conf, jid)).start()
						except:
							LAST['null'] += 1
			else:
				AVIPES[conf]['jids'] = [jid]
				AVIPES[conf]['ltime'] = now_time

def handler_antivipe_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/antivipe.txt'
			if body in [u'вкл', 'on', '1']:
				AVIPES[source[1]] = {'ltime': 0, 'num': 0, 'jids': []}
				write_file(filename, "'on'")
				reply(type, source, u'Функция антивайпа включена!')
			elif body in [u'выкл', 'off', '0']:
				if source[1] in AVIPES:
					del AVIPES[source[1]]
				write_file(filename, "'off'")
				reply(type, source, u'Функция антивайпа отключена!')
			else:
				reply(type, source, u'Читай помощь по команде!')
		elif source[1] in UNAVALABLE:
			reply(type, source, u'Если бот не админ - антивайп неработоспособен...')
		elif source[1] in AVIPES:
			reply(type, source, u'Функция антивайпа включена!')
		else:
			reply(type, source, u'Функция антивайпа отключена!')
	else:
		reply(type, source, u'только в чате мудак!')

def antivipe_init(conf):
	if check_file(conf, 'antivipe.txt', "'on'"):
		if eval(read_file('dynamic/'+conf+'/antivipe.txt')) != 'off':
			AVIPES[conf] = {'ltime': 0, 'jids': []}
	else:
		delivery(u'Внимание! Не удалось создать antivipe.txt для "%s"!' % (conf))

register_presence_handler(handler_antivipe_presence)
register_join_handler(handler_antivipe_join)
register_command_handler(handler_antivipe_control, 'антивайп', ['админ','все'], 20, 'Включение/отключение функции защиты от вайп атак. Способно защитить от примитивных и средних атак. По умолчанию включен.', 'антивайп [вкл/on/1/выкл/off/0]', ['антивайп on','антивайп off'])

register_stage1_init(antivipe_init)
