# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  verification_plugin.py
#  Ver.3.5

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

OTVET = {}
VERON = {}

def veron_timer(conf, nick, jid):
	if jid in OTVET[conf]:
		del OTVET[conf][jid]
		handler_kick(conf, nick, u'%s: Не прошел авторизацию!' % (handler_botnick(conf)))

def handler_verification(conf, nick, afl, role):
	if VERON[conf] != 'off' and afl == 'none':
		jid = handler_jid(conf+'/'+nick)
		if jid not in ADLIST:
			if not conf in OTVET:
				OTVET[conf] = {}
			QA = random.choice(QUESTIONS.keys())
			OTVET[conf][jid] = {'ansver': QUESTIONS[QA]['answer'], 'col': 0}
			handler_visitor(conf, nick, u'%s: Авторизация...' % (handler_botnick(conf)))
			msg(conf+'/'+nick, u'Привет! Это IQ проверка, чтобы получить голос %s, У тебя три попытки и 1 минута!' % (QUESTIONS[QA]['question']))
			try:
				threading.Timer(60, veron_timer,(conf, nick, jid)).start()
			except:
				LAST['null'] += 1

def handler_verification_answer(raw, type, source, body):
	if type == 'private' and source[1] in VERON:
		if VERON[source[1]] != 'off' and source[1] in OTVET:
			jid = handler_jid(source[0])
			if jid in OTVET[source[1]]:
				if OTVET[source[1]][jid]['ansver'] == body.lower():
					del OTVET[source[1]][jid]
					handler_participant(source[1], source[2], u'Авторизация пройдена!')
					reply(type, source, u'Ок, признаю - ты не бот')
				elif OTVET[source[1]][jid]['col'] >= 3:
					del OTVET[source[1]][jid]
					handler_kick(source[1], source[2], u'%s: Не прошел авторизацию!' % (handler_botnick(source[1])))
				else:
					OTVET[source[1]][jid]['col'] += 1
					reply(type, source, u'Включи мозг! Неправильно!')

def handler_verification_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/verification.txt'
			if body in [u'вкл', 'on', '1']:
				VERON[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'авторизация включена')
			elif body in [u'выкл', 'off', '0']:
				VERON[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'авторизация выключена')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if VERON[source[1]] == 'off':
				reply(type, source, u'сейчас авторизация выключена')
			else:
				reply(type, source, u'сейчас авторизация включена')
	else:
		reply(type, source, u'только в чате мудак!')

def verification_init(conf):
	if check_file(conf, 'verification.txt', "'off'"):
		state = eval(read_file('dynamic/'+conf+'/verification.txt'))
	else:
		state = 'off'
		delivery(u'Внимание! Не удалось создать verification.txt для "%s"!' % (conf))
	VERON[conf] = state

register_join_handler(handler_verification)
register_message_handler(handler_verification_answer)
register_command_handler(handler_verification_control, 'авторизация', ['админ','все'], 20, 'Проверка вновь вошедшего пользователя на "бота", без параметра покажет текущее состояние\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'авторизация [вкл/on/1/выкл/off/0]', ['авторизация вкл', 'авторизация выкл'])

register_stage1_init(verification_init)
