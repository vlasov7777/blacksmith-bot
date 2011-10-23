# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  invite_plugin.py

# Idea: Als [Als@exploit.in]
# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

INV_TIMES = {}

def invite_timer(conf):
	if conf not in INV_TIMES:
		INV_TIMES[conf] = 0
	return INV_TIMES[conf]

def handler_send_invite(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			timer = (time.time() - invite_timer(source[1]))
			if timer >= 300:
				args = body.split()
				nick = args[0].strip()
				if nick.count('@') and nick.count('.'):
					jid = nick
				elif nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = False
				if jid:
					if len(args) >= 2:
						reason = body[(body.find(' ') + 1):].strip()
					else:
						reason = False
					INV_TIMES[source[1]] = time.time()
					invite = xmpp.Message(to = source[1])
					INFA['outmsg'] += 1
					id = 'inv_'+str(INFA['outmsg'])
					invite.setID(id)
					x = xmpp.Node('x')
					x.setNamespace(xmpp.NS_MUC_USER)
					inv = x.addChild('invite', {'to': jid})
					if reason:
						inv.setTagData('reason', reason)
					else:
						inv.setTagData('reason', u'Вас приглашает '+source[2])
					invite.addChild(node = x)
					JCON.send(invite)
					reply(type, source, u'Приглашение выслано!')
				else:
					reply(type, source, u'Я его незнаю!')
			else:
				strtimer = timeElapsed(300 - timer)
				reply(type, source, u'Приглашения можно отсылать 1 раз в 5 мин. (Осталось: %s)' % (strtimer))
		else:
			reply(type, source, u'Чего нада!?')
	else:
		reply(type, source, u'Ты реально тупиш!')

register_command_handler(handler_send_invite, 'призвать', ['все','разное'], 20, 'Отсылает инвайт указанному юзеру.', 'призвать [жид/ник] [причина]', ['призвать Маша так надо','призвать когонить','призвать cuvak@jabber.ru'])
