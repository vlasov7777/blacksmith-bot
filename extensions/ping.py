# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  ping_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

PINGSTAT = {}


def handler_ping(type, source, nick):
	user, jid = nick, nick
	if nick:
		if source[1] in GROUPCHATS:
			if nick in GROUPCHATS[source[1]]:
				if not GROUPCHATS[source[1]][nick]['ishere']:
					reply(type, source, u'его нет здесь')
					return
				conf_nick = source[1]+'/'+nick
				user, jid = conf_nick, handler_jid(conf_nick)
	else:
		user, jid = source[0], handler_jid(source[0])
	iq = xmpp.Iq(to = user, typ = 'get')
	INFO['outiq'] += 1
	iq.addChild('ping', {}, [], xmpp.NS_PING)
	jClient.SendAndCallForResponse(iq, handler_ping_answer, {'t0': time.time(), 'mtype': type, 'source': source, 'nick': nick, 'jid': jid, 'user': user})

def handler_ping_answer(coze, stanza, t0, mtype, source, nick, jid, user):
		if stanza:
			if stanza.getType() == 'result':
				repl, difference = u'Понг от', (time.time() - t0)
				Ping = round(difference, 3)
				if jid not in PINGSTAT:
					PINGSTAT[jid] = []
				PINGSTAT[jid].append(Ping)
				if nick:
					repl += u' %s - %s секунд.' % (nick, str(Ping))
					if Ping > 12.00:
						repl += u' Кажись он висит!'
				else:
					repl += u' тебя - %s секунд.' % str(Ping)
					if Ping <= 0.10:
						repl += u' Твой понг реактивен!'
					elif (Ping > 0.10) & (Ping <= 0.50):
						repl += u' Твой понг отличный!'
					elif (Ping > 0.50) & (Ping <= 1.00):
						repl += u' Твой понг нормальный.'
					elif (Ping > 1.00) & (Ping <= 1.20):
						repl += u' Твой понг нормален.'
					elif (Ping > 1.20) & (Ping <= 1.60):
						repl += u' Твой понг медленный.'
					elif (Ping > 1.60) & (Ping <= 2.00):
						repl += u' Твой понг очень медленный.'
					elif (Ping > 2.00) & (Ping <= 6.00):
						repl += u' Твой понг тормоз!'
					else:
						repl += u' Убейся ап стену!'
				reply(mtype, source, repl)
			else:
				reping_by_version(mtype, source, user, jid, nick)

def reping_by_version(type, source, user, jid, nick):
	iq = xmpp.Iq(to = user, typ = 'get')
	iq.addChild('query', {}, [], xmpp.NS_VERSION)
	jClient.SendAndCallForResponse(iq, handler_ping_ver_answer, {'t1': time.time(), 'type': type, 'source': source, 'nick': nick, 'jid': jid, 'user': user})

def handler_ping_ver_answer(coze, stanza, t1, type, source, nick, jid, user):
		if stanza:
			if stanza.getType() == 'result':
				name, answer, difference = '[no name]', '', (time.time() - t1)
				Props = stanza.getQueryChildren()
				for Prop in Props:
					Pname = Prop.getName()
					if Pname == 'name':
						name = Prop.getData()
				Ping = round(difference, 3)
				if jid not in PINGSTAT:
					PINGSTAT[jid] = []
				PINGSTAT[jid].append(Ping)
				if nick:
					answer += u' от %s - за %s секунд.' % (nick, str(Ping))
				else:
					answer += u' от тебя - за %s секунд.' % str(Ping)
				repl = u'Понга нет. Ответ на версию ('+name+')'+answer
			else:
				repl = u'Ни пинга, ни версии...'
			reply(type, source, repl)

def form_ping_stat(jid):
	mass, col, max, min = 0, 0, 0, 999999.999
	for ping in PINGSTAT[jid]:
		mass += ping
		col += 1
		if ping < min:
			min = ping
		if ping > max:
			max = ping
	return (col, min, max, mass)

def handler_ping_stat(type, source, nick):
	if nick:
		if GROUPCHATS.has_key(source[1]) and nick in GROUPCHATS[source[1]]:
			jid = handler_jid(source[1]+'/'+nick)
		else:
			jid = nick
		if jid in PINGSTAT:
			(col, min, max, mass) = form_ping_stat(jid)
			if col != 0:
				repl = u'\nСтатистика пинга (всего %s):\nСамый быстрый пинг - %s\nСамый медленный пинг - %s\nСреднее время пинга - %s' % (str(col), str(min), str(max), str(round(mass / col, 3)))
			else:
				repl = u'На %s статистики нет!' % (jid)
		else:
			repl = u'На %s статистики нет!' % (jid)
	else:
		jid = handler_jid(source[0])
		if jid in PINGSTAT:
			(col, min, max, mass) = form_ping_stat(jid)
			if col != 0:
				repl = u'\nСтатистика пинга (всего %s):\nСамый быстрый пинг - %s\nСамый медленный пинг - %s\nСреднее время пинга - %s' % (str(col), str(min), str(max), str(round(mass / col, 3)))
			else:
				repl = u'На тебя статистики нет!'
		else:
			repl = u'На тебя статистики нет!'
	reply(type, source, repl)

command_handler(handler_ping, 10, "ping")
command_handler(handler_ping_stat, 10, "ping")