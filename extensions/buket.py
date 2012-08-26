# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  buket_plugin.py

# delirium_plugin.py | Als [Als@exploit.in]
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

def handler_buket(type, source, nick):
	if type == 'public':
		if not nick:
			nick = source[2]
		if nick != handler_botnick(source[1]):
			if nick in GROUPCHATS[source[1]]:
				flowers = eval(read_file('static/buket.txt'))['buket']
				action = random.choice(flowers)
				msg(source[1], u'/me '+action % (nick))
			else:
				reply(type, source, u'кому!? нет таких тут!')
		else:
			reply(type, source, u'Сам себе? Не муди!')
	else:
		reply(type, source, u'Работает только в чате!')

def handler_drink(type, source, nick):
	if type == 'public':
		if not nick:
			nick = source[2]
		if nick != handler_botnick(source[1]):
			if nick in GROUPCHATS[source[1]]:
				alko = eval(read_file('static/buket.txt'))['drink']
				action = random.choice(alko)
				msg(source[1], u'/me '+action % (nick))
			else:
				reply(type, source, u'Кому наливать то? Здесь нет таких! Раскрой глаза алкаш!')
		else:
			reply(type, source, u'Нееэээ я и так буухоай!...')
	else:
		reply(type, source, u'Работает только в чате!')

command_handler(handler_buket, 10, "buket")
command_handler(handler_drink, 10, "buket")
