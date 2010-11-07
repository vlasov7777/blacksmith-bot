# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  afl-list_plugin.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

IDS_AFLIST = []

def get_afl_hnd(body):
	list = {u'овнер': 'owner', u'админ': 'admin', u'мембер': 'member', u'бан': 'outcast'}
	for afl in list.keys():
		if body.count(afl):
			return list[afl]
	return None

def handler_afl_list(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			afl = get_afl_hnd(body.lower())
			if afl:
				iq = xmpp.Iq(to = source[1], typ = 'get')
				INFA['outiq'] += 1
				ID = 'list_'+str(INFA['outiq'])
				IDS_AFLIST.append(ID)
				iq.setID(ID)
				query = xmpp.Node('query')
				query.setNamespace(xmpp.NS_MUC_ADMIN)
				query.addChild('item', {'affiliation': afl})
				iq.addChild(node = query)
				JCON.SendAndCallForResponse(iq, handler_list_answer, {'type': type, 'source': source, 'afl': afl})
			else:
				reply(type, source, u'чего?')
		else:
			reply(type, source, u'ты точно ничего не забыл?')
	else:
		reply(type, source, u'ты не в чате мундос')

def handler_list_answer(coze, stanza, type, source, afl):
	ID = stanza.getID()
	if ID in IDS_AFLIST:
		IDS_AFLIST.remove(ID)
		if stanza:
			if stanza.getType() == 'result':
				MASS = stanza.getChildren()
				if MASS:
					Props, col, list = MASS[0].getChildren(), 0, u'Список %s:' % (afl)
					for item in Props:
						if item != 'None':
							col = col + 1
							jid = item.getAttrs()['jid']
							if afl == 'outcast':
								if jid in ADLIST:
									handler_unban(source[1], jid)
							list += '\n'+str(col)+'. '+jid
							try:
								reason = (item.getTag('reason')).getData()
								if reason:
									list += ' ['+reason+']'
							except:
								LAST['null'] += 1
					if col != 0:
						if type == 'public':
							reply(type, source, u'глянь в приват')
						reply('private', source, list)
					else:
						reply(type, source, u'пусто')
				else:
					reply(type, source, u'что-то не вышло')
			else:
				reply(type, source, u'аблом')
		else:
			reply(type, source, u'что-то не вышло')
	else:
		reply(type, source, u'не получилось')
	
register_command_handler(handler_afl_list, 'список', ['админ','все'], 20, 'Показывает в зависимости от выбранного ключа список админов, овнеров, мемберов или забаненных конфы', 'список [параметры]', ['список овнеров','список бани','список мемберов','список админов'])
