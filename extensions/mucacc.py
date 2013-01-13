# BS mark.1-55
# /* coding: utf-8 */

#	BlackSmith plugin
#	© simpleApps, 2012.

BanBase = {}
BanBaseFile = "dynamic/banbase.txt"

def handle_AflRl(coze, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		reply(mType, source, u"Сделано.")
	else:
		reply(mType, source, u"Запрещено. Тип: %s." % stanza.getType())

def mucAccHandler(mType, source, body, func):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split(None, 1)
			nick = args[0].strip()
			if nick.count(".") or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(u"%s/%s" % (source[1], nick))
				else:
					jid = nick
				if (jid in ADLIST and func.func_name in ("outcast", "kick")) and (jid not in (handler_jid(u"%s/%s" % (source[1], source[2]), source[2]))):
					return reply(mType, source, u"Не стоит этого делать.")
				else:
					if len(args) > 1:
						reason = args[1].strip()
					else:
						reason = source[2]
					if func.func_name in ("outcast", "none", "member", "admin", "owner"):
						func(source[1], jid, reason, (handle_AflRl, {"mType": mType, "source": source}))
					else:
						func(source[1], nick, reason, (handle_AflRl, {"mType": mType, "source": source}))
		else:
			reply(mType, source, u"Некого.")
	else:
		reply(mType, source, u"Неподходящее место, не правда ли?")

def command_kick(mType, source, body):
	mucAccHandler(mType, source, body, kick)

def command_visitor(mType, source, body):
	mucAccHandler(mType, source, body, visitor)

def command_participant(mType, source, body):
	mucAccHandler(mType, source, body, participant)

def command_moder(mType, source, body):
	mucAccHandler(mType, source, body, moderator)

def command_member(mType, source, body):
	mucAccHandler(mType, source, body, member)

def command_admin(mType, source, body):
	mucAccHandler(mType, source, body, admin)

def command_owner(mType, source, body):
	mucAccHandler(mType, source, body, owner)

def command_ban(mType, source, body):
	mucAccHandler(mType, source, body, outcast)

def command_none(mType, source, body):
	mucAccHandler(mType, source, body, none)

def command_fullban(mType, source, body):
	if body:
		args = body.split(None, 1)
		nick = args[0].strip()
		if nick.count('.') or nick in GROUPCHATS[source[1]]:
			if nick in GROUPCHATS[source[1]]:
				jid = handler_jid('%s/%s' % (source[1], nick))
			else:
				jid = nick
			if len(args) > 1:
				reason = args[1].strip()
			else:
				reason = source[2]
			if BanBase.get(jid):
				reply(mType, source, u"Этот пользователь уже глобально забанен.")
				return
			else:
				number = len(GROUPCHATS.keys())
				BanBase[jid] = {"date": time.strftime("%d.%m.%Y (%H:%M:%S)"),
 								"number": number,
 								"reason": reason}
				write_file(BanBaseFile, str(BanBase))
			for conf in GROUPCHATS.keys():
				outcast(conf, jid, reason)
			answer = u"«%s» успешно забанен в %d конференциях." % (jid, number)
		else:
			answer = u"Это не ник или юзеров с таким ником здесь не было."
	elif BanBase:
		answer = "\n[#] [JID] [Причина] [Кол-во чатов]\n"
		num = 0
		for jid in BanBase.keys():
			if len(BanBase[jid].values()) > 2:
				date, reason, number = BanBase[jid].values()
			else:
				date, reason = BanBase[jid].values()
				number = 0
			num += 1
			answer +=  u"\n%i. %s (%s) %s [%d]" % (num, jid, reason, date, number)
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
				none(conf, jid)
			reply(mType, source, u'Сделано.')
		else:
			reply(mType, source, u'Не вижу JID.')
	else:
		reply(mType, source, u'Кого разбанивать-то?')

def banbase_init():
	if initialize_file(BanBaseFile, `{}`):
		globals()["BanBase"] = eval(read_file(BanBaseFile))
	else:
		Print('\n\nError: can`t create banbase.txt!', color2)


handler_register("00si", banbase_init)
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
