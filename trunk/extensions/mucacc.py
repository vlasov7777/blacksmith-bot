# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  mucacc_plugin.py

# CallForResponse (c) Gigabyte
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

BanBase = {}
BanBaseFile = "dynamic/banbase.txt"

def IQSender(mType, source, conf, item_name, item, afrls, afrl, nick, rsn = None):
	stanza = xmpp.Iq(to = conf, typ = 'set')
	INFA['outiq'] += 1
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	afl_role = query.addChild('item', {item_name: item, afrls: afrl})
	if rsn:
		afl_role.setTagData('reason', rsn)
	stanza.addChild(node = query)
	JCON.SendAndCallForResponse(stanza, handler_afrls_answer, {'mType': mType, 'source': source})

def handler_afrls_answer(coze, stanza, mType, source):
	if stanza.getType() == 'result':
		reply(mType, source, u"Сделано.")
	else:
		reply(mType, source, u"Запрещено. Тип: %s." % stanza.getmType())

def handler_ban2(mType, source, conf, jid, nick, reason):
	IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'outcast', nick, reason)
def handler_none2(mType, source, conf, jid, nick, reason):
	IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'none', nick, reason)
def handler_member2(mType, source, conf, jid, nick, reason):
	IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'member', nick, reason)
def handler_admin2(mType, source, conf, jid, nick, reason):
	IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'admin', nick, reason)
def handler_owner2(mType, source, conf, jid, nick, reason):
	IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'owner', nick, reason)
def handler_kick2(mType, source, conf, nick, reason):
	IQSender(mType, source, conf, 'nick', nick, 'role', 'none', nick, reason)
def handler_visitor2(mType, source, conf, nick, reason):
	IQSender(mType, source, conf, 'nick', nick, 'role', 'visitor', nick, reason)
def handler_participant2(mType, source, conf, nick, reason):
	IQSender(mType, source, conf, 'nick', nick, 'role', 'participant', nick, reason)
def handler_moder2(mType, source, conf, nick, reason):
	IQSender(mType, source, conf, 'nick', nick, 'role', 'moderator', nick, reason)

def command_kick(mType, source, body):
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
				handler_kick2(mType, source, source[1], nick, reason)
			else:
				reply(mType, source, u'кикать своего админа? да ни за что!')
		else:
			reply(mType, source, u'кого?')
	else:
		reply(mType, source, u'приколист :-D')

def command_visitor(mType, source, body):
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
				handler_visitor2(mType, source, source[1], nick, reason)
			else:
				reply(mType, source, u'затыкать своего админа? да ни за что!')
		else:
			reply(mType, source, u'кого?')
	else:
		reply(mType, source, u'приколист :-D')

def command_participant(mType, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				reason = body[(body.find(' ') + 1):].strip()
			else:
				reason = source[2]
			handler_participant2(mType, source, source[1], args[0].strip(), reason)
		else:
			reply(mType, source, u'кого?')
	else:
		reply(mType, source, u'приколист :-D')

def command_moder(mType, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				reason = body[(body.find(' ') + 1):].strip()
			else:
				reason = source[2]
			handler_moder2(mType, source, source[1], args[0].strip(), reason)
		else:
			reply(mType, source, u'кого выделывать то?')
	else:
		reply(mType, source, u'приколист :-D')

def command_member(mType, source, body):
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
				handler_member2(mType, source, source[1], jid, nick, reason)
			else:
				reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(mType, source, u'кого выделывать то?')
	else:
		reply(mType, source, u'приколист :-D')

def command_admin(mType, source, body):
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
				handler_admin2(mType, source, source[1], jid, nick, reason)
			else:
				reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(mType, source, u'кого выделывать то?')
	else:
		reply(mType, source, u'приколист :-D')

def command_owner(mType, source, body):
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
				handler_owner2(mType, source, source[1], jid, nick, reason)
			else:
				reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(mType, source, u'кого выделывать то?')
	else:
		reply(mType, source, u'приколист :-D')

def command_ban(mType, source, body):
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
					handler_ban2(mType, source, source[1], jid, nick, reason)
				else:
					reply(mType, source, u'своего админа? да ни за что!')
			else:
				reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(mType, source, u'кого?')
	else:
		reply(mType, source, u'приколист :-D')

def command_none(mType, source, body):
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
				handler_none2(mType, source, source[1], jid, nick, reason)
			else:
				reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
		else:
			reply(mType, source, u'кого?')
	else:
		reply(mType, source, u'приколист :-D')

def command_fullban(mType, source, body):
		if body:
			args = body.split()
			nick = args[0].strip()
			if nick.count('.') or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid('%s/%s' % (source[1], nick))
				else:
					jid = nick
				if len(args) > 1:
					reason = body[(body.find(' ') + 1):].strip()
				else:
					reason = source[2]
				if BanBase.get(jid):
					reply(mType, source, u"Этот пользователь уже глобально забанен.")
					return
				else:
					BanBase[jid] = {"date": time.strftime("%d.%m.%Y (%H:%M:%S)"),
     								"reason": reason}
					write_file(BanBaseFile, str(BanBase))
				for conf in GROUPCHATS.keys():
					handler_banjid(conf, jid, reason)
				answer = u"Сделано."
			else:
				answer = u"Это не JID и юзеров с таким ником здесь не было."
		elif BanBase:
			answer = str()
			num = 0
			for jid in BanBase.keys():
				date, reason = BanBase[jid].values()
				num += 1
				answer +=  u"\n%i. %s (%s) [%s]." % (num, jid, reason, date)
		else:
			answer = u"В базе фуллбана пусто."
		reply(mType, source, answer)

def command_fullunban(mType, source, jid):
	if jid:
		if jid.count('.') and not jid.count(' '):
			if jid in BanBase:
				del BanBase[jid]
				write_file(BanBaseFile, str(BanBase))
			for conf in GROUPCHATS.keys():
				handler_unban(conf, jid)
			reply(mType, source, u'Сделано.')
		else:
			reply(mType, source, u'Хрень пишешь! Это не жид!')
	else:
		reply(mType, source, u'кого разбанивать то?')

def banbase_init():
	if initialize_file(BanBaseFile, `{}`):
		globals()["BanBase"] = eval(read_file(BanBaseFile))
	else:
		Print('\n\nError: can`t create banbase.txt!', color2)


register_stage0_init(banbase_init)
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
