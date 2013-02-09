# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
	
BLACK_LIST = 'dynamic/blacklist.txt'

CHAT_CACHE = {}
AMSGBL = []
CHAT_DIRTY = {}

def handler_chat_cache(stanza, ltype, source, body):
	try:
		subject = stanza.getTag('subject')
	except:
		subject = False
	if ltype != 'public' or subject or not source[2]:
		return
	header = u'[%s] %s» ' % (time.strftime('%H:%M:%S (%d.%m.%Y) GMT', time.gmtime()), source[2])
	CHAT_CACHE[source[1]]['1'] = CHAT_CACHE[source[1]]['2']
	if len(body) > 256:
		body = body[:256]+'[...]'
	CHAT_CACHE[source[1]]['2'] = header+body

def handler_clean(type, source, body):
	if GROUPCHATS.has_key(source[1]):
		if CHAT_DIRTY[source[1]]:
			CHAT_DIRTY[source[1]] = False
			if type != 'private':
				change_bot_status(source[1], u"Чистка...", "dnd")
			zero = xmpp.Message(to = source[1], typ = "groupchat")
			for Numb in xrange(24):
				if not GROUPCHATS.has_key(source[1]):
					return
				try:
					jClient.send(zero)
				except IOError:
					return
				INFO['outmsg'] += 1
				if (Numb != 23):
					time.sleep(1.4)
			if type != 'private':
				message = STATUS[source[1]]['message']
				status = STATUS[source[1]]['status']
				change_bot_status(source[1], message, status)
			CHAT_CACHE[source[1]] = {'1': '', '2': ''}
			CHAT_DIRTY[source[1]] = True
		else:
			reply(type, source, u'и так чищу!')
	else:
		reply(type, source, u'сам свой ростер чисть!')

def last_chat_cache(type, source, body):
	confs = GROUPCHATS.keys()
	confs.sort()
	if body:
		body = body.lower()
		if body in confs:
			conf = body
		elif check_number(body):
			number = int(body) - 1
			if number >= 0 and number <= len(confs):
				conf = confs[number]
			else:
				conf = False
		else:
			conf = False
		if conf:
			cache = ''
			if CHAT_CACHE[conf]['1']:
				cache += '\n'+CHAT_CACHE[conf]['1']
			if CHAT_CACHE[conf]['2']:
				cache += '\n'+CHAT_CACHE[conf]['2']
			if not cache:
				cache = u'пусто'
			reply(type, source, cache)
		else:
			reply(type, source, u'меня там нет!')
	else:
		col, list = 0, ''
		for conf in confs:
			col = col + 1
			list += u'\n№ '+str(col)+'. - '+conf
		reply(type, source, list)

def handler_test(type, source, body):
	if time.localtime()[1:3] == (4, 1):
		testfr = [u"КОТЭ ОПАСНОСТЕ!!11", u"ТЕЛОИД11111", 
				u"ГОЛАКТЕГО ОПАСНОСТЕ1111", u"ПЫЫщщщщщЩЩЬ!!111", u"АДИНАДИН!!!!"
				u"ЪЖСЛО111", u"ЧАКЕ НЕГОДУЕ......", u"ОНОТОЛЕ СЕРЧАЕ.", u"КОТЭ РАДУЕ!1", u"ПИПЛ ШОкЕ11"]
		answer = random.choice(testfr)
	else:
		testfr = {0: u"Всё в порядке! (Ошибок нет)",
				  1: u"Что-то сломалось... (1 ошибка)",
				  2: u"Что-то сломалось дважды... (2 ошибки)",
				  3: u"Что-то сломалось дважды и ещё раз сломалось... (3 ошибки) (!)",
				  4: u"Плоховато мне, перезапуститься бы... (4 ошибки) (!!)",
				  "more": u"Сегодня явно не мой день (%d ошибок) (!!!)"}
		answer = testfr.get(INFO["errs"], testfr["more"])
		
	reply(type, source, answer + (' (PID: %s)' % str(BOT_PID)))

def handler_admin_message(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			jid = args[0].strip()
			if jid.count('@') and jid.count('.'):
				inst = jid.split('/')[0].lower()
				if jid.count('@conf') and inst not in GROUPCHATS:
					reply(type, source, u'меня нет в этой конфе')
				else:
					mess = body[(body.find(' ') + 1):].strip()
					if len(mess) <= 1024:
						msg(jid, u'Сообщение от '+source[2]+': '+mess)
						reply(type, source, u'сделано')
					else:
						reply(type, source, u'Слишком длинная мессага!')
			else:
				reply(type, source, u'Ээ нет, это вообще не жид!')
		else:
			reply(type, source, u'А что слать-то?')
	else:
		reply(type, source, u'ты чё-то тупишь')

def handler_admin_say(type, source, body):
	if body:
		if len(body) <= 256:
			msg(source[1], body)
		else:
			msg(source[1], body[:256])
	else:
		reply(type, source, u'Ну а дальше?')

def handler_global_message(type, source, body):
	if body:
		for conf in GROUPCHATS.keys():
			msg(conf, u'### Сообщение от '+source[2]+':\n'+body)
		reply(type, source, u'Мессага успешно разослана')
	else:
		reply(type, source, u'А что слать то?')

def handler_auto_message(type, source, body):
	if body:
		jid = handler_jid(source[0])
		if jid in AMSGBL:
			reply(type, source, u'тебе запрещено отсылать мессаги админу')
		elif len(body) <= 1024:
			delivery(u'Сообщение от '+source[2]+' ('+jid+'): '+body)
			reply(type, source, u'сделано')
		else:
			reply(type, source, u'Слишком длинная мессага!')
	else:
		reply(type, source, u'Ну а дальше?')

def handler_amsg_blacklist(type, source, body):
	if body:
		args = body.split()
		if len(args) == 2:
			jid = args[1].strip()
			if jid.count('@') and jid.count('.'):
				check = args[0].strip()
				if check == '+':
					if jid not in AMSGBL:
						AMSGBL.append(jid)
						write_file(BLACK_LIST, str(AMSGBL))
						repl = u'добавил %s в чёрный список' % (jid)
					else:
						repl = u'этот жид и так там'
				elif check == '-':
					if jid in AMSGBL:
						AMSGBL.remove(jid)
						write_file(BLACK_LIST, str(AMSGBL))
						repl = u'удалил %s из чёрного списка' % (jid)
					else:
						repl = u'этого жида и так там нет'
				else:
					repl = u'инвалид синтакс'
			else:
				repl = u'ан нет, это вообще не жид!'
		else:
			repl = u'инвалид синтакс'
	else:
		repl, col = u'Чёрный список:', 0
		for jid in AMSGBL:
			col = col + 1
			repl += '\n'+str(col)+'. '+jid
		if col == 0:
			repl = u'Чёрный список пуст'
	reply(type, source, repl)

def amsg_blacklist_init():
	if initialize_file(BLACK_LIST, '[]'):
		globals()['AMSGBL'] = eval(read_file(BLACK_LIST))
	else:
		Print('\n\nError: can`t create black list file!', color2)

def chat_cache_init(conf):
	CHAT_CACHE[conf] = {'1': '', '2': ''}
	CHAT_DIRTY[conf] = True

handler_register("01eh", handler_chat_cache)
command_handler(handler_clean, 15, "collect")
command_handler(last_chat_cache, 20, "collect")
command_handler(handler_test, 10, "collect")
command_handler(handler_admin_message, 100, "collect")
command_handler(handler_admin_say, 20, "collect")
command_handler(handler_global_message, 100, "collect")
command_handler(handler_auto_message, 10, "collect")
command_handler(handler_amsg_blacklist, 100, "collect")
handler_register("00si", amsg_blacklist_init)

handler_register("01si", chat_cache_init)
