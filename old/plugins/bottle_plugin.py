# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  bottle_plugin.py

# Idea: 40tman (40tman@qip.ru)
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_bottle(type, source, player):
	if type == 'public':
		if not player:
			player = source[2]
		botnick = handler_botnick(source[1])
		if player != botnick:
			if player in GROUPCHATS[source[1]]:
				GAME = []
				for chuvak in GROUPCHATS[source[1]]:
					if GROUPCHATS[source[1]][chuvak]['ishere']:
						if chuvak != player and chuvak != botnick:
							GAME.append(chuvak)
				if len(GAME) != 0:
					user = random.choice(GAME)
					msg(source[1], u'/me закрутил бутылочку... Она указала на -> '+user)
					cache = []
					cache.extend(eval(read_file('static/bottle.txt')))
					try:
						base = eval(read_file('dynamic/'+source[1]+'/bottle.txt'))
					except:
						base = {}
					for key in base:
						cache.append(base[key])
					action = random.choice(cache)
					repl = replace_all(action, {'%NICK%': player, '%USER%': user})
					list = [':lol:', '*ROFL*', ':D', '*crazy*', u'УуааАхАХа!!', u'ЫЫыы', u'Бгг', u'Гг', u'ГЫы', u'БууГага']
					lol = random.choice(list)
					time.sleep(2)
					msg(source[1], u'Сейчас:\n'+repl+'\n'+lol)
				else:
					reply(type, source, u'Блин я последнюю бутылку разбил!')
			else:
				reply(type, source, u'Ты чё слепой!? нету его!')
		else:
			reply(type, source, u'Пошел вон! я не играю!')	
	else:
		reply(type, source, u'Нихрена! Только в чате')

def handler_bottle_control(type, source, body):
	if source[1] in GROUPCHATS:
		bottle_file = 'dynamic/'+source[1]+'/bottle.txt'
		try:
			base = eval(read_file(bottle_file))
		except:
			base = {}
		if body:
			args = body.split()
			if len(args) >= 2:
				check = args[0].strip()
				if check == '+':
					text = body[(body.find(' ') + 1):].strip()
					if body.count('%NICK%') and body.count('%USER%'):
						if len(text) <= 256:
							if len(base.keys()) <= 24:
								for number in range(1, 25):
									if str(number) not in base:
										base[str(number)] = text
										break
								write_file(bottle_file, str(base))
								reply(type, source, u'записано')
							else:
								reply(type, source, u'больше 24х вариантов нельзя')
						else:
							reply(type, source, u'слишком многа текста (лимит 256 знаков)')
					else:
						reply(type, source, u'%NICK% и %USER% - обязательные аргументы!')
				elif check == '-':
					text = args[1].strip()
					if check_number(text):
						if base.has_key(text):
							del base[text]
							write_file(bottle_file, str(base))
							reply(type, source, u'удалено')
						else:
							reply(type, source, u'нет такой записи')
					else:
						reply(type, source, u'это вообще не число!')
				else:
					reply(type, source, u'вообще чёто не то пишеш')
			else:
				reply(type, source, u'недобор аргументов')
		elif len(base.keys()) != 0:
			repl, list = '\n', sorted(base.items(), lambda x,y: int(x[0]) - int(y[0]))
			for x, z in list:
				repl += x+') '+z+'\n'
			reply(type, source, repl)
		else:
			reply(type, source, u'база пуста!')
	else:
		reply(type, source, u'Нихрена! Только в чате')

def bottle_init(conf):
	if not check_file(conf, 'bottle.txt'):
		delivery(u'Внимание! Не удалось создать bottle.txt для "%s"!' % (conf))

register_command_handler(handler_bottle, 'бутыль', ['фан','все'], 10, 'Игра в бутылочку', 'бутыль [nick]', ['бутыль','бутыль Evgen'])
register_command_handler(handler_bottle_control, 'бутыль*',  ['фан','все'], 20, 'Устанавливает/удаляет фразы для игры в бутылочку, при установлении фразы - параметры должны содержать %USER% (место для вставки случайного юзера) и %NICK% (место для вставки ника играющего юзера), без параметров покажет фразы из базы', 'бутыль* [+/-] [параметры]', ['бутыль* + %NICK% кусает %USER% за ухо','бутыль* - 2', 'бутыль*'])

register_stage1_init(bottle_init)
