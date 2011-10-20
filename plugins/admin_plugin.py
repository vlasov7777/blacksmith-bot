# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  admin_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

PRFX_LIST = ['!','@','#','.','*']

def handler_set_prefix(type, source, prefix):
	if source[1] in GROUPCHATS:
		if prefix:
			if prefix.lower() in [u'удалить', 'del', u'дел']:
				if source[1] in PREFIX:
					del PREFIX[source[1]]
					write_file('dynamic/%s/prefix.txt' % (source[1]), "'none'")
					reply(type, source, u'Теперь нет префикса!')
				else:
					reply(type, source, u'Итак нет префикса!')
			elif prefix in PRFX_LIST:
				PREFIX[source[1]] = prefix
				write_file('dynamic/%s/prefix.txt' % (source[1]), '"%s"' % (prefix))
				reply(type, source, u'Знак "%s" отныне является здесь префиксом' % (prefix))
			else:
				reply(type, source, u'Недоступный префикс! Доступные: '+', '.join(PRFX_LIST))
		elif source[1] in PREFIX:
			reply(type, source, u'Знак "%s" является префиксом здесь' % (PREFIX[source[1]]))
		else:
			reply(type, source, u'Префикс не установлен!')
	else:
		reply(type, source, u'Не тупи! Команда только для чата!')

def handler_admin_join(type, source, body):
	if body:
		list = body.split()
		conf = list[0].strip().lower()
		if conf.count('@conference.') and conf.count('.') >= 2:
			if conf not in GROUPCHATS:
				if len(list) == 2:
					code = list[1].strip()
					if code.count('{') and code.count('}'):
						codename = replace_all(code, ['{', '}'], '')
						reason = body[(body.find(code) + (len(code) + 1)):].strip()
					else:
						codename = None
						reason = body[(body.find(' ') + 1):].strip()
				else:
					codename = None
					reason = None
				jid = handler_jid(source[0])
				if jid not in [BOSS, BOSS.lower()]:
					admin_info = u'Внимание! %s (%s) загнал меня в -> "%s"' % (source[2], jid, conf)
					if reason:
						admin_info += u'\nПричина: %s' % (reason)
					delivery(admin_info)
				if codename:
					join_groupchat(conf, handler_botnick(conf), codename)
				else:
					join_groupchat(conf, handler_botnick(conf))
				time.sleep(6)
				if GROUPCHATS.has_key(conf):
					reply(type, source, u'Я зашёл в -> "%s"' % (conf))
					info = u'Я от %s' % (source[2])
					if reason:
						info += '\nReason: %s' % (reason)
					msg(conf, info)
				else:
					reply(type, source, u'Не дополз до -> "%s"...' % (conf))
			else:
				reply(type, source, u'Я итак там! Кончай бухать!')
		else:
			reply(type, source, u'Это не конференция и я туда не пойду')
	else:
		reply(type, source, u'Ну и что же ты хочеш?')

def handler_admin_rejoin(type, source, body):
	if body:
		conf = (body.split()[0]).lower()
	else:
		conf = source[1]
	reason = 'Command "rejoin" from %s' % (source[2])
	if body.count(' '):
		reason += '\nReason: %s' % body[(body.find(' ') + 1):].strip()
	chats = eval(read_file(GROUPCHATS_FILE))
	if chats.has_key(conf):
		leave_groupchat(conf, reason)
		time.sleep(2)
		join_groupchat(conf, handler_botnick(conf), chats[conf]['code'])
		time.sleep(6)
		if GROUPCHATS.has_key(conf):
			reply(type, source, u'Перезашёл!')
		else:
			reply(type, source, u'Не смог перезайти в -> "%s"' % (conf))
	else:
		reply(type, source, u'Меня в "%s" нет и не было!' % (conf))

def handler_admin_leave(type, source, body):
	if body:
		list = body.split()
		conf = list[0].strip().lower()
		if len(list) == 1:
			reason = None
		else:
			reason = body[(body.find(' ') + 1):].strip()
	else:
		reason, conf = None, source[1]
	jid = handler_jid(source[0])
	if not body or jid in ADLIST or conf == source[1]:
		if conf in GROUPCHATS:
			if jid not in [BOSS, BOSS.lower()]:
				admin_info = u'АХТУНГ! %s (%s) выгнал меня из -> "%s"' % (source[2], jid, conf)
				if reason:
					admin_info += u'\nПричина: %s' % (reason)
				delivery(admin_info)
			status = u'Меня уводит %s' % (source[2])
			if reason:
				status += u'\nПричина: %s' % (reason)
			msg(conf, status)
			time.sleep(2)
			leave_groupchat(conf, status)
			if conf != source[1]:
				reply(type, source, u'Я ушёл из -> "%s"' % (conf))
		else:
			reply(type, source, u'Меня итак там нет!')
	else:
		reply(type, source, u'Чё!? Выкуси!')

def handler_admin_restart(type, source, reason):
	status = u'Перезагрузка... Command from %s' % (source[2])
	if reason:
		status += '\nReason: %s' % (reason)
	for conf in GROUPCHATS.keys():
		msg(conf, status)
	time.sleep(6)
	send_unavailable(status)
	call_stage3_init()
	Exit('\n\nRESTARTING...', 0, 5)

def handler_admin_exit(type, source, reason):
	status = u'Выключение... Command from %s' % (source[2])
	if reason:
		status += '\nReason: %s' % (reason)
	for conf in GROUPCHATS.keys():
		msg(conf, status)
	time.sleep(6)
	send_unavailable(status)
	call_stage3_init()
	Exit('\n\n--> BOT STOPPED', 1, 30)

def handler_error_stat(type, source, body):
	if body:
		if check_number(body):
			number = int(body)
			if number in ERRORS:
				error = ERRORS[number]
				try:
					error = unicode(error)
					if type == 'public':
						reply(type, source, u'Глянь в приват')
					msg(source[0], error)
				except:
					reply(type, source, u'Нечитаема! Попробуй посмотреть в крэшлогах')
			else:
				reply(type, source, u'Ошибки №%s не существует!' % (body))
		else:
			reply(type, source, u'Как "%s" может быть номером ошибки если это вообще не число?' % (body))
	else:
		reply(type, source, u'Всего произошло %d ошибок' % len(ERRORS.keys()))

def handler_timeup_info(type, source, body):
	Now_time = time.time()
	start = u'\nВремя работы: %s' % (timeElapsed(Now_time - RUNTIMES['START']))
	restarts = len(RUNTIMES['REST'])
	if restarts:
		rest = (u'\nПоследняя сессия: %s\nВсего %d перезагрузок: ' % (timeElapsed(Now_time - INFO['start']), restarts))+', '.join(sorted(RUNTIMES['REST']))
	else:
		rest = u' - Работаю без перезагрузок!'
	reply(type, source, start+rest)

def handler_botup_info(type, source, body):
	if INFO['start']:
		PID, Now_time = str(BOT_PID), time.time()
		repl = u'\n*// Статистика работы (Bot PID: %s):\n-//- Рабочая сессия %s' % (PID, timeElapsed(Now_time - RUNTIMES['START']))
		if RUNTIMES['REST']:
			repl += u'\n-//- Последняя сессия %s' % (timeElapsed(Now_time - INFO['start']))
		repl += u'\n-//- Обработано %s презенсов и %s iq-запросов\n-//- Отправлено %s сообщений и %s iq-запросов' % (str(INFO['prs']), str(INFO['iq']), str(INFA['outmsg']), str(INFA['outiq']))
		repl += u'\n-//- Произошло %s ошибок и %s Dispatch Errors\n-//- Получено %s сообщений\n-//- Выполнено %s команд' % (str(len(ERRORS.keys())), str(INFO['errs']), str(INFO['msg']), str(INFO['cmd']))
		repl += u'\n-//- Создано файлов %s\n-//- Прочтений файлов %s\n-//- Записей в файлах %s\n-//- Записей crash логов %s' % (str(INFA['fcr']), str(INFA['fr']), str(INFA['fw']), str(INFA['cfw']))
		memory = memory_usage()
		if memory:
			repl += u'\n-//- Потратил %dкб оперативной памяти' % (memory)
		col, acol = 0, 0
		for xthr in threading.enumerate():
			col += 1
			if xthr.isAlive():
				acol += 1
		repl += u'\n-//- Создано %s тредов, %s(%s) из них активно' % (INFO['thr'], acol, col)
		(user, system, atime, itime, jtime,) = os.times()
		repl += u'\n-//- Потратил %.2f секунд процессора\n-//- + %.2f секунд системного времени\n-//- Итог: %.2f секунд общесистемного времени' % (user, system, (user + system))
	else:
		repl = u'Упс попоему я выключен! lol'
	reply(type, source, repl)

def handler_command_stat(type, source, body):
	if body:
		command = body.lower()
		if command in COMMSTAT:
			repl = u'Статистика по команде "%s":\nВсего использовали - %s раз (%s юзеров)' % (command, str(COMMSTAT[command]['col']), str(len(COMMSTAT[command]['users'])))
		else:
			repl = u'Нет статистики по этой "команде"'
	else:
		list = []
		for command in COMMSTAT:
			if COMMSTAT[command]['col']:
				list.append([COMMSTAT[command]['col'], len(COMMSTAT[command]['users']), command])
		list.sort()
		list.reverse()
		repl, col = u'\n[№][Команда][Использований][Юзеров использовало]', 0
		for item in list:
			col = col + 1
			repl += '\n%s. %s - %s (%s)' % (str(col), item[2], str(item[0]), str(item[1]))
			if col >= 20:
				break
	reply(type, source, repl)

def load_conf_prefix(conf):
	if check_file(conf, 'prefix.txt', "'none'"):
		prefix = eval(read_file('dynamic/%s/prefix.txt' % (conf)))
		if prefix != 'none':
			PREFIX[conf] = prefix
	else:
		delivery(u'Внимание! Не удалось создать prefix.txt для "%s"!' % (conf))

register_command_handler(handler_set_prefix, 'префикс', ['админ','все'], 30, 'Установить префикс для команд в конференции (кроме: "хелп", "комлист", "команды", "префикс". - они будут работать и без префикса), без параметров покажет текущий префикс.\nДоступные префиксы: '+', '.join(PRFX_LIST), 'префикс [!/#/./*/удалить/del/дел]', ['префикс !','префикс del'])
register_command_handler(handler_admin_join, 'джойн', ['суперадмин','все'], 80, 'Вход в определённую комнату, если она запаролена пароль следует указать как второй параметр в фигурных скобках', 'джойн [конфа] [{password}] [причина]', ['джойн Witcher@conference.jabber.ru','джойн Witcher@conference.jabber.ru {supercode47} по просьбе овнера'])
register_command_handler(handler_admin_rejoin, 'реджойн', ['суперадмин','все'], 80, 'Перезаход в определённую конфу, без параметра перезайдёт в тут где была вызвана команда', 'реджойн [конференция]', ['реджойн','реджойн Witcher@conference.jabber.ru'])
register_command_handler(handler_admin_leave, 'свал', ['админ','все'], 30, 'Выход из текущей или указанной комнаты', 'свал [конфа] [причина]', ['свал','свал Witcher@conference.jabber.ru мёртвая конфа'])
register_command_handler(handler_admin_restart, 'рестарт', ['суперадмин','все'], 100, 'Рестарт бота', 'рестарт [причина]', ['рестарт','рестарт обновление'])
register_command_handler(handler_admin_exit, 'выкл', ['суперадмин','все'], 100, 'Выключение бота', 'выкл [причина]', ['выкл','выкл обновление'])
register_command_handler(handler_error_stat, 'ошибка', ['суперадмин','все'], 100, 'Без параметров покажет колличество произошедших ошибок, с параметром в виде номера ошибки - покажет ошибку', 'ошибка [№ ошибки]', ['ошибка', 'ошибка 2'])
register_command_handler(handler_timeup_info, 'таймап', ['суперадмин','все'], 20, 'Выдаёт время автономной работы бота + колличество перезагрузок', 'таймап', ['таймап'])
register_command_handler(handler_botup_info, 'ботап', ['админ','все'], 20, 'Выдаёт полную статистику за время работы бота', 'ботап', ['ботап'])
register_command_handler(handler_command_stat, 'комстат', ['инфо','все'], 10, 'Выдаёт статистику по использованию команд, без параметров выдаст топ 20 команд', 'космстат [команда]', ['комастат','комстат пинг'])

register_stage1_init(load_conf_prefix)
