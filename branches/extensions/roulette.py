#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  roulette_plugin.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_roulette_one(type, source, nick):
	if source[1] in GROUPCHATS:
		if nick:
			if not user_level(source[0], source[1]) < 15 and nick != source[2]:
				reply(type, source, u'ты можешь стрелять только в себя')
				return
			if not nick in GROUPCHATS[source[1]] or not GROUPCHATS[source[1]][nick]['ishere']:
				reply(type, source, u'юзера с таким ником здесь нет')
				return
		else:
			nick = source[2]
		if user_level(source[1]+'/'+nick, source[1]) < 15:
			if random.randrange(1, 3) == 2:
				handler_kick(source[1], source[2], u'мозги забрызгали стены...')
			else:
				reply(type, source, u'пронесло...')
		else:
			reply(type, source, u'не поднимается рука в модера стрелять')
	else:
		reply(type, source, u'осечка...')

command_handler(handler_roulette_one, 10, "roulette")
