# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  help_plugin.py

# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_comaccess(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			access = COMMANDS[command]['access']
			reply(type, source, u'Доступ к команде "'+command+'" = '+str(access))
		else:
			reply(type, source, u'нет такой команды')
	else:
		reply(type, source, u'Команды "None" не существует! lol')

def handler_help_help(type, source, body):
	if body:
		command = body.lower()
		if len(command) <= 24:
			if command in COMMANDS:
				mess = COMMANDS[command]['desc'].decode('utf-8')+u'\nКатегории: '
				mess += ', '.join(COMMANDS[command]['category']).decode('utf-8')
				mess += u'\nИспользование: '+COMMANDS[command]['syntax'].decode('utf-8')+u'\nПримеры:'
				for example in COMMANDS[command]['examples']:
					mess += '\n  >>  '+example.decode('utf-8')
				mess += u'\nНеобходимый уровень доступа: '+str(COMMANDS[command]['access'])
			else:
				mess = u'Нет такой команды, чтобы узнать точный список напиши "комлист"'
		else:
			mess = u'Команды длинне 24х символов точно не существует!'
	else:
		mess = u'Для просмотра команд напишите: "комлист" - вывод списка с разбивкой по доступам или "команды" - вывод списков по категориям, а также напишите "хелп" [команда] для получения помощи по команде'
	reply(type, source, mess)

def handler_command_list(type, source, body):
	acc100 = acc80 = acc30 = acc20 = acc15 = acc10 = list()
	cat = (u'все').encode('utf-8')
	if source[1] in PREFIX:
		pfx = u' (Командный префикс - "'+PREFIX[source[1]]+'"):'
	else:
		pfx = ':'
	for cmd in COMMANDS:
		if cat in COMMANDS[cmd]['category']:
			if COMMANDS[cmd]['access'] == 100:
				acc100.append(cmd)
			elif COMMANDS[cmd]['access'] == 80:
				acc80.append(cmd)
			elif COMMANDS[cmd]['access'] == 30:
				acc30.append(cmd)
			elif COMMANDS[cmd]['access'] == 20:
				acc20.append(cmd)
			elif COMMANDS[cmd]['access'] == 15:
				acc15.append(cmd)
			elif COMMANDS[cmd]['access'] == 10:
				acc10.append(cmd)
	superadmins = u'\n\n### Команды для Суперадмина (доступ 100) - '+str(len(acc100)+len(acc80)+len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
	chiefs = u'\n\n### Команды для Глоб.Админа (доступ 80) - '+str(len(acc80)+len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
	owners = u'\n\n### Команды  для Владельцев (доступ 30) - '+str(len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
	admins = u'\n\n### Команды для Админов (доступ 20) - '+str(len(acc20)+len(acc15)+len(acc10))+':\n'
	moders = u'\n\n### Команды для Модеров (доступ 15) - '+str(len(acc15)+len(acc10))+':\n'
	users = u'\n\n### Команды для Участников (доступ 10) - '+str(len(acc10))+':\n'
	level = u'\n\n### Твой уровень  доступа: '
	access = user_level(source[0], source[1])
	if access == 100:
		level += u'100 (BOSS) - тебе доступны все команды'
	elif access == 80:
		level += u'80 (Chief) - тебе доступны все команды кроме суперадминских'
	elif access == 30:
		level += u'30 (Овнер) - вам доступны все команды с доступом до 30 (включительно)'
	elif access == 20:
		level += u'20 (Админ) - вам доступны команды с доступом до 20 (включительно)'
	elif access == 15 or access == 16:
		level += u'15 (Модер) - вам доступны команды для участников + пара модерских'
	elif access == 10 or access == 11:
		level += u'10 (Участник) - вам доступны команды только низшего уровня доступа (10)'
	else:
		level += u'%s - нестандартный доступ, я *dntknw* на что ты способен' % str(access)
	acc100.sort(), acc80.sort(), acc30.sort(), acc20.sort(), acc15.sort(), acc10.sort()
	boss, friend, owner, admin, moder, user = ', '.join(acc100), ', '.join(acc80), ', '.join(acc30), ', '.join(acc20), ', '.join(acc15), ', '.join(acc10)
	if type == 'public':
		reply(type, source, u'ушел')
	reply('private', source, u'Полный спикок команд'+pfx+superadmins+boss+chiefs+friend+owners+owner+admins+admin+moders+moder+users+user+level)

def handler_help_commands(type, source, body):
	if body:
		if source[1] in PREFIX:
			pfx = u'\n--> Командный префикс - "'+PREFIX[source[1]]+'"'
		else:
			pfx = ''
		repl, dsbl = [], []
		all = 0
		total = 0
		cmdcat = body.encode('utf-8')
		catcom = set([((cmdcat in COMMANDS[cmd]['category']) and cmd) or None for cmd in COMMANDS]) - set([None])
		if catcom:
			for cat in catcom:
				all = all + 1
				if source[1] in COMMOFF and cat in COMMOFF[source[1]]:
					dsbl.append(cat)
				else:
					repl.append(cat)
					total = total + 1
			if repl:
				if type == 'public':
					reply(type, source, u'ушли')
				repl.sort()
				answ = u'Список команд в категории "'+body+'" ('+str(total)+u' штук):\n\n'+', '.join(repl)+pfx+u'\n\nСписок команд с разбивкой по доступам по команде "комлист"\nЧтобы узнать доступ к определённой команде напишишите "комдоступ" [команда]'
				if dsbl:
					dsbl.sort()
					answ += u'\n\nСледующие команды здесь отключены ('+str(len(dsbl))+u' штук):\n\n'+', '.join(dsbl)
				reply('private', source, answ)
			else:
				reply(type, source, u'неа')
		else:
			reply(type, source, u'а есть и такая?')
	else:
		cats = set()
		for cmd in [COMMANDS[cmd]['category'] for cmd in COMMANDS]:
			cats = cats | set(cmd)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type, source, u'ушли')
		reply('private', source, u'Список категорий команд: \n'+cats+u'\n\nДля просмотра списка команд в категории наберите "команды" [нужная категория]')

register_command_handler(handler_comaccess, 'комдоступ', ['все','инфо'], 10, 'Узнать доступ к определённой команде', 'комдоступ [команда]', ['комдоступ ботник'])
register_command_handler(handler_help_help, 'хелп', ['все','инфо'], 10, 'Даёт основную справку или посылает информацию об определённой команде.', 'хелп [команда]', ['хелп', 'хелп авторизация'])
register_command_handler(handler_command_list, 'комлист', ['все','инфо'], 10, 'Выдаёт полный список команд с разбивкой по доступам.', 'комлист', ['комлист'])
register_command_handler(handler_help_commands, 'команды', ['все','инфо'], 10, 'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', 'команды [категория]', ['команды','команды все'])
