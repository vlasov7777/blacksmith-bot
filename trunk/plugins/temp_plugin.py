# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  temp_plugin.py

# Ported from Neytron by: WitcherGeralt (WitcherGeralt.im@gmail.com)
# http://witcher-team.ucoz.ru/

def handler_convert_temperature(type, source, body):
	if body:
		splitdata = string.split(body)
		try:
			input_value = float(splitdata[0])
			if len(splitdata) >= 2:
				unit_system = splitdata[1][0]
			else:
				unit_system = 'f'
		except ValueError:
			try:
				input_value = float(splitdata[0][:-1])
			except ValueError:
				reply(type, source, 'Syntax Error')
				return
			unit_system = splitdata[0][-1]
		unit_system = string.lower(unit_system)
		if unit_system == 'c':
			repl = '%s F' % str(round(input_value * 9 / 5 + 32, 1))
		else:
			repl = '%s C' % str(round((input_value - 32) * 5 / 9, 1))
	else:
		repl = 'C=(F-32)*5/9 F=C*9/5+32'
	reply(type, source, repl)

register_command_handler(handler_convert_temperature, 'температура', ['все','инфо'], 10, 'Переводит из градусов Цельсия в градусы по Фаркнгейту и наоборот', 'температура [#] [C/F]', ['температура 10 F', 'температура 29 C'])
