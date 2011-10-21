#===istalismanplugin===
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  more_plugin.py

#  Initial Copyright © 2009 Als [als-als@ya.ru]
#  Modifications: WitcherGeralt [WitcherGeralt@rocketmail.com]

MORE = {}

def handler_more(type, source, body):
	if type == 'public' and MORE.has_key(source[1]):
		if MORE[source[1]]:
			reply(type, source, MORE[source[1]])
	else:
		reply(type, source, u'а смысл?')

def handler_more_outmsg(target, body, obody):
	if MORE.has_key(target):
		if hash(obody) != MORE[target]:
			if len(obody) > CHAT_MSG_LIMIT:
				MORE[target] = obody[CHAT_MSG_LIMIT:]

def init_more(conf):
	MORE[conf] = None

register_outgoing_message_handler(handler_more_outmsg)
register_command_handler(handler_more, 'далее', ['все','разное'], 10, 'Показывает следующую часть сообщения посланного в общий чат конференции (так как оно обрезается до %d символов)' % CHAT_MSG_LIMIT, 'далее', ['далее'])

register_stage1_init(init_more)
