# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  mucacc_plugin.py

# CallForResponse (c) Gigabyte
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

AFLRLS_REPLS = u'Вытащил %s из бани!/Забанил %s навеке >:D/Отобрал аффиляцию у %s, как конфетку у ребёнка :D/Теперь %s у нас в составе!/Оо! %s теперь крутой.../Нифига себе, как %s высоко забрался!/Хаха! %s отхватил пендюль!/Заткнул %s пасть старым потником!/Дал %s участника./Теперь %s модер.'.split('/')

IDS_ADMIN_IQ = []

def handler_IQ_SendAndCall(type, source, repl, conf, item_name, item, afrls, afrl, nick, rsn = None):
	stanza = xmpp.Iq(to = conf, typ = 'set')
	INFA['outiq'] += 1
	ID = 'lytic_%d' % (INFA['outiq'])
	IDS_ADMIN_IQ.append(ID)
	stanza.setID(ID)
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	afl_role = query.addChild('item', {item_name: item, afrls: afrl})
	if rsn:
		afl_role.setTagData('reason', rsn)
	stanza.addChild(node = query)
	JCON.SendAndCallForResponse(stanza, handler_afrls_answer, {'type': type, 'source': source, 'nick': nick, 'repl': repl})

def handler_afrls_answer(coze, stanza, type, source, nick, repl):
	 ID = stanza.getID()
	 if ID in IDS_ADMIN_IQ:
		IDS_ADMIN_IQ.remove(ID)
		if stanza.getType() == 'result':
			reply(type, source, repl % (nick))
		else:
			reply(type, source, u'Так нельзя!')

def handler_ban2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[1], conf, 'jid', jid, 'affiliation', 'outcast', nick, reason)
def handler_none2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[2], conf, 'jid', jid, 'affiliation', 'none', nick, reason)
def handler_member2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[3], conf, 'jid', jid, 'affiliation', 'member', nick, reason)
def handler_admin2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[4], conf, 'jid', jid, 'affiliation', 'admin', nick, reason)
def handler_owner2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[5], conf, 'jid', jid, 'affiliation', 'owner', nick, reason)
def handler_kick2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[6], conf, 'nick', nick, 'role', 'none', nick, reason)
def handler_visitor2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[7], conf, 'nick', nick, 'role', 'visitor', nick, reason)
def handler_participant2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[8], conf, 'nick', nick, 'role', 'participant', nick, reason)
def handler_moder2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, AFLRLS_REPLS[9], conf, 'nick', nick, 'role', 'moderator', nick, reason)

def command_kick(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			jid = handler_jid(source[1]+'/'+nick)
			if jid not in ADLIST:
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_kick2(type, source, source[1], nick, reason)
			else:
				reply(type, source, u'кикать своего админа? да ни за что!')
		else:
			reply(type, source, u'кого?')
	else:
		reply(type, source, u'приколист :-D')

def command_visitor(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			jid = handler_jid(source[1]+'/'+nick)
			if jid not in ADLIST:
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_visitor2(type, source, source[1], nick, reason)
			else:
				reply(type, source, u'затыкать своего админа? да ни за что!')
		else:
			reply(type, source, u'кого?')
	else:
		reply(type, source, u'приколист :-D')

def command_participant(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				reason = body[(body.find(' ') + 1):].strip()
			else:
				reason = source[2]
			handler_participant2(type, source, source[1], args[0].strip(), reason)
		else:
			reply(type, source, u'кого?')
	else:
		reply(type, source, u'приколист :-D')

def command_moder(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				reason = body[(body.find(' ') + 1):].strip()
			else:
				reason = source[2]
			handler_moder2(type, source, source[1], args[0].strip(), reason)
		else:
			reply(type, source, u'кого выделывать то?')
	else:
		reply(type, source, u'приколист :-D')

def command_member(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_member2(type, source, source[1], jid, nick, reason)
			else:
				reply(type, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(type, source, u'кого выделывать то?')
	else:
		reply(type, source, u'приколист :-D')

def command_admin(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_admin2(type, source, source[1], jid, nick, reason)
			else:
				reply(type, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(type, source, u'кого выделывать то?')
	else:
		reply(type, source, u'приколист :-D')

def command_owner(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_owner2(type, source, source[1], jid, nick, reason)
			else:
				reply(type, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(type, source, u'кого выделывать то?')
	else:
		reply(type, source, u'приколист :-D')

def command_ban(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if jid not in ADLIST:
					if len(args) >= 2:
						reason = body[(body.find(' ') + 1):].strip()
					else:
						reason = source[2]
					handler_ban2(type, source, source[1], jid, nick, reason)
				else:
					reply(type, source, u'своего админа? да ни за что!')
			else:
				reply(type, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(type, source, u'кого?')
	else:
		reply(type, source, u'приколист :-D')

def command_none(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				handler_none2(type, source, source[1], jid, nick, reason)
			else:
				reply(type, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(type, source, u'кого?')
	else:
		reply(type, source, u'приколист :-D')

def command_fullban(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = nick
				if len(args) >= 2:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				for conf in GROUPCHATS.keys():
					handler_banjid(conf, jid, reason)
				reply(type, source, u'сделано')
			else:
				reply(type, source, u'хрень пишеш это не жид и юзеров с таким ником здесь небыло')
		else:
			reply(type, source, u'кого банить то?')
	else:
		reply(type, source, u'это надо делать в чате')

def command_fullunban(type, source, jid):
	if jid:
		if jid.count('.') and not jid.count(' '):
			for conf in GROUPCHATS.keys():
				handler_unban(conf, jid)
			reply(type, source, u'сделано')
		else:
			reply(type, source, u'Хрень пишешь! Это не жид!')
	else:
		reply(type, source, u'кого разбанивать то?')

register_command_handler(command_moder, 'модер', ['админ','все'], 20, 'Делает юзера модером', 'модер [nick]', ['модер чел','модер чел'])
register_command_handler(command_member, 'мембер', ['админ','все'], 20, 'Делает юзера мембером', 'мембер [nick/jid]', ['мембер чел','мембер чел','мембер admin@jrap.ru'])
register_command_handler(command_admin, 'админ', ['админ','все'], 30, 'Делает юзера админом', 'админ [nick/jid]', ['админ чел','админ чел','админ admin@jrap.ru'])
register_command_handler(command_owner, 'овнер', ['админ','все'], 30, 'Делает юзера владельцен', 'овнер [nick/jid]', ['овнер чел','овнер чел','овнер admin@jrap.ru'])
register_command_handler(command_kick, 'кик', ['админ','все'], 15, 'Кикает чела из конфы', 'кик [nick] [причина]', ['кик чел','кик чел урод'])
register_command_handler(command_visitor, 'визитор', ['админ','все'], 15, 'Лишает юзера голоса', 'визитор [nick] [причина]', ['визитор чел','визитор чел заткнись'])
register_command_handler(command_participant, 'участник', ['админ','все'], 15, 'Даёт посетителю право голоса или снимает модера', 'участник [nick]', ['участник чел','участник другой_чел'])
register_command_handler(command_none, 'никто', ['админ','все'], 20, 'Делает юзера никем, т.е. снимает аффиляцию, в том числе и разбанивает', 'никто [nick]', ['никто чел','никто чел'])
register_command_handler(command_ban, 'бан', ['админ','все'], 20, 'Банит юзера/жид/сервер', 'бан [nick/jid] [причина]', ['бан чел','бан чел критин','бан qip.ru быдлосервак','бан user@qip.ru'])
register_command_handler(command_fullban, 'фулбан', ['суперадмин','все'], 80, 'Банит юзера во всех конфах бота', 'фулбан [jid/nick] [причина]', ['фулбан bancheg@qip.ru','фулбан чувак'])
register_command_handler(command_fullunban, 'фулyнбан', ['суперадмин','все'], 80, 'вытаскивает жид из бани во всех конфах бота', 'фулуннбан [jid]', ['фулyнбан bancheg@qip.ru'])
