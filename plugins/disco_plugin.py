# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  disco_plugin.py

# Author:
#  Als [Als@exploit.in]
# Modifications:
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_disco(type, source, body):
	if body:
		args = body.split(' ', 2)
		if type == 'private':
			stop = 100
		else:
			stop = 20
		tojid, srch = args[0], False
		if len(args) >= 2:
			if check_number(args[1]):
				stop = int(args[1])
				if type == 'public' and stop >= 50:
					stop = 50
				elif stop >= 250:
					stop = 250
				if len(args) >= 3:
					srch = args[2]
			else:
				srch = args[1]
		iq = xmpp.Iq(to = tojid, typ = 'get')
		INFA['outiq'] += 1
		iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
		JCON.SendAndCallForResponse(iq, handler_disco_ext, {'type': type, 'source': source, 'stop': stop, 'srch': srch, 'tojid': tojid})
	else:
		reply(type, source, u'Ну а дальше то чего?')

def handler_disco_ext(coze, stanza, type, source, stop, srch, tojid):
	repl, dcnt, disco = '', True, []
	if stanza:
		if stanza.getType() == 'result':
			try:
				Props = stanza.getQueryChildren()
			except:
				Props = None
			if Props:
				for x in Props:
					att = x.getAttrs()
					if att.has_key('name'):
						try:
							st = re.search('^(.*) \((.*)\)$', att['name']).groups()
							disco.append([st[0], att['jid'], st[1]])
							dcnt = False
						except:
							if dcnt or tojid.count('@'):
								if tojid.count('@'):
									disco.append(att['name'])
								else:
									disco.append([att['name'], att['jid']])
					else:
						disco.append(att['jid'])
			if disco:
				handler_disco_answer(type, source, stop, disco, srch)
			else:
				reply(type, source, u'пустое диско')
		else:
			reply(type, source, u'не могу')
	else:
		reply(type, source, u'аблом...')

def handler_disco_answer(type, source, stop, disco, srch):
	if stop != 0:
		repl, total, dis = u'\nРезультат:\n', 0, []
		if len(disco[0]) == 3:
			disco = sortdis(disco)
			for x in disco:
				total += 1
				if srch:
					if srch.endswith('@'):
						if x[1].startswith(srch):
							dis.append(str(total)+') '+x[0]+' ['+x[1]+']: '+str(x[2]))
							break
						else:
							continue
					elif not x[0].count(srch) and not x[1].count(srch):
						continue
				dis.append(str(total)+') '+x[0]+' ['+x[1]+']: '+str(x[2]))
				if len(dis) == stop:
					break
		elif len(disco[0]) == 2:
			disco.sort()
			for x in disco:
				total += 1
				if srch and not x[0].count(srch) and not x[1].count(srch):
					continue
				dis.append(str(total)+') '+x[0]+' ['+x[1]+']')
				if len(dis) == stop:
					break
		else:
			disco.sort()
			for x in disco:
				total += 1
				try:
					x = str(x)
				except:
					try:
						x = unicode(x)
					except:
						x = '[SENSORED]'
				if srch and not x.count(srch):
					continue
				dis.append(str(total)+') '+x)
				if len(dis) == stop:
					break
		if dis:
			if len(disco) != len(dis):
				dis.append(u'всего %s пунктов' % str(len(disco)))
		else:
			repl = u'пустое диско'
		reply(type, source, repl+'\n'.join(dis))
	else:
		reply(type, source, u'всего %s пунктов' % str(len(disco)))

def sortdis(dis):
	disd, diss, disr = [], [], []
	for x in dis:
		try:
			int(x[2])
			disd.append(x)
		except:
			diss.append(x)
	disd.sort(lambda x,y: int(x[2]) - int(y[2]))
	disd.reverse()
	diss.sort()
	for x in disd:
		disr.append(x)
	for x in diss:
		disr.append(x)
	return disr

register_command_handler(handler_disco, 'диско', ['инфо','все'], 10, 'Показывает результаты обзора сервисов для указанного jid.\nВторой или третий (если также даётся ограничитель кол-ва) параметр - поиск. Ищет заданное слово в jid и описании элемента оценки. Если поисковым словом задать имя конференции до названия сервера (например qwerty@), то покажет место этой конференции в общем рейтинге.\nВ общий чат может дать max 50 результатов, без указания кол-ва - 10.\n В приват может дать max 250, без указания кол-ва 50.', 'диско <сервер> <кол-во результатов> <поисковая строка>', ['диско jabber.aq','диско conference.jabber.aq 5','диско conference.jabber.aq qwerty','диско conference.jabber.aq 5 qwerty','диско conference.jabber.aq qwerty@'])
