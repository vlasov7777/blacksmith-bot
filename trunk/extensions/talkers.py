# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  talkers_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

TALKERS = {}

def handler_talkers(type, source, body):
	if body:
		if source[1] in GROUPCHATS:
			args = body.split()
			if len(args) >= 2:
				seckey, key = body[(body.find(' ') + 1):].strip(), args[0].strip().lower()
				if key in [u'топ', 'top']:
					if seckey in [u'локальный', 'local']:
						list = []
						for jid in TALKERS[source[1]]['jids']:
							nick = TALKERS[source[1]]['jids'][jid]['lastnick']
							msgs = TALKERS[source[1]]['jids'][jid]['msgs']
							words = TALKERS[source[1]]['jids'][jid]['words']
							list.append([msgs, words, nick])
						list.sort()
						list.reverse()
						col = 0
						repl = u'\n[№][Юзер][Фраз][Слов][Коэф.]'
						for item in list:
							col = col + 1
							repl += '\n'+str(col)+'. '+item[2]+'\t\t'+str(item[0])+'\t'+str(item[1])+'\t'+str(round((round(item[1]) / round(item[0])), 1))
							if col >= 10:
								break
					elif seckey in [u'глобальный', 'global']:
						globlist = {}
						for conf in TALKERS.keys():
							for jid in TALKERS[conf]['jids']:
								nick = TALKERS[conf]['jids'][jid]['lastnick']
								msgs = TALKERS[conf]['jids'][jid]['msgs']
								words = TALKERS[conf]['jids'][jid]['words']
								if jid in globlist:
									globlist[jid]['msgs'] += msgs
									globlist[jid]['words'] += words
								else:
									globlist[jid] = {'lastnick': nick,'msgs': msgs, 'words': words}
						list = []
						for jid in globlist:
							msgs = globlist[jid]['msgs']
							nick = globlist[jid]['lastnick']
							words = globlist[jid]['words']
							list.append([msgs, words, nick])
						list.sort()
						list.reverse()
						col = 0
						repl = u'\n[№][Юзер][Фраз][Слов][Коэф.]'
						for item in list:
							col = col + 1
							repl += '\n'+str(col)+'. '+item[2]+'\t\t'+str(item[0])+'\t'+str(item[1])+'\t'+str(round((round(item[1]) / round(item[0])), 1))
							if col >= 20:
								break
					else:
						repl = u'Топ чего?'
				elif key in [u'глобальный', 'global']:
					if seckey in [u'мой', 'my']:
						jid = handler_jid(source[0])
						msgs = 0
						words = 0
						for conf in TALKERS.keys():
							if jid in TALKERS[conf]['jids']:
								msgs += TALKERS[conf]['jids'][jid]['msgs']
								words += TALKERS[conf]['jids'][jid]['words']
						if msgs != 0:
							repl = u'\n[Фраз][Слов][Коэф.]\n'+str(msgs)+'\t'+str(words)+'\t'+str(round((round(words) / round(msgs)), 1))
						else:
							repl = u'На тебя нет статистики...'
					elif seckey.count('@') and seckey.count('.') or seckey in GROUPCHATS[source[1]]:
						if seckey in GROUPCHATS[source[1]]:
							jid = handler_jid(source[1]+'/'+seckey)
						else:
							jid = seckey
						msgs = 0
						words = 0
						for conf in TALKERS.keys():
							if jid in TALKERS[conf]['jids']:
								msgs += TALKERS[conf]['jids'][jid]['msgs']
								words += TALKERS[conf]['jids'][jid]['words']
						if msgs != 0:
							repl = u'\n[Фраз][Слов][Коэф.]\n'+str(msgs)+'\t'+str(words)+'\t'+str(round((round(words) / round(msgs)), 1))
						else:
							repl = u'На него нет статистики...'
					else:
						repl = u'Это не жид и юзера с таким ником я здесь не видел!'
				elif key in [u'локальный', 'local']:
					if seckey in [u'мой', 'my']:
						jid = handler_jid(source[0])
						if jid in TALKERS[source[1]]['jids']:
							msgs = TALKERS[source[1]]['jids'][jid]['msgs']
							words = TALKERS[source[1]]['jids'][jid]['words']
							repl = u'\n[Фраз][Слов][Коэф.]\n'+str(msgs)+'\t'+str(words)+'\t'+str(round((round(words) / round(msgs)), 1))
						else:
							repl = u'Помоему ты ниразу ничего не сказал...'
					elif seckey.count('@') and seckey.count('.') or seckey in GROUPCHATS[source[1]]:
						if seckey in GROUPCHATS[source[1]]:
							jid = handler_jid(source[1]+'/'+seckey)
						else:
							jid = seckey
						if jid in TALKERS[source[1]]['jids']:
							msgs = TALKERS[source[1]]['jids'][jid]['msgs']
							words = TALKERS[source[1]]['jids'][jid]['words']
							repl = u'\n[Фраз][Слов][Коэф.]\n'+str(msgs)+'\t'+str(words)+'\t'+str(round((round(words) / round(msgs)), 1))
						else:
							repl = u'Помоему он ниразу ничего не сказал...'
					else:
						repl = u'Это не жид и юзера с таким ником я здесь не видел!'
				else:
					repl = u'Читай помощь по команде!'
			else:
				repl = u'Читай помощь по команде!'
		else:
			repl = u'Команда доступна только в конференции!'
	else:
		repl = u'Читай помощь по команде!'
	reply(type, source, repl)

def handler_talkers_register(raw, type, source, body):
	if type == 'public' and source[2] != '':
		jid, words = handler_jid(source[0]), body.split()
		if jid in TALKERS[source[1]]['jids']:
			TALKERS[source[1]]['jids'][jid]['lastnick'] = source[2]
			TALKERS[source[1]]['jids'][jid]['msgs'] += 1
			TALKERS[source[1]]['jids'][jid]['words'] += len(words)

		else:
			TALKERS[source[1]]['jids'][jid] = {'lastnick': source[2], 'msgs': 1, 'words': len(words)}
		TALKERS[source[1]]['msgs'] += 1
		if TALKERS[source[1]]['msgs'] >= 32:
			TALKERS[source[1]]['msgs'] = 0
			write_file('dynamic/'+source[1]+'/talkers.txt', str(TALKERS[source[1]]['jids']))

def talkers_save():
	for conf in TALKERS.keys():
		if TALKERS[conf]['msgs']:
			write_file('dynamic/'+conf+'/talkers.txt', str(TALKERS[conf]['jids']))

def talkers_init(conf):
	TALKERS[conf] = {'msgs': 0, 'jids': {}}
	if check_file(conf, 'talkers.txt'):
		TALKERS[conf]['jids'] = eval(read_file('dynamic/'+conf+'/talkers.txt'))
	else:
		delivery(u'Внимание! Не удалось создать talkers.txt для "%s"!' % (conf))

register_message_handler(handler_talkers_register)
command_handler(handler_talkers, 10, "talkers")
register_stage3_init(talkers_save)

register_stage1_init(talkers_init)
