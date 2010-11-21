# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  logger_plugin.py

# Author:
#  Anaлl Verrier [mail: elghinn@free.fr]
# Modifications:
#  Als [mail: Als@exploit.in]
#  mrDoctorWho [JID: nexus@xmpp.ru]

AFLID = {'none': u'никто', 'member': u'участвующий', 'admin': u'админ', 'owner': u'владелец'}
ROLEID = {'visitor': u'посетитель', 'participant': u'участник', 'moderator': u'модератор'}

from math import modf as math_modf

LOG_HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.userjoin {color: #009900; font-style: italic; font-weight: bold}
.userleave {color: #dc143c; font-style: italic; font-weight: bold}
.statuschange {color: #a52a2a; font-weight: bold}
.rachange {color: #0000FF; font-weight: bold}
.userkick {color: #FF7F50; font-weight: bold}
.userban {color: #DAA520; font-weight: bold}
.nickchange {color: #FF69B4; font-style: italic; font-weight: bold}
.timestamp {color: #aaa;}
.timestamp a {color: #aaa; text-decoration: none;}
.system {color: #090; font-weight: bold;}
.emote {color: #800080;}
.self {color: #0000AA;}
.selfmoder {color: #DC143C;}
.normal {color: #483d8b;}
#mark { color: ##DAA520; text-align: left; font face="arial"; letter-spacing: 5px; font-weight: bold }
#mark2 { color: #FF0000; text-align: right; font face="arial"; letter-spacing: 5px; font-weight: bold }
h1 { color: #369; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #639; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a.h1 {text-decoration: none;color: #369;}
#//-->
</style>
</head>
<body>
<div id="mark">BlackSmith logger_Plugin`s File
<br>
Marking: Anall Verrier [mail: elghinn@free.fr]</div>
<div id="mark2">Mods &copy; mrDoctorWho [JID: nexus@xmpp.ru]
<br>
for <a href="http://witcher-team.ucoz.ru/">http://witcher-team.ucoz.ru/</a></div>
<h1><a class="h1" href="xmpp:%s?join" title="Join room">%s</a></h1>
<h2>%s</h2>
<div>
<tt>
"""

LOG_CONFIG_FILE = 'static/logstate.txt'
LOG_CACHE_FILE = 'dynamic/logcache.txt'

LOG_DIR = 'logs'
DEF_LOG_STATE = False

try:
	LOG_CONFIG = file(LOG_CONFIG_FILE)
	exec LOG_CONFIG in globals()
	LOG_CONFIG.close()
except:
	Print('\n\nError: unable to load logger config!\nPlugin will be working with default values...', color2)

if LOG_DIR[-1] == '/':
	LOG_DIR = LOG_DIR[:-1]

LOG_FILENAME_CACHE = {}

LOG_ENABLED = []

def log_write_header(fl, source, times):
	if not check_nosimbols(source):
		source = source.encode('utf-8')
	date = time.strftime('%A, %B %d, %Y', times)
	fl.write(LOG_HEADER % (' - '.join([source, date]), source, source, date))

def log_get_fp(type, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
	str_year, str_month, str_day = str(year), str(month), str(day)
	file_dir = '/'.join([LOG_DIR, conf, str_year, str_month])
	if not check_nosimbols(file_dir):
		file_dir = encode_filename(file_dir)
	filename = file_dir+'/'+str_day+'.html'
	alt_filename = file_dir+'/'+str_day+'._html'
	if not os.path.exists(file_dir):
		try:
			os.makedirs(file_dir)
		except:
			return False
	if LOG_FILENAME_CACHE.has_key(conf):
		xfile = LOG_FILENAME_CACHE[conf]
		if xfile != filename:
			if os.path.exists(xfile):
				fl_old = file(xfile, 'a')
				fl_old.write('\n</tt>\n</div>\n</body>\n</html>')
				fl_old.close()
		if os.path.exists(filename):
			fl = file(filename, 'a')
			return fl
		else:
			LOG_FILENAME_CACHE[conf] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fl = file(filename, 'w')
			log_write_header(fl, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fl
	else:
		if os.path.exists(filename):
			LOG_FILENAME_CACHE[conf] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fl = file(alt_filename, 'a')
			return fl
		else:
			LOG_FILENAME_CACHE[conf] = filename
			fl = file(filename, 'w')
			log_write_header(fl, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fl

def log_regex_url(matchobj):
	return '<a href="'+matchobj.group(0)+'">'+matchobj.group(0)+'</a>'

def log_write(body, nick, conf, ismoder = 0):
	decimal = str(int(math_modf(time.time())[0]*100000))
	(year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
	body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	body = re.sub('(http|ftp)(\:\/\/[^\s<]+)', log_regex_url, body).replace('\n', '<br/>')
	body, nick = body.encode('utf-8'), nick.encode('utf-8')
	timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
	fl = log_get_fp(type, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	if fl:
		fl.write('<span class="timestamp"><a id="t'+timestamp[1:-1]+'.'+decimal+'" href="#t'+timestamp[1:-1]+'.'+decimal+'">'+timestamp+'</a></span> ')
		if not nick:
			fl.write('<span class="system">'+body+'</span><br />\n')
		elif body[:3].lower() == '/me':
			fl.write('<span class="emote">* %s %s</span><br />\n' % (nick, body[3:]))
		elif nick == '@$$leave$$@':
			fl.write('<span class="userleave">'+body+'</span><br />\n')
		elif nick == '@$$join$$@':
			fl.write('<span class="userjoin">'+body+'</span><br />\n')
		elif nick == '@$$status$$@':
			fl.write('<span class="statuschange">'+body+'</span><br />\n')
		elif nick == '@$$ra$$@':
			fl.write('<span class="rachange">'+body+'</span><br />\n')
		elif nick == '@$$userkick$$@':
			fl.write('<span class="userkick">'+body+'</span><br />\n')
		elif nick == '@$$userban$$@':
			fl.write('<span class="userban">'+body+'</span><br />\n')
		elif nick == '@$$nickchange$$@':
			fl.write('<span class="nickchange">'+body+'</span><br />\n')
		elif ismoder:
			fl.write('<span class="selfmoder">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
		else:
			fl.write('<span class="self">&lt;%s&gt;</span> %s<br />\n' % (nick, body))

def log_handler_message(raw, type, source, body):
	if source[1] in LOG_ENABLED and type == 'public':
		if source[2] in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][source[2]].has_key('ismoder') and GROUPCHATS[source[1]][source[2]]['ismoder']:
			ismoder = 1
		else:
			ismoder = 0
		log_write(body, source[2], source[1], ismoder)

def log_handler_join(conf, nick, afl, role):
	if conf in LOG_ENABLED:
		if afl in AFLID:
			afl = AFLID[afl]
		if role in ROLEID:
			role = ROLEID[role]
		log_write(u'%s подключился как %s %s' % (nick, afl, role), '@$$join$$@', conf)

def log_handler_leave(conf, nick, reason, code):
	if conf in LOG_ENABLED:
		if code:
			if code == '307':
				if reason:
					log_write(u'%s выгнали из конференции (kick) (%s)' % (nick, reason), '@$$userkick$$@', conf)
				else:
					log_write(u'%s выгнали из конференции (kick)' % (nick), '@$$userkick$$@', conf)			
			elif code == '301':
				if reason:
					log_write(u'%s был забанен (%s)' % (nick, reason), '@$$userban$$@', conf)
				else:
					log_write(u'%s был забанен' % (nick), '@$$userban$$@', conf)
		else:
			if reason:
				log_write(u'%s  вышел из конференции (%s)' % (nick, reason), '@$$leave$$@', conf)
			else:
				log_write(u'%s вышел из конференции' % (nick), '@$$leave$$@', conf)

def log_handler_presence(Prs):
	fromjid = Prs.getFrom()
	conf = fromjid.getStripped()
	if conf in LOG_ENABLED:
		nick = fromjid.getResource()
		Ptype = Prs.getType()
		if Ptype == 'unavailable':
			scode = Prs.getStatusCode()
			if scode == '303':
				log_write(u'%s сменил ник на %s' % (nick, Prs.getNick()), '@$$nickchange$$@', conf)
		else:
			afl = Prs.getAffiliation()
			if afl in AFLID:
				afl = AFLID[afl]
			role = Prs.getRole()
			if role in ROLEID:
				role = ROLEID[role]
			STATS = {'away': u'отошел', 'xa': u'недоступен', 'dnd': u'занят', 'chat': u'готов поболтать'}
			try:
				status = Prs.getShow()
			except:
				status = u'онлайн'
			if status in STATS:
				status = STATS[status]
			try:
				text = Prs.getStatus()
			except:
				text = ''
			if text:
				log_write(u'%s (%s %s) теперь %s (%s)' % (nick, afl, role, status, text), '@$$status$$@', conf)
			else:
				log_write(u'%s (%s %s) теперь %s' % (nick, afl, role, status), '@$$status$$@', conf)	

def handler_logger_state(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/logstate.txt'
			if body in [u'вкл', 'on', '1']:
				if source[1] not in LOG_ENABLED:
					LOG_ENABLED.append(source[1])
					write_file(filename, 'on')
					reply(type, source, u'логгер включен')
				else:
					reply(type, source, u'логгер итак включен')
			elif body in [u'выкл', 'off', '0']:
				if source[1] in LOG_ENABLED:
					LOG_ENABLED.remove(source[1])
					write_file(filename, 'off')
					reply(type, source, u'логгер выключен')
				else:
					reply(type, source, u'логгер итак выключен')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if source[1] in LOG_ENABLED:
				reply(type, source, u'сейчас логгер включен')
			else:
				reply(type, source, u'сейчас логгер выключен')
	else:
		reply(type, source, u'только в чате мудак!')

def logger_cache_file_init():
	if initialize_file(LOG_CACHE_FILE):
		LOG_FILENAME_CACHE = eval(read_file(LOG_CACHE_FILE))
	else:
		Print('\n\nError: can`t create logcache.txt!')

def logger_init(conf):
	if check_file(conf, 'logstate.txt', DEF_LOG_STATE):
		state = read_file('dynamic/'+conf+'/logstate.txt')
		if state == 'on':
			LOG_ENABLED.append(conf)
	else:
		delivery(u'Внимание! Не удалось создать logstate.txt для "%s"!' % (conf))

if DEF_LOG_STATE:
	register_message_handler(log_handler_message)
	register_join_handler(log_handler_join)
	register_leave_handler(log_handler_leave)
	register_presence_handler(log_handler_presence)
	register_command_handler(handler_logger_state, 'логгер', ['админ','все'], 30, 'Включение/выключение логирования конференции, без параметров покажет текущее состояние.', 'логгер [on/off/вкл/выкл/1/0]', ['логгер вкл','логгер','логгер выкл'])
	register_stage0_init(logger_cache_file_init)
	register_stage1_init(logger_init)
