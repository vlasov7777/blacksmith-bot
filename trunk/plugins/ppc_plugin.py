# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  ppc_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_ppc(type, source, nick):
	if type == 'public':
		if nick:
			if nick != handler_botnick(source[1]):
				if nick in GROUPCHATS[source[1]]:
					ppc = eval(read_file('static/delirium.txt'))['ppc']
					action = random.choice(ppc)
					msg(source[1], u'/me '+action % (nick))
				else:
					reply(type, source, u'Ты чё слепой!? нету его!')
			else:
				reply(type, source, u'Ща тебя ушатаю!')	
		else:
			reply(type, source, u'отвали хренов мазохист')
	else:
		reply(type, source, u'Нихрена! Только в чате')

def handler_facko(type, source, body):
	if type == 'public':
		if body:
			if body != handler_botnick(source[1]):
				args = body.split()
				if len(args) >= 3:
					HIT = [u'ногой', u'битой', u'кулаком', u'хлыстом', u'молотком', u'палкой с гвоздями', u'кастетом', u'ногой с вертухи', u'кирпичом']
					veapoon = random.choice(HIT)
					nick = args[0].strip()
					part = args[1].strip()
					klich = body[(body.find(part) + (len(part) + 1)):].strip()
					msg(source[1], u'/me с боевым кличем: " %s " - заехал %s %s по %s' % (klich, nick, veapoon, part))
				else:
					reply(type, source, u'Недобор параметров!')
			else:
				reply(type, source, u'Тебя щас наебашу!')
		else:
			reply(type, source, u'Себя заебашить решил?')
	else:
		reply(type, source, u'Нихрена! Только в чате')

register_command_handler(handler_ppc, 'ушатать', ['фан','все'], 10, 'Мочит юзера - "Злой тык"', 'ушатать [nick]', ['ушатать ]{vich'])
register_command_handler(handler_facko, 'мочи',  ['фан','все'], 10, 'Мочит юзера', '\nмочи [ник] [куда бить(в 3ем лице)] [боевой клич]', ['мочи ]{vich голове Спахвати на!!'])
