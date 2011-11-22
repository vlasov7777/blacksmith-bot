# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  antispamer_plugin.py

# Coded by: mrDoctorWho & WitcherGeralt (WitcherGeralt@jabber.ru)
# for http://witcher-team.ucoz.ru/

SPAMSERVERS = u'jabber.454.ru;jabber.fr;pluser.ru;12jabber.com;jabber.3gnt.org;gabbler.de;jabber.workaround.org;12jabber.com;ipse.zapto.org;jabber80.com;headcounter.org;users.gauner.org;jabber.produm.net'
SPAMSERVINFO = {'banned': {}, 'update': 'None'}

def handler_antispamer(type, source, body):
	if body:
		filename = 'dynamic/'+source[1]+'/antispamer.txt'
		body = body.lower()
		if body in [u'бан', 'ban']:
			reply(type, source, u'OK. Начинаю банить...')
			reason = u'спамерский сервер (%s/%s: antispamer plugin)' % (handler_botnick(source[1]), source[2])
			for jid in SPAMSERVERS.split(';'):
				handler_banjid(source[1], jid, reason)
				time.sleep(0.6)
			ban_time = time.strftime('%d.%m.%Y (%H:%M:%S) GMT', time.gmtime())
			SPAMSERVINFO['banned'][source[1]] = ban_time
			write_file(filename, ban_time)
			reply(type, source, u'Все в бане!')
		elif body in [u'унбан', 'unban']:
			reply(type, source, u'OK. Начинаю амнистию...')
			for jid in SPAMSERVERS.split(';'):
				handler_unban(source[1], jid)
				time.sleep(0.6)
			SPAMSERVINFO['banned'][source[1]] = "None"
			write_file(filename, "None")
			reply(type, source, u'Спамеры амнистированы!')
		elif body in [u'лист', 'list', '*']:
			list, col = '', 0
			for serv in SPAMSERVERS.split(';'):
				col = col + 1
				list += '\n'+str(col)+'. '+serv
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, (u'Список спамсерверов (%s):' % (col))+list)
		else:
			reply(type, source, u'Читай хелп!')
	else:
		answer = u'\nСерверов в списке - %s\nПоследнее обновление - %s\nКогда забанены - %s'
		col = str(len(SPAMSERVERS.split(';')))
		update = SPAMSERVINFO['update']
		state = SPAMSERVINFO['banned'][source[1]]
		reply(type, source, answer % (col, update, state))

def spamer_state(conf):
	if check_file(conf, 'antispamer.txt', "None"):
		state = read_file('dynamic/'+conf+'/antispamer.txt')
	else:
		state = "None"
		delivery(u'Внимание! Не удалось создать antispamer.txt для "%s"!' % (conf))
	SPAMSERVINFO['banned'][conf] = state

def load_servers():
	servers = ['<-- start -->', '<-- end -->']
	update = ['<-- update -->', '<-- /update/ -->']
	try:
		data = read_link('http://witcher-team.ucoz.ru/spamservers.list')
		globals()['SPAMSERVERS'] = re_search(data, servers[0], servers[1])
		SPAMSERVINFO['update'] = re_search(data, update[0], update[1])
	except:
		print_exc()
		delivery(u'Внимание! Список спамсерверов не подгружен!')

command_handler(handler_antispamer, 30, "antispamer")

register_stage1_init(spamer_state)
register_stage2_init(load_servers)
