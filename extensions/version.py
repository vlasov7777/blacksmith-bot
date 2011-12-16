#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
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
					reply(mType, source, "Его здесь нет")
					return
			else:
				target = args
		else:
			reply(mType, source, u"Только для конференций")
			return
	else:
		target = source[0]
	iq = xmpp.Iq(to = target, typ = "get")
	iq.addChild("query", {}, [], xmpp.NS_VERSION)
	JCON.SendAndCallForResponse(iq, answer_version, {"mType": mType, "source": source})

def answer_version(coze, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		Name, Ver, Os = "[None]", "[None]", "[None]"
		for x in stanza.getQueryChildren():
			xname = x.getName()
			if xname == "name":
				Name = x.getData()
			elif xname == "version":
				Ver = x.getData()
			elif xname == "os":
				Os = x.getData()
		answer = "\nName: %s\nVer.: %s\nOS: %s" % (Name, Ver, Os)
	else:
		answer = u"Нет ответа."
	reply(mType, source, answer)

command_handler(command_getVersion, 10, "version")