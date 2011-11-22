#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman Bot plugin
#  udalit_plugin.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

UDl = False

def handler_user_del(type, source, body):
	if source[1] in GROUPCHATS and source[2] != '':
		if int(user_level(source[0], source[1])) >= 15:
			reply(type, source, u'только для немодеров')
		elif UDl == False:
			globals()['UDl'] = True
			if source[2] in GROUPCHATS[source[1]]:
				col = 0
				while GROUPCHATS[source[1]][source[2]]['ishere']:
					col += 1
					if col >= 100:
						globals()['UDl'] = False
						handler_kick(source[1], source[2], 'error 404: not found')
						break
					JCON.send(xmpp.protocol.Message(source[0], u'удаление начато! Во избежания прерывания дождитесь окончания процесса. Всего удалено: '+str(col)+'%','chat'))
		else:
			reply(type, source, u'попробуй чуть позже')
	else:
		reply(type, source, u'Много хочешь')

command_handler(handler_user_del, 10, "udalit")
