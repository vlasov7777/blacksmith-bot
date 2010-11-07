# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  timer_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

TCMDS = [u'пинг', u'тест', u'сказать', u'чисть', u'анекдот', u'тык', u'ботап', u'топик', u'призвать', u'участник']

TIMERS = {'col': 0, 'tmrs': {}}

def timer_col():
	col = 0
	for timer in TIMERS['tmrs']:
		if TIMERS['tmrs'][timer].isAlive():
			col = col + 1
	return col

def timer_bust_handler(timer):
	if timer > 86400:
		return u'Больше 24х часов нельзя!'
	elif timer < 60:
		return u'Меньше минуты безсмысленно!'
	return False

def handler_command_timer(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			timer = args[0].strip()
			if check_number(timer):
				jid = handler_jid(source[0])
				timer = int(timer)
				command = args[1].strip().lower()
				error = False
				if command in [u'стоп', 'stop']:
					if jid in ADLIST:
						if timer in TIMERS['tmrs']:
							if TIMERS['tmrs'][timer].isAlive():
								try:
									TIMERS['tmrs'][timer].cancel()
								except:
									error = True
								if error:
									reply(type, source, u'Ошибка! Не удалось остановить таймер!')
								else:
									reply(type, source, u'Таймер остановлен!')
							else:
								reply(type, source, u'Таймер итак уже остановлен!')
						else:
							reply(type, source, u'Нет такого таймера!')
					else:
						reply(type, source, u'Эй! Ты не суперадмин!')
				elif timer_col() <= 15:
					bust = timer_bust_handler(timer)
					if bust:
						reply(type, source, bust)
					elif command in TCMDS or jid == (BOSS or BOSS.lower()):
						if len(args) >= 3:
							Params = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
						else:
							Params = ''
						if len(Params) <= 96:
							if COMMANDS.has_key(command):
								if COMMAND_HANDLERS.has_key(command):
									NUM = len(TIMERS['tmrs']) + 1
									handler = COMMAND_HANDLERS[command]
									TIMERS['tmrs'][NUM] = threading.Timer(timer, execute_command_handler,(handler, command, type, source, Params))
									try:
										TIMERS['tmrs'][NUM].start()
									except:
										error = True
									if error:
										try:
											del TIMERS['tmrs'][NUM]
										except:
											LAST['null'] += 1
										reply(type, source, u'Ошибка! Не удалось создать таймер!')
									else:
										TIMERS['col'] += 1
										reply(type, source, u'Через %s выполню твою команду' % timeElapsed(timer))
							else:
								reply(type, source, u'нет такой команды')
						else:
							reply(type, source, u'слишком длинные параметры')
					else:
						reply(type, source, u'таймер на эту команду для тебя недоступен\nДоступны следующие таймеры: '+', '.join(sorted(TCMDS)))
				else:
					reply(type, source, u'Сейчас активно 16 таймеров, больше нельзя!')
			else:
				reply(type, source, u'Ты указал неверное число!')
		else:
			reply(type, source, u'Инвалид синтакс!')
	else:
		alive = ''
		for timer in TIMERS['tmrs']:
			if TIMERS['tmrs'][timer].isAlive():
				alive += str(timer)+' *'
		if alive:
			list = u' таймеров\n- %s из них активно активно (PIDs): %s' % (str(timer_col()), alive)
		else:
			list = u' таймеров - все завершены'
		if TIMERS['col'] != 0:
			repl = u'\nВсего было активировано '+str(TIMERS['col'])+list
		else:
			repl = u'Пока небыло активировано ни одного таймера'
		reply(type, source, repl)

register_command_handler(handler_command_timer, 'таймер', ['все','разное'], 20, 'Устанавливает таймер (время в секундах) на выполнение команды.\nДля BOSS`а доступны все команды для запуска таймера, также глобальные админы могут остановить любой таймер (таймер [№] стоп)\nЕсли вы не BOSS, то для вас доступны только следующие команды: '+', '.join(sorted(TCMDS)).encode('utf-8'), 'таймер [время/номер таймера] [команда]', ['таймер 86400 сказать да здравствует новый день!','таймер 43200 ботап'])
