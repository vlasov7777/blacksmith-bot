# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  © mrDoctorWho & WitcherGeralt, 2011 — 2013.


## server stats.
def command_server_stats(mType, source, server):
	if not server:
		server = SERVER
	INFO["outiq"] += 1
	iq = xmpp.Iq("get", to = server)
	iq.addChild("query", namespace = xmpp.NS_STATS)
	jClient.SendAndCallForResponse(iq, answer_server_stats, {"mType": mType, "source": source})

def answer_server_stats(some, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		INFO["outiq"] += 1
		iq = xmpp.Iq("get", to = stanza.getFrom())
		iq.addChild("query", {}, stanza.getQueryChildren(), xmpp.NS_STATS)
		jClient.SendAndCallForResponse(iq, answer_server_stats_get, {"mType": mType, "source": source})
	else:
		reply(mType, source, u"Нет ответа...")

def answer_server_stats_get(some, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		ls = []
		for node in stanza.getQueryChildren():
			name = node.getAttr("name")
			value = node.getAttr("value")
			if name and value:
				ls.append("%s: %s" % (name, value))
		if ls:
			ls.insert(0, "\n*** Статистика %s:" % stanza.getFrom())
			answer = str.join(chr(10), ls)
		else:
			answer = u"Нет результата."
	else:
		answer = u"Нет ответа."
	reply(mType, source, answer)


command_handler(command_server_stats, 10, "infa")


VcardDesc = {"NICKNAME": "Nick",
			"GIVEN": "Name",
			"FAMILY": "Surname",
			"FN": "Full Name",
			"BDAY": "Birthday",
			"USERID": "e-Mail",
			"URL": "Web Page",
			"DESC": "Description",
			"NUMBER": "Phone",
			"EXTADR": "Address",
			"PCODE": "Post Code",
			"LOCALITY": "City",
			"CTRY": "Country",
			"ORGNAME": "Organization",
			"ORGUNIT": "Department"}



def command_vcard(mType, source, args):
	if args:
		args = args.lstrip()
		if args in GROUPCHATS.get(source[1], {}):
			instance = "%s/%s" % (source[1], args)
		elif "@" in args and "." in args:
			instance = args
		else:
			return reply(mType, source, u"«%s» — сейчас нет в чате и на JabberID это не похоже." % args)
	elif source[1] in GROUPCHATS:
		instance = source[0]
	else:
		return reply(mType, source, u"Только для чатов.")
	INFO["outiq"] += 1
	iq = xmpp.Iq("get", to = instance)
	iq.addChild("vCard", namespace = xmpp.NS_VCARD)
	jClient.SendAndCallForResponse(iq, vcard_answer, {"mType": mType, "source": source})


def parse_vcard(node, ls):
	if node.kids:
		for sNode in node.getChildren():
			name = sNode.getName()
			if name == "PHOTO":
				continue
			parse_vcard(sNode, ls)
	else:
		data = (node.getData()).strip()
		if data and len(data) <= 512:
			name = node.getName()
			name = VcardDesc.get(name, name.capitalize())
			ls.append("%s: %s" % (name, data))

def vcard_answer(something, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		ls = []
		parse_vcard(stanza, ls)
		if ls:
			ls.insert(0, "==>")
			answer = str.join(chr(10), ls)
			if mType == "groupchat":
				msg(source[1], answer)
				del answer
		else:
			answer = u"VCard пуст!"
	else:
		answer = u"Нет ответа..." # OOPS!
	if locals().has_key("answer"):
		reply(mType, source, answer)

command_handler(command_vcard, 10, "vcard")


def command_getVersion(mType, source, args):
	if args:
		args = args.lstrip()
		if args in GROUPCHATS.get(source[1], {}):
			target = "%s/%s" % (source[1], args)
		elif "@" in args and "." in args:
			target = args
		else:
			return reply(mType, source, u"«%s» — сейчас нет в чате и на JabberID это не похоже." % args)
	elif source[1] in GROUPCHATS:
		target = source[0]
	else:
		return reply(mType, source, u"Только для чатов.")
	iq = xmpp.Iq(to = target, typ = "get")
	iq.addChild("query", {}, [], xmpp.NS_VERSION)
	jClient.SendAndCallForResponse(iq, answer_version, {"mType": mType, "source": source})

def answer_version(coze, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		Name, Ver, OS = "[None]", "[None]", "[None]"
		data =  stanza.getQueryChildren()
		if data:
			for x in data:
				xname = x.getName()
				if xname == "name":
					Name = x.getData()
				elif xname == "version":
					Ver = x.getData()
				elif xname == "os":
					OS = x.getData()
			answer = "\nName: %s\nVer.: %s\nOS: %s" % (Name, Ver, OS)
		else:
			answer = u"Error: null."
	else:
		answer = u"Нет ответа."
	reply(mType, source, answer)

command_handler(command_getVersion, 10, "version")

def command_uptime(mType, source, server):
	if not server:
		server = SERVER
	INFO["outiq"] += 1
	iq = xmpp.Iq("get", to = server)
	iq.addChild("query", namespace = xmpp.NS_LAST)
	jClient.SendAndCallForResponse(iq, idle_answer, {"mType": mType, "source": source, "instance": server, "typ": None})

def command_idle(mType, source, args):
	if args:
		args = args.lstrip()
		if args in GROUPCHATS.get(source[1], {}):
			instance = "%s/%s" % (source[1], args)
		elif "@" in args and "." in args:
			instance = args
		else:
			answer = u"«%s» — сейчас нет в чате и на JabberID это не похоже." % args
	elif source[1] in GROUPCHATS:
		instance = source[0]
	else:
		answer = u"Только для чатов."
	if not locals().has_key("answer"):
		iq = xmpp.Iq("get", to = instance)
		iq.addChild("query", namespace = xmpp.NS_LAST)
		jClient.SendAndCallForResponse(iq, idle_answer, {"mType": mType, "source": source, "instance": instance, "typ": True})
	else:
		reply(mType, source, answer)

def idle_answer(spam, stanza, mType, source, instance, typ):
	if xmpp.isResultNode(stanza):
		seconds = stanza.getTagAttr("query", "seconds")
		if seconds and check_number(seconds):
			answer = (u"Последняя активность «%s» — %s назад." if typ else u"Время работы «%s» — %s.") % (instance, timeElapsed(int(seconds)))
	if not locals().has_key("answer"):
		answer = u"Нет ответа от «%s»." % instance
	reply(mType, source, answer)


command_handler(command_uptime, 10, "idle")
command_handler(command_idle, 10, "idle")

