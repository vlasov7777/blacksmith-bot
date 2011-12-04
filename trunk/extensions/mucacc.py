# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  mucacc_plugin.py

# CallForResponse (c) Gigabyte
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_IQ_SendAndCall(type, source, conf, item_name, item, afrls, afrl, nick, rsn = None):
	stanza = xmpp.Iq(to = conf, typ = 'set')
	INFA['outiq'] += 1
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	afl_role = query.addChild('item', {item_name: item, afrls: afrl})
	if rsn:
		afl_role.setTagData('reason', rsn)
	stanza.addChild(node = query)
	JCON.SendAndCallForResponse(stanza, handler_afrls_answer, {'type': type, 'source': source})

def handler_afrls_answer(coze, stanza, type, source):
	if stanza.getType() == 'result':
		reply(type, source, u"Сделано.")
	else:
		reply(type, source, u"Запрещено. Тип: %s." % stanza.getType())

def handler_ban2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'jid', jid, 'affiliation', 'outcast', nick, reason)
def handler_none2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'jid', jid, 'affiliation', 'none', nick, reason)
def handler_member2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'jid', jid, 'affiliation', 'member', nick, reason)
def handler_admin2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'jid', jid, 'affiliation', 'admin', nick, reason)
def handler_owner2(type, source, conf, jid, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'jid', jid, 'affiliation', 'owner', nick, reason)
def handler_kick2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'nick', nick, 'role', 'none', nick, reason)
def handler_visitor2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'nick', nick, 'role', 'visitor', nick, reason)
def handler_participant2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'nick', nick, 'role', 'participant', nick, reason)
def handler_moder2(type, source, conf, nick, reason):
	handler_IQ_SendAndCall(type, source, conf, 'nick', nick, 'role', 'moderator', nick, reason)

def command_kick(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			nick = args[0].strip()
			jid = handler_jid('%s/%s' % (source[1], nick))
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
			jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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
					jid = handler_jid('%s/%s' % (source[1], nick))
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

command_handler(command_moder, 20, "mucacc")
command_handler(command_member, 20, "mucacc")
command_handler(command_admin, 30, "mucacc")
command_handler(command_owner, 30, "mucacc")
command_handler(command_kick, 15, "mucacc")
command_handler(command_visitor, 15, "mucacc")
command_handler(command_participant, 15, "mucacc")
command_handler(command_none, 20, "mucacc")
command_handler(command_ban, 20, "mucacc")
command_handler(command_fullban, 80, "mucacc")
command_handler(command_fullunban, 80, "mucacc")
