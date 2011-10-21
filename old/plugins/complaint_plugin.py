#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  complaint_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

def handler_complaint(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			if type == 'private':
				args = body.split()
				if len(args) >= 2:
					nick = args[0].strip()
					if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
						if user_level(source[1]+'/'+nick, source[1]) < 20:
							body = body[(body.find(' ') + 1):].strip()
							if len(nick) <= 16 and len(body) <= 96:
								for admin in GROUPCHATS[source[1]]:
									jid = source[1]+'/'+admin
									if user_level(jid, source[1]) >= 20:
										msg(jid, (u'Юзер "%s" жалуется на "%s" \nПричина: ' % (source[2], nick))+body)
								reply(type, source, u'жалоба была разослана всем админам')
							else:
								reply(type, source, u'Слишком много написал!')
						else:
							reply(type, source, u'Даже не думай! Он админ!')
					else:
						reply(type, source, u'Я непонимаю на кого ты жалуешся...')
				else:
					reply(type, source, u'Ну а дальше?')
			else:
				reply(type, source, u'Работает только в привате!')
		else:
			reply(type, source, u'Ну а дальше?')
	else:
		reply(type, source, u'ты дурак или притворяешся?')
				
register_command_handler(handler_complaint, 'жалоба',  ['все','разное'], 10, 'Пожаловаться на определённый ник по определённой причине. Работает только у меня в привате!', 'жалоба [ник] [причина]', ['жалоба Nick7 спам'])
