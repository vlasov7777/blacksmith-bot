# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  new_year_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_new_year(type, source, body):
	months = {'01': 0, '02': 31, '03': 59, '04': 90, '05': 120, '06': 151, '07': 181, '08': 212, '09': 243, '10': 273, '11': 304, '12': 334}
	tt = (time.strftime('%m/%d/%H/%M/%S', time.gmtime())).split('/')
	repl = u'До нового года (по GMT) осталось - '
	days = 365 - (months[tt[0]] + int(tt[1]))
	if days:
		repl += str(days)
		repl += u' дн '
	hours = 23 - int(tt[2])
	if hours:
		repl += str(hours)
		repl += u' час '
	mins = 59 - int(tt[3])
	if mins:
		repl += str(mins)
		repl += u' мин '
	secs = (59 - int(tt[4])) + 1
	if secs:
		repl += str(secs)
		repl += u' сек'
	reply(type, source, repl)

register_command_handler(handler_new_year, 'нг', ['все','фан'], 10, 'Показывает сколько осталось до нового года (по Гринвичу)', 'нг', ['нг'])
