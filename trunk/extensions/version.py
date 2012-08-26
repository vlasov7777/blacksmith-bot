# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  version_plugin.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def command_getVersion(mType, source, args):
	if args:
		if GROUPCHATS.get(source[1]):
			if args in GROUPCHATS[source[1]]:
				target = "%s/%s" % (source[1], args.lstrip())
				if not GROUPCHATS[source[1]][args]['ishere']:
					reply(mType, source, "Его здесь нет.")
					return
			else:
				target = args
		else:
			reply(mType, source, u"Только для конференций.")
			return
	else:
		target = source[0]
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