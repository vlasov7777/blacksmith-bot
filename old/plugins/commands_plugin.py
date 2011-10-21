# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  commands_plugin.py

# Idea: 40tman (40tman@qip.ru)
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_commands(type, source, body):
	if body:
		if body.count('/'):
			if body.count('/') <= 3:
				list = body.split('/')
				for cmd in list:
					if cmd != '/':
						args = cmd.split()
						command = args[0].strip().lower()
						if len(args) >= 2:
							Parameters = cmd[(cmd.find(' ') + 1):].strip()
						else:
							Parameters = ''
						if len(Parameters) <= 96:
							if COMMANDS.has_key(command):
								if cmd != list[0]:
									time.sleep(2)
								call_command_handlers(command, type, source, Parameters, command)
							else:
								reply(type, source, u'нет такой команды!')
						else:
							reply(type, source, u'слишком длинные параметры!')
			else:
				reply(type, source, u'больше 4х нельзя!')
		else:
			reply(type, source, u'инвалид синтакс!')
	else:
		reply(type, source, u'чего хочешь то?')

register_command_handler(handler_commands, 'командс', ['все','разное'], 20, 'Выполняет до четырёх команд одновременно', 'командс or * [cmd 1]/[cmd 2]', ['командс тест/пинг','* тест/пинг'])
register_command_handler(handler_commands, '*', ['разное'], 20, 'Выполняет до четырёх команд одновременно', '* [cmd 1]/[cmd 2]', ['* тест/пинг'])
