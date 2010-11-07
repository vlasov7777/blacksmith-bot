#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  turn_plugin.py

#  Idea © 2008 Als [Als@exploit.in]
#  Initial Copyright © 2008 dimichxp [dimichxp@gmail.com]
#  Modifications © 2010 WitcherGeralt [WitcherGeralt@rocketmail.com]

global_en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,.Ю`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>Б~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,.ю`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>б~"))

turn_msgs = {}

def handler_turn_last(type, source, body):
	if type == 'public':
		if not body:
			body = turn_msgs[source[1]][handler_jid(source[0])]
			if body != None:
				if body not in [u'турн', 'turn']:
					list = {}
					for nick in GROUPCHATS[source[1]].keys():
						if GROUPCHATS[source[1]][nick]['ishere']:
							for key in [nick+key for key in [':',',','>']]:
								if body.count(key):
									col = '*%s*' % str(len(list.keys()) + 1)
									list[col] = key
									body = body.replace(key, col)
						if body.count(nick):
							col2 = '*%s*' % str(len(list.keys()) + 1)
							list[col2] = nick
							body = body.replace(nick, col2)
					rebody = reduce(lambda x,y: en2ru_table.get(x,x)+en2ru_table.get(y,y), body)
					for x in list:
						rebody = rebody.replace(x, list[x])
					msg(source[1], u'turn\->\n%s» %s' % (source[2], rebody))
				else:
					reply(type, source, u'последнее что ты сказал было "turn" :lol:')
			else:
				reply(type, source, u'ты ещё ничего не говорил')
		else:
			reply(type, source, u'Держи: '+reduce(lambda x,y: global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y), body))
	else:
		reply(type, source, u'команда выполняется только в чате')

def handler_turn_save_msg(raw, type, source, body):
	if type == 'public' and source[1] in turn_msgs and source[2] != '':
		jid = handler_jid(source[0])
		if jid in turn_msgs[source[1]] and jid != source[1]:
			turn_msgs[source[1]][jid] = body

def handler_turn_join(conf, nick, afl, role):
	if not conf in turn_msgs:
		turn_msgs[conf] = {}
	jid = handler_jid(conf+'/'+nick)
	if not jid in turn_msgs[conf]:
		turn_msgs[conf][jid] = None

register_message_handler(handler_turn_save_msg)
register_join_handler(handler_turn_join)
register_command_handler(handler_turn_last, 'турн', ['все','разное'], 10, 'Переключает раскладку для последнего сообщения от юзера вызвавшего команду.', 'турн', ['турн'])
