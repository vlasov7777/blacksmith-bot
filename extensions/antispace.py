# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  antispace_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

ANTISPACE = {}

def handler_antispace(Prs):
	conf = Prs.getFrom().getStripped()
	if ANTISPACE[conf] != 'off':
		code = Prs.getStatusCode()
		if code == '303':
			nick = Prs.getNick()
		else:
			nick = Prs.getFrom().getResource()
		if nick.count(' '):
			handler_kick(conf, nick, u'Пробелы в нике запрещены!')

def handler_antispace_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/antispace.txt'
			if body in [u'вкл', 'on', '1']:
				ANTISPACE[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'антиспэйс включен')
			elif body in [u'выкл', 'off', '0']:
				ANTISPACE[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'антиспэйс выключен')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if ANTISPACE[source[1]] == 'off':
				reply(type, source, u'сейчас антиспэйс выключен')
			else:
				reply(type, source, u'сейчас антиспэйс включен')
	else:
		reply(type, source, u'только в чате мудак!')

def antispace_init(conf):
	if check_file(conf, 'antispace.txt', "'off'"):
		state = eval(read_file('dynamic/'+conf+'/antispace.txt'))
	else:
		state = 'off'
		delivery(u'Внимание! Не удалось создать antispace.txt для "%s"!' % (conf))
	ANTISPACE[conf] = state

register_presence_handler(handler_antispace)
command_handler(handler_antispace_control, 20, "antispace")

register_stage1_init(antispace_init)
