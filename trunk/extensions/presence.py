# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  presence_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  dimichxp [dimichxp@gmail.com]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

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
		iq.setID('ping_'+str(INFA['outiq']))
		iq.addChild('ping', {}, [], xmpp.NS_PING)
		JCON.SendAndCallForResponse(iq, check_alive_answer, {})
	try:
		threading.Timer(360, check_alive_handler).start()
	except:
		pass

def check_alive_answer(coze, stanza):
	if stanza:
		conf, error = (stanza.getFrom()).getStripped(), stanza.getErrorCode()
		if error in ['405', None]:
			pass
		else:
			try:
				threading.Timer(180, error_join_timer,(conf,)).start()
			except:
				pass

register_presence_handler(check_nick_command)

register_stage2_init(check_alive_handler)
