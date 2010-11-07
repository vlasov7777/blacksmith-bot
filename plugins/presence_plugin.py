# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  presence_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  dimichxp [dimichxp@gmail.com]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

AFLS = {'owner': 15, 'admin': 5, 'member': 1, 'none': 0}
ROLES = {'moderator': 15, 'participant': 10, 'visitor': 0}

CHECK_ALIVE = []

def afls_roles_userlevel(Prs):
	fromjid = Prs.getFrom()
	conf = fromjid.getStripped()
	nick = fromjid.getResource()
	jid = handler_jid(conf+'/'+nick)
	if jid not in GLOBACCESS:
		if conf in CONFACCESS and jid in CONFACCESS[conf]:
			LAST['null'] += 1
		elif conf in GROUPCHATS and nick in GROUPCHATS[conf]:
			afl = Prs.getAffiliation()
			if afl in AFLS:
				afl_access = AFLS[afl]
			else:
				afl_access = 0
			role = Prs.getRole()
			if role in ROLES:
				role_access = ROLES[role]
			else:
				role_access = 0
			access = afl_access + role_access
			change_local_access(conf, jid, access)

def check_nick_command(Prs):
	fromjid = Prs.getFrom()
	conf = fromjid.getStripped()
	code = Prs.getStatusCode()
	if code == '303':
		nick = Prs.getNick()
	else:
		nick = fromjid.getResource()
	nick = nick.strip()
	if nick:
		if len(nick) > 16:
			handler_kick(conf, nick, u'Слишком длинный ник!')
		else:
			cmd_nick = nick.split()[0].strip()
			if conf in PREFIX:
				item = command_Prefix(conf, cmd_nick.lower())
			else:
				item = cmd_nick.lower()
			if conf in MACROS.macrolist.keys():
				cmds = (COMMANDS.keys() + MACROS.gmacrolist.keys() + MACROS.macrolist[conf].keys())
			else:
				cmds = (COMMANDS.keys() + MACROS.gmacrolist.keys())
			if item in cmds or nick.count('%s'):
				handler_kick(conf, nick, u'Твой ник под запретом!')

def check_alive_handler():
	for conf in GROUPCHATS.keys():
		iq = xmpp.Iq(to = conf+'/'+handler_botnick(conf), typ = 'get')
		INFA['outiq'] += 1
		ID = 'ping_'+str(INFA['outiq'])
		CHECK_ALIVE.append(ID)
		iq.addChild('ping', {}, [], xmpp.NS_PING)
		iq.setID(ID)
		JCON.SendAndCallForResponse(iq, check_alive_answer, {})
	try:
		threading.Timer(360, check_alive_handler).start()
	except:
		LAST['null'] += 1

def check_alive_answer(coze, stanza):
	ID = stanza.getID()
	if ID in CHECK_ALIVE:
		CHECK_ALIVE.remove(ID)
		if stanza:
			conf, error = (stanza.getFrom()).getStripped(), stanza.getErrorCode()
			if error in ['405', None]:
				LAST['null'] += 1
			else:
				try:
					threading.Timer(180, error_join_timer,(conf,)).start()
				except:
					LAST['null'] += 1

register_presence_handler(afls_roles_userlevel)
register_presence_handler(check_nick_command)

register_stage2_init(check_alive_handler)
