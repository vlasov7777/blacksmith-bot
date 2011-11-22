#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  stanza_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>

def handler_stanza(source, type, node):
	if node:
		try:
			JCON.send(xmpp.simplexml.XML2Node(unicode(node).encode('utf-8'))); repl = "ok"
		except:
			repl = u'Чёто эта хрень не шлётся...'
	else:
		repl = u'ты что посылать собрался?'
	reply(source, type, repl)

command_handler(handler_stanza, 100, "stanza")
