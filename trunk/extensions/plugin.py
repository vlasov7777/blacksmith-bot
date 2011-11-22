# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  plugin_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

OUT_COMMANDS = {}

def handler_out_list(type, source):
	if OUT_COMMANDS:
		repl = u'Список отключённых команд: '+', '.join(sorted(OUT_COMMANDS.keys()))
	else:
		repl = u'Оключённых команд нет!'
	reply(type, source, repl)

def handler_command_out(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			OUT_COMMANDS[command] = COMMANDS[command]
			del COMMANDS[command]
			reply(type, source, u'Команда "%s" глобально отключена' % (command))
		else:
			reply(type, source, u'нет такой команды')
	else:
		handler_out_list(type, source)

def handler_from_out_com(type, source, body):
	if body:
		command = body.lower()
		if command in OUT_COMMANDS:
			COMMANDS[command] = OUT_COMMANDS[command]
			del OUT_COMMANDS[command]
			reply(type, source, u'Команда "%s" включена' % (command))
		else:
			reply(type, source, u'в базе возврата нет этой команды')
	else:
		handler_out_list(type, source)

def handler_plug_list(type, source, body):
	ltc, tal, Ypl, Npl = [], [], [], []
	for Plugin in os.listdir(PLUGIN_DIR):
		Ext = Plugin[-3:].lower()
		if Ext == '.py':
			try:
				data = open('%s/%s' % (PLUGIN_DIR, Plugin)).read(20)
			except:
				data = str()
			Plug = Plugin.split('.')
			if data.count('# BS mark.1'):
				ltc.append(Plug[0]); Ypl.append(Plugin)
			elif data.count('talis'):
				tal.append(Plug[0]); Ypl.append(Plugin)
			else:
				Npl.append(Plug[0])
	if body == 'get_valid_plugins':
		return sorted(Ypl)
	else:
		repl = ''
		if ltc:
			repl += u'\nДоступно %d плагинов BlackSmith бота:\n' % len(ltc)
			repl += ', '.join(sorted(ltc))
		if tal:
			repl += u'\nДоступно %d плагинов Talisman бота:\n' % len(tal)
			repl += ', '.join(sorted(tal))
		if Npl:
			repl += u'\nВнимание! Вналичии %d недоступных плагинов:\n' % len(Npl)
			repl += ', '.join(sorted(Npl))
		reply(type, source, repl)

def handler_load_plugin(type, source, body):
	if body:
		Plugin = '%s.py' % body.lower()
		if Plugin in handler_plug_list(type, source, 'get_valid_plugins'):
			try:
				execfile('%s/%s' % (PLUGIN_DIR, Plugin))
				repl = u'Плагин %s был успешно подгружен!' % (Plugin)
			except:
				exc = sys.exc_info()
				repl = u'Плагин %s не был подгружен!\nОшибка: %s:\n%s' % (Plugin, exc[0].__name__, exc[1])
		else:
			repl = u'Этот плагин не был найден в списке'
	else:
		repl = u'Если незнаеш чего грузить - глянь список (команда: плаг_лист)'
	reply(type, source, repl)

command_handler(handler_from_out_com, 100, "plugin")
command_handler(handler_command_out, 100, "plugin")
command_handler(handler_plug_list, 80, "plugin")
command_handler(handler_load_plugin, 100, "plugin")
