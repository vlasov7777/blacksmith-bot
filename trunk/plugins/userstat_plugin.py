# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  userstat_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

AFLID = {'none': u'никто', 'member': u'участвующий', 'admin': u'админ', 'owner': u'владелец'}
ROLEID = {'visitor': u'посетитель', 'participant': u'участник', 'moderator': u'модератор'}

USERSTAT = {}

def handler_userstat(Prs):
	Ptype = Prs.getType()
	if Ptype != 'error':
		fromjid = Prs.getFrom()
		conf = fromjid.getStripped()
		nick = fromjid.getResource()
		jid = handler_jid(conf+'/'+nick)
		if jid not in USERSTAT[conf]['jids']:
			USERSTAT[conf]['jids'][jid] = {'joined': '', 'seen': '', 'joins': 0, 'ishere': True, 'afl': u'никто', 'role': u'участник', 'leave': u'нет', 'nicks': []}
		if Ptype == 'unavailable':
			code = Prs.getStatusCode()
			if code == '303':
				new_nick = Prs.getNick()
				if new_nick not in USERSTAT[conf]['jids'][jid]['nicks']:
					USERSTAT[conf]['jids'][jid]['nicks'].append(new_nick)
			else:
				USERSTAT[conf]['jids'][jid]['seen'] = time.strftime('%d.%m.%Y (%H:%M:%S) GMT', time.gmtime())
				USERSTAT[conf]['jids'][jid]['ishere'] = False
				reason = Prs.getReason() or Prs.getStatus()
				if not reason:
					reason = u'причина отсутствует'
				if code == '307':
					USERSTAT[conf]['jids'][jid]['leave'] = u'Получил КИК ('+reason+')'
				elif code == '301':
					USERSTAT[conf]['jids'][jid]['leave'] = u'Получил БАН ('+reason+')'
				else:
					USERSTAT[conf]['jids'][jid]['leave'] = reason
		elif Ptype in ['available', None]:
			if not USERSTAT[conf]['jids'][jid]['ishere']:
				USERSTAT[conf]['jids'][jid]['joined'] = time.strftime('%d.%m.%Y (%H:%M:%S) GMT', time.gmtime())
				USERSTAT[conf]['jids'][jid]['ishere'] = True
				USERSTAT[conf]['jids'][jid]['joins'] += 1
			if nick not in USERSTAT[conf]['jids'][jid]['nicks']:
				USERSTAT[conf]['jids'][jid]['nicks'].append(nick)
			afl = Prs.getAffiliation()
			if afl in AFLID:
				afl = AFLID[afl]
			USERSTAT[conf]['jids'][jid]['afl'] = afl
			role = Prs.getRole()
			if role in ROLEID:
				role = ROLEID[role]
			USERSTAT[conf]['jids'][jid]['role'] = role
		USERSTAT[conf]['col'] += 1
		if USERSTAT[conf]['col'] >= 16:
			USERSTAT[conf]['col'] = 0
			write_file('dynamic/'+conf+'/userstat.txt', str(USERSTAT[conf]['jids']))

def handler_check_userstat(type, source, body):
	if source[1] in GROUPCHATS:
		if not body:
			jid = handler_jid(source[0])
		elif body.count('@') and body.count('.') and not body.count(' '):
			jid = body
		elif body in GROUPCHATS[source[1]]:
			jid = handler_jid(source[1]+'/'+body)
		else:
			jid = False
		if jid and jid in USERSTAT[source[1]]['jids']:
			repl = u'\nВсего входов - '+str(USERSTAT[source[1]]['jids'][jid]['joins'])
			if USERSTAT[source[1]]['jids'][jid]['joined']:
				repl += u'\nВремя последнего входа - '+USERSTAT[source[1]]['jids'][jid]['joined']
			afl_role = USERSTAT[source[1]]['jids'][jid]['afl']+' / '+USERSTAT[source[1]]['jids'][jid]['role']
			repl += u'\nПоследняя роль - '+afl_role
			if USERSTAT[source[1]]['jids'][jid]['joins'] >= 2 and USERSTAT[source[1]]['jids'][jid]['seen']:
				repl += u'\nВремя последнего выхода - '+USERSTAT[source[1]]['jids'][jid]['seen']
				repl += u'\nпричина выхода - '+USERSTAT[source[1]]['jids'][jid]['leave']
			repl += u'\nНики: '+', '.join(sorted(USERSTAT[source[1]]['jids'][jid]['nicks']))
			reply(type, source, repl)
		else:
			reply(type, source, u'на него нет статистики')
	else:
		reply(type, source, u'Ээй! Ты не в чате!')

def handler_userstat_here(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			nick = body
		else:
			nick = source[2]
		if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
			if body:
				repl = u'"%s" сидит здесь - ' % (nick)
			else:
				repl = u'ты провёл здесь - '
			reply(type, source, repl+timeElapsed(time.time() - GROUPCHATS[source[1]][nick]['joined']))
		else:
			reply(type, source, u'сейчас его нет здесь')
	else:
		reply(type, source, u'Ээй! Ты не в чате!')

def userstat_save():
	for conf in USERSTAT.keys():
		if USERSTAT[conf]['col']:
			write_file('dynamic/'+conf+'/userstat.txt', str(USERSTAT[conf]['jids']))

def userstat_init(conf):
	USERSTAT[conf] = {'col': 0, 'jids': {}}
	if check_file(conf, 'userstat.txt'):
		try:
			USERSTAT[conf]['jids'] = eval(read_file('dynamic/'+conf+'/userstat.txt'))
			for jid in USERSTAT[conf]['jids']:
				USERSTAT[conf]['jids'][jid]['ishere'] = False
		except:
			LAST['null'] += 1
	else:
		delivery(u'Внимание! Не удалось создать userstat.txt для "%s"!' % (conf))

register_presence_handler(handler_userstat)
register_command_handler(handler_check_userstat, 'юзерстат', ['все','инфо'], 20, 'Показывает статистику по конференции определённого юзера, без параметров покажет вашу статистику\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'юзерстат [nick]', ['юзерстат leon'])
register_command_handler(handler_userstat_here, 'пребывание', ['все','инфо'], 10, 'Показывает время проведёноое определённым юзером в конференции (последний вход), без параметров покажет вашу статистику', 'пребывание [nick]', ['пребывание leon'])
register_stage3_init(userstat_save)

register_stage1_init(userstat_init)
