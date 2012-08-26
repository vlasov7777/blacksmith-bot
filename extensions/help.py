# BS mark.1-55
# coding: utf-8

#  BlackSmith plugin
#  help_plugin.py

# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def command_comaccess(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			access = COMMANDS[command]['access']
			reply(type, source, u'Доступ к команде "'+command+'" = '+str(access))
		else:
			reply(type, source, u'нет такой команды')
	else:
		reply(type, source, u'Команды "None" не существует! lol')

def command_help(type, source, body):
	if body:
		command = body.lower()
		if len(command) <= 24:
			if command in COMMANDS:
				try:
					if COMMANDS[command].has_key('desc'):
						fr = COMMANDS[command]
					else:
						plug = COMMANDS[command]['plug']
						inst = COMMAND_HANDLERS[command].func_name
						fr = eval(read_file("help/%s" % plug).decode("utf-8"))[inst]
					mess = fr['desc']
					mess += u'\nИспользование: '+fr['syntax']+u'\nПримеры:'
					for example in fr['examples']:
						mess += '\n  >>  '+example
					mess += u'\nНеобходимый уровень доступа: '+str(COMMANDS[command]['access'])
				except:
					mess = u'нет хелпа'
			else:
				mess = u'Нет такой команды, чтобы узнать точный список напиши "комлист"'
		else:
			mess = u'Команды длинне 24х символов точно не существует!'
	else:
		mess = u'Для просмотра команд напишите "комлист"'
	reply(type, source, mess)

def command_comlist(type, source, body):
	acc100, acc80, acc30, acc20, acc15, acc10 = [], [], [], [], [], []
	if source[1] in PREFIX:
		pfx = u' (Командный префикс - "'+PREFIX[source[1]]+'"):'
	else:
		pfx = ':'
	for cmd in COMMANDS:
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
	msg(source[0], u'Полный спикок команд'+pfx+superadmins+boss+chiefs+friend+owners+owner+admins+admin+moders+moder+users+user+level)


def command_commands(type, source, body):
	answer = u"\nСписок команд в категории \"все\" (всего %d штук):\n\n%s." % (len(COMMANDS.keys()), ", ".join(sorted(COMMANDS.keys())))
	if len(COMMOFF.get(source[1], [])):
		answer += u"\n\nСледующие команды здесь отключены: \n%s." % ", ".join(sorted(COMMOFF.get(source[1], [])))
	answer += u"\n\n*** Чтобы узнать доступ к определённой команде, напишите \"комдоступ [команда]\"."
	if PREFIX.get(source[1]):
		answer += u"\n*** Префикс команд: \"%s\"." % PREFIX.get(source[1])
	if type != "private":
		reply(type, source, u"В привате.")	
	msg(source[0], answer)


command_handler(command_comaccess, 10, "help")
command_handler(command_help, 10, "help")
command_handler(command_comlist, 10, "help")
command_handler(command_commands, 10, "help")
