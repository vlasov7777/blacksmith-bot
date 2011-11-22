# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  logger_plugin.py

# Author:
#  Anaлl Verrier [mail: elghinn@free.fr]
# Modifications:
#  Als [mail: Als@exploit.in]
#  mrDoctorWho [site: http://simpleapps.ru]

AFLID = {"none":   u"посетитель",
		 "member": u"участник",
		 "admin":  u"администратор",
		 "owner":  u"владелец"}

ROLEID = {"visitor": 	 u"гость",
		  "moderator": 	 u"модератор",
		  "participant": u"участник"}

STATS = {"xa": 	 u"недоступен",
		 "dnd":  u"не беспокоить",
		 "away": u"отсутствую",
		 "chat": u"готов поболтать",
		 None: u"доступен"}

from math import modf as math_modf

LOG_HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.shadowed {font-family:times; font-size:17pt; color:#2396ed; text-shadow: #000000 1px 0px 3px}
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
a.h1 {text-decoration: none;color: #369;}
#//-->
</style>
</head>
<body>
<div class="shadowed" align="right">BlackSmith Bot logger file</div>
<div class="shadowed" align="center"><a href="xmpp:%s?join" title="Join to %s">%s</a><hr></div></hr>
<h3><div class="shadowed">%s<hr></div></h3>
<div>
<tt>
"""

LOG_CONFIG_FILE = 'static/logstate.txt'
LOG_CACHE_FILE = 'dynamic/logcache.txt'

LOG_DIR = 'logs'
DEF_LOG_STATE = False

try:
	execfile(LOG_CONFIG_FILE)
except:
	Print('\n\nError: unable to load logger config!\nPlugin will be working with default values...', color2)

if LOG_DIR[-1] == '/':
	LOG_DIR = LOG_DIR[:-1]

LOG_FILENAME_CACHE = {}

LOG_ENABLED = []

Months = {"January":   u"Январь",
		  "February":  u"Февраль",
		  "March": 	   u"Март",
		  "April": 	   u"Апрель",
		  "May": 	   u"Май",
		  "June": 	   u"Июнь",
 		  "July": 	   u"Июль",
 		  "August":    u"Август",
 		  "September": u"Сентябрь",
 		  "October":   u"Октябрь",
 		  "November":  u"Ноябрь",
		  "December":  u"Декабрь"}

Days = {"Monday": 	u"Понедельник",
		"Tuesday": 	u"Вторник",
		"Wednesday":u"Среда",
		"Thursday": u"Четверг",
		"Friday": 	u"Пятница",
		"Saturday": u"Суббота",
		"Sunday": 	u"Воскресенье"}

def DateTimeReplacer(time):
	for x in Months.keys():
		time = time.replace(x, Months[x])
	for x in Days.keys():
		time = time.replace(x, Days[x])
	return time

def log_write_header(fl, source, times):
	if not chkUnicode(source):
		source = source.encode('utf-8')
	date = DateTimeReplacer(time.strftime('%A, %B %d, %Y', times))
	fl.write(LOG_HEADER % (' - '.join([source, date]), source, source, source, date))

def log_get_fp(type, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
	str_year, str_month, str_day = str(year), str(month), str(day)
	file_dir = '/'.join([LOG_DIR, conf, str_year, str_month])
	if not chkUnicode(file_dir):
		file_dir = chkFile(file_dir)
	filename = file_dir+'/'+str_day+'.html'
	if not os.path.exists(file_dir):
		try:
			os.makedirs(file_dir)
		except:
			return False
	if LOG_FILENAME_CACHE.has_key(conf):
		xfile = LOG_FILENAME_CACHE[conf]
		if xfile != filename:
			if os.path.exists(xfile):
				 write_file(xfile, '\n</tt>\n</div>\n</body>\n</html>', "a")
	if os.path.exists(filename):
		fl = file(filename, 'a')
	else:
		LOG_FILENAME_CACHE[conf] = filename
		write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
		fl = file(filename, 'a')
		INFA['fcr'] += 1
		log_write_header(fl, conf, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	return fl

def log_regex_url(matchobj):
	return '<a href="'+matchobj.group(0)+'">'+matchobj.group(0)+'</a>'

def log_write(body, nick, conf, ismoder = 0):
	decimal = str(int(math_modf(time.time())[0]*100000))
	(year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
	body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	body = re.sub('(https|http|ftp)(\:\/\/[^\s<]+)', log_regex_url, body).replace('\n', '<br/>')
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
		log_write(u'*** %s заходит как %s и %s' % (nick, role, afl), '@$$join$$@', conf)

def log_handler_leave(conf, nick, reason, code):
	if conf in LOG_ENABLED:
		if code:
			if code == '307':
				if reason:
					log_write(u'*** %s выгнали из конференции (%s)' % (nick, reason), '@$$userkick$$@', conf)
				else:
					log_write(u'*** %s выгнали из конференции' % (nick), '@$$userkick$$@', conf)
			elif code == '301':
				if reason:
					log_write(u'*** %s запретили входить в данную конференцию (%s)' % (nick, reason), '@$$userban$$@', conf)
				else:
					log_write(u'*** %s запретили входить в данную конференцию' % (nick), '@$$userban$$@', conf)
		else:
			if reason:
				log_write(u'*** %s выходит из конференции (%s)' % (nick, reason), '@$$leave$$@', conf)
			else:
				log_write(u'*** %s выходит из конференции' % (nick), '@$$leave$$@', conf)

def log_handler_presence(Prs):
	fromjid = Prs.getFrom()
	conf = fromjid.getStripped()
	if conf in LOG_ENABLED:
		nick = fromjid.getResource()
		Ptype = Prs.getType()
		if Ptype == 'unavailable':
			scode = Prs.getStatusCode()
			if scode == '303':
				log_write(u'*** %s меняет ник на %s' % (nick, Prs.getNick()), '@$$nickchange$$@', conf)
		else:
			afl = Prs.getAffiliation()
			if afl in AFLID:
				afl = AFLID[afl]
			role = Prs.getRole()
			if role in ROLEID:
				role = ROLEID[role]
			try:
				status = Prs.getShow()
			except:
				status = u'доступен'
			if status in STATS:
				status = STATS[status]
			try:
				text = Prs.getStatus()
			except:
				text = str()
			if text:
				log_write(u'*** %s (%s, %s) теперь %s (%s)' % (nick, afl, role, status, text), '@$$status$$@', conf)
			else:
				log_write(u'*** %s (%s, %s) теперь %s' % (nick, afl, role, status), '@$$status$$@', conf)

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
					reply(type, source, u'логгер и так включен')
			elif body in [u'выкл', 'off', '0']:
				if source[1] in LOG_ENABLED:
					LOG_ENABLED.remove(source[1])
					write_file(filename, 'off')
					reply(type, source, u'логгер выключен')
				else:
					reply(type, source, u'логгер и так выключен')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if source[1] in LOG_ENABLED:
				reply(type, source, u'сейчас логгер включен')
			else:
				reply(type, source, u'сейчас логгер выключен')
	else:
		reply(type, source, u'только в чате!')

def logger_cache_file_init():
	if initialize_file(LOG_CACHE_FILE):
		LOG_FILENAME_CACHE = eval(read_file(LOG_CACHE_FILE))
	else:
		Print('\n\nError: can`t read logcache.txt!')

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
