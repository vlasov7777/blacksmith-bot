#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  delirium_plugin.py

#  Author: Als [Als@exploit.in]
#  Modifications: WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_poke(type, source, nick):
	if type == 'public':
		if nick:
			if not nick == handler_botnick(source[1]):
				if nick in GROUPCHATS[source[1]]:
					pokes = []
					pokes.extend(poke_work(source[1]))
					pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
					repl = random.choice(pokes)
					msg(source[1], u'/me '+repl % (nick))
				else:
					reply(type, source, u'нету его')
			else:
				reply(type, source, u'пшел вон!')
		else:
			reply(type, source, u'мазохист? :D')
	else:
		reply(type, source, u'неа')

def handler_poke_control(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			cmd = args[0].strip().lower()
			if cmd in [u'адд', '+']:
				text = body[(body.find(' ') + 1):].strip()
				if text.count('%s'):
					if poke_work(source[1], 1, text):
						reply(type, source, u'добавлено')
					else:
						reply(type, source, u'больше нельзя')
				else:
					reply(type, source, u'не вижу %s')
			elif cmd in [u'дел', '-']:
				text = args[1].strip()
				if check_number(text):
					if poke_work(source[1], 2, text):
						reply(type, source, u'удалено')
					else:
						reply(type, source, u'такой нет')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		repl, res = '', poke_work(source[1], 3)
		if res:
			res = sorted(res.items(), lambda x,y: int(x[0]) - int(y[0]))
			for num, phrase in res:
				repl += num+') '+phrase+'\n'
			reply(type, source, repl.strip())
		else:
			reply(type, source, u'нет пользовательских фраз')

def poke_work(conf, action = None, phrase = None):
	if check_file(conf, 'delirium.txt'):
		base = 'dynamic/'+conf+'/delirium.txt'
		try:
			pokedb = eval(read_file(base))
		except:
			pokedb = {}
		if action == 1:
			for number in range(1, 21):
				if str(number) not in pokedb:
					pokedb[str(number)] = phrase
					write_file(base, str(pokedb))
					return True
			return False
		elif action == 2:
			if phrase == '0':
				pokedb.clear()
				write_file(base, str(pokedb))
				return True
			elif phrase in pokedb:
				del pokedb[phrase]
				write_file(base, str(pokedb))
				return True
			else:
				return False
		elif action == 3:
			return pokedb
		else:
			pokes = []
			for poke in pokedb.itervalues():
				pokes.append(poke)
			return pokes
	return False

register_command_handler(handler_poke, 'тык', ['фан','все'], 10, 'Тыкает юзера, заставляет его обратить внимание на вас/на чат', 'тык <ник>|<параметр>', ['тык qwerty','тык*'])
register_command_handler(handler_poke_control, 'тык*', ['фан','все'], 20, 'Добавить/удалить пользовательскую фразу, без параметров покажет текущие пользовательские фразы. Переменная %s во фразе обозначает место для вставки ника (обязательный параметр). Фраза должна быть написана от третьего лица, т.к. будет использоваться в виде "/me ваша фраза". max кол-во пользовательских фраз - 20', 'тык* [+/адд/-/дел]', ['тык* + побил %s','тык* - 4','тык*'])
