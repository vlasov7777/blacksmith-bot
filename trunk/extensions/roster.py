# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  roster_plugin.py

# Author: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def roster_control(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			jid = args[1].strip()
			if jid.count('@') and jid.count('.'):
				action = args[0].strip()
				if action == '+':
					JCON.Roster.Authorize(jid)
					JCON.Roster.Subscribe(jid)
					if len(args) >= 3:
						if len(args) >= 4:
							lx = args[3].strip().lower()
						else:
							lx = 'el-lx body'
						if lx in [u'админ', 'admin']:
							JCON.Roster.setItem(jid, args[2].strip(), ['ADMINS'])
							reply(type, source, u'добавил в группу "ADMINS" с ником "%s"' % (args[2].strip()))
						else:
							RSTR['AUTH'].append(jid)
							if jid in RSTR['BAN']:
								RSTR['BAN'].remove(jid)
							write_file(ROSTER_FILE, str(RSTR))
							JCON.Roster.setItem(jid, args[2].strip(), ['USERS'])
							reply(type, source, u'добавил в группу "USERS" с ником "%s"' % (args[2].strip()))
					else:
						RSTR['AUTH'].append(jid)
						if jid in RSTR['BAN']:
							RSTR['BAN'].remove(jid)
						write_file(ROSTER_FILE, str(RSTR))
						JCON.Roster.setItem(jid, jid.split('@')[0], ['USERS'])
						reply(type, source, u'добавил в группу "USERS"')
				elif action == '-':
					if jid in JCON.Roster.getItems():
						RSTR['BAN'].append(jid)
						if jid in RSTR['AUTH']:
							RSTR['AUTH'].remove(jid)
						write_file(ROSTER_FILE, str(RSTR))
						JCON.Roster.Unsubscribe(jid)
						JCON.Roster.delItem(jid)
						reply(type, source, u'сделано')
					else:
						reply(type, source, u'у меня в ростере его и так нет')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		list, col = '', 0
		for jid in JCON.Roster.getItems():
			if not jid.count('@conf'):
				col = col + 1
				list += '\n'+str(col)+'. '+jid
		if col != 0:
			reply(type, source, (u'\nВсего (%s) контактов:' % str(col))+list)
		else:
			reply(type, source, u'Мой ростер пуст...')

def roster_work(type, source, body):
	if body:
		body = body.lower()
		if body in [u'вкл', 'on', '1']:
			RSTR['VN'] = 'on'
			write_file(ROSTER_FILE, str(RSTR))
			reply(type, source, u'Прием сообщений из ростера включен')
		elif body in [u'выкл', 'off', '0']:
			RSTR['VN'] = 'off'
			write_file(ROSTER_FILE, str(RSTR))
			reply(type, source, u'Прием сообщений из ростера отключен')
		elif body in [u'тест', 'iq', '2']:
			RSTR['VN'] = 'iq'
			write_file(ROSTER_FILE, str(RSTR))
			reply(type, source, u'Включена IQ-проверка')
		else:
			reply(type, source, u'я непонял чего ты хочеш')
	else:
		if RSTR['VN'] == 'on':
			reply(type, source, u'Сейчас прием сообщений из ростера включен')
		elif RSTR['VN'] == 'off':
			reply(type, source, u'Сейчас прием сообщений из ростера отключен')
		elif RSTR['VN'] == 'iq':
			reply(type, source, u'Сейчас включена IQ-проверка')

IQNT = {'col': 0, 'Yes!': True, 'list': []}

def IQ_finish():
	IQNT['Yes!'] = True
	if IQNT['list'] != []:
		repl = u'Список атаковавших:\n'+', '.join(sorted(IQNT['list']))
		IQNT['list'] = []
	else:
		repl = u'Фу пронесло... Это была не атака :D'
	delivery(repl)

def IQ_minus():
	if IQNT['col']:
		IQNT['col'] += -1

def Handler_Roster_IQ(stanza):
	if stanza.getTags('query', {}, xmpp.NS_ROSTER):
		if stanza.getType() == 'set':
			Query = stanza.getTag('query')
			if Query:
				item = Query.getTag('item')
				subscr = item.getAttr('subscription')
				user = item.getAttr('jid')
				if subscr and user:
					if IQNT['Yes!']:
						IQNT['col'] += 1
						if IQNT['col'] <= 4:
							if subscr == 'both':
								if JCON.Roster.getSubscription(user) != 'both' and user not in [BOSS, BOSS.lower()]:
									delivery(u'Контакт %s добавлен в ростер!' % (user))
							elif subscr == 'remove':
								delivery(u'Контакт %s удалился из ростера!' % (user))
						else:
							IQNT['list'].append(user)
							IQNT['Yes!'] = False
							delivery(u'Внимание! Меня атакуют (вроде), через 10 минут пришлю отчёт...')
							try:
								threading.Timer(600, IQ_finish).start()
							except:
								pass
						try:
							threading.Timer(18, IQ_minus).start()
						except:
							pass
					else:
						IQNT['list'].append(user)

command_handler(roster_control, 80, "roster")
command_handler(roster_work, 80, "roster")
register_iq_handler(Handler_Roster_IQ)
