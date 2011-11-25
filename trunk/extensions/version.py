#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  version_plugin.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_version(type, source, nick):
	if source[1] in GROUPCHATS:
		if nick:
			if nick in GROUPCHATS[source[1]]:
				if not GROUPCHATS[source[1]][nick]['ishere']:
					reply(type, source, u'его нет здесь')
					return
				recipient = source[1]+'/'+nick
			else:
				recipient = nick
		else:
			recipient = source[0]
		iq = xmpp.Iq(to = recipient, typ = 'get')
		INFA['outiq'] += 1
		iq.addChild('query', {}, [], xmpp.NS_VERSION)
		JCON.SendAndCallForResponse(iq, handler_version_answer, {'type': type, 'source': source})
	else:
		reply(type, source, u'только в чате')

def handler_version_answer(coze, stanza, type, source):
		if stanza:
			if stanza.getType() == 'result':
				name = '[no name]'
				ver = '[no ver]'
				os = '[no os]'
				Props = stanza.getQueryChildren()
				for Prop in Props:
					Pname = Prop.getName()
					if Pname == 'name':
						name = Prop.getData()
					elif Pname == 'version':
						ver = Prop.getData()
					elif Pname == 'os':
						os = Prop.getData()
				repl = "\nName: %s\nVer.: %s\nOS: %s" % (name, ver, os)
			else:
				repl = u'он зашифровался'
		else:
			repl = u'нету такого'
		reply(type, source, repl)

command_handler(handler_version, 10, "version")
