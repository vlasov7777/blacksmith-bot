#! /usr/bin/env python
# -*- coding: utf-8 -*-

#  BlackSmith Bot Core
#  BlackSmith.py

#  Als [Als@exploit.in]
#  Evgen [meb81@mail.ru]
#  dimichxp [dimichxp@gmail.com]
#  mrDoctorWhо [mrdoctorwho@gmail.com]
#  Boris Kotov [admin@avoozl.ru]
#  Mike Mintz [mikemintz@gmail.com]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

#  By WitcherGeralt, based on Talisman by Als (Neutron by Gh0st)

################ import modules ################################################################

from __future__ import with_statement

from xml.parsers.expat import ExpatError as BadlyFormedStanza

from traceback import format_exc as error_, print_exc as Print_Error

import sys, os, time, gc, codecs, types, threading, base64

os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, "modules")

from enconf import *; from hammer import *

import xmpp, macros, simplejson, re, string, random, urllib, urllib2

################ Statistics cache ##############################################################

INFO = {'start': 0, 'msg': 0, 'prs': 0, 'iq': 0, 'cmd': 0, 'thr': 0, 'errs': 0}
INFA = {'outmsg': 0, 'outiq': 0, 'fr': 0, 'fw': 0, 'fcr': 0, 'cfw': 0}
RSTR = {'AUTH': [], 'BAN': [], 'VN': 'off'}
STOP = {'mto': 0, 'jids': {}}
DCNT = {'col': 0, 'Yes!': True}
LAST = {'time': 0, 'null': 0, 'cmd': 'start'}

################ friendly handlers #############################################################

if os.environ.has_key("TERM"):
	COLORS_ENABLED = True
else:
	COLORS_ENABLED = False

color0 = chr(27)+"[0m"
color1 = chr(27)+"[33m"
color2 = chr(27)+"[31;1m"
color3 = chr(27)+"[32m"
color4 = chr(27)+"[34;1m"

def retry_body(x, y):
	try:
		body, color = unicode(x), y
	except:
		body, color = x, False
	return (body, color)

def text_color(text, color):
	if COLORS_ENABLED:
		text = color+text+color0
	return text

def Print(text, color = False):
	try:
		if color:
			text = text_color(text, color)
		print text
	except:
		LAST['null'] += 1

def try_sleep(slp):
	try:
		time.sleep(slp)
	except KeyboardInterrupt:
		os.abort()
	except:
		LAST['null'] += 1

def Exit(text, exit, slp):
	Print(text, color2); try_sleep(slp)
	if exit:
		os.abort()
	else:
		os.execl(sys.executable, sys.executable, sys.argv[0])

################ Configuration Items ###########################################################

GENERAL_CONFIG_FILE = 'static/source.py'
GLOBACCESS_FILE = 'dynamic/access.txt'
GROUPCHATS_FILE = 'dynamic/chats.txt'
QUESTIONS_FILE = 'static/veron.txt'
ROSTER_FILE = 'dynamic/roster.txt'
PLUGIN_DIR = 'plugins'
PID_FILE = 'PID.txt'

BOT_OS, BOT_PID = os.name, os.getpid()

if BOT_OS == 'nt':
	os.system('COLOR 0C')

def PASS_GENERATOR(codename, col):
	symbols = '0123456789%s._(!}{#)' % (string.letters)
	for x in range(0, col):
		codename += random.choice(symbols)
	return codename

try:
	GENERAL_CONFIG = file(GENERAL_CONFIG_FILE)
	exec GENERAL_CONFIG in globals()
	GENERAL_CONFIG.close()
except:
	Exit('\n\nError: unable to read general config file!', 1, 30)

try:
	reload(sys)
	sys.setdefaultencoding('utf-8')
except:
	Print('\n\nError: can`t set default encoding!', color2)

try:
	execfile('static/versions.py')
except:
	Exit('\n\nError: verfile (versions.py) isn`t exists!', 1, 30)

if BOT_OS == 'nt':
	os.system('Title BlackSmith - %s' % (Caps))

DEFAULT_NICK = DEFAULT_NICK_(DEFAULT_NICK)
MEMORY_LIMIT = MEMORY_LIMIT_(MEMORY_LIMIT)

################ lists handlers ################################################################

MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
IQ_HANDLERS = []
PRESENCE_HANDLERS = []
COMMAND_HANDLERS = {}

STAGE0_INIT = []
STAGE1_INIT = []
STAGE2_INIT = []
STAGE3_INIT = []

################ lists & client & others #######################################################

MACROS = macros.Macros()
ONLINE = False
online = lambda cl: cl.isConnected()
ADLIST = []
ANSWER = {}
PREFIX = {}
STATUS = {}
ERRORS = {}
COMMOFF = {}
COMMSTAT = {}
COMMANDS = {}
RUNTIMES = {}
BOT_NICKS = {}
QUESTIONS = {}
ACCBYCONF = {}
CONFACCESS = {}
GLOBACCESS = {}
GROUPCHATS = {}
UNAVALABLE = []

(JCON, ROSTER) = (None, False)

smph = threading.BoundedSemaphore(value = 100)
mtx = threading.Lock()
wsmph = threading.BoundedSemaphore(value = 1)

################ file work handlers ############################################################

def check_file(conf = None, file = "", data = ""):
	if conf:
		filename = 'dynamic/%s/%s' % (conf, file)
		if not check_nosimbols(filename):
			filename = encode_filename(filename)
	else:
		filename = 'dynamic/%s' % (file)
	return initialize_file(filename, data)

def initialize_file(filename, data = ""):
	if len(filename.split('/')) >= 4:
		return False
	if os.path.exists(filename):
		return True
	try:
		folder = os.path.dirname(filename)
		if folder and not os.path.exists(folder):
			os.mkdir(folder, 0755)
		if os.access(filename, os.F_OK):
			fl = file(filename, 'w')
		else:
			fl = open(filename, 'w')
		INFA['fcr'] += 1
		if not data:
			data = '{}'
		fl.write(data)
		fl.close()
	except:
		return False
	return True

def read_file(filename):
	if filename.count('/') > 1:
		if not check_nosimbols(filename):
			filename = encode_filename(filename)
	fl = file(filename, 'r')
	INFA['fr'] += 1
	data = fl.read()
	fl.close()
	return data

def file_add(filename, data):
	if filename.count('/') > 1:
		if not check_nosimbols(filename):
			filename = encode_filename(filename)
	try:
		fl = file(filename, 'a')
		INFA['fw'] += 1
		fl.write(data)
		fl.close()
	except:
		LAST['null'] += 1

def write_file(filename, data):
	if filename.count('/') > 1:
		if not check_nosimbols(filename):
			filename = encode_filename(filename)
	with wsmph:
		mtx.acquire()
		try:
			fl = file(filename, 'w')
			INFA['fw'] += 1
			fl.write(data)
			fl.close()
		finally:
			mtx.release()

################ lytic crashlog ################################################################

def Dispatch_fail():
	crashfile = file('__main__.crash', 'a')
	Print_Error(limit = None, file = crashfile)
	crashfile.close()

def lytic_crashlog(handler, command = None):
	DIR, handler, Number, error_body = "feillog", handler.func_name, (len(ERRORS.keys()) + 1), error_()
	ERRORS[Number] = error_body
	if ONLINE:
		if command:
			error = u'команды "%s" (%s)' % (command, handler)
		else:
			error = u'процесса "%s"' % (handler)
		delivery(u'При выполнении %s --> произошла ошибка!' % (error))
	else:
		Print('\n\nError: can`t execut "%s"!' % (handler), color2)
	filename = (DIR+'/error[%s]%s.crash') % (str(INFA['cfw'] + 1), time.strftime('[%H.%M.%S][%d.%m.%Y]', time.localtime()))
	try:
		if not os.path.exists(DIR):
			os.mkdir(DIR, 0755)
		crashfile = file(filename, 'w')
		INFA['cfw'] += 1
		Print_Error(limit = None, file = crashfile)
		crashfile.close()
		if ONLINE:
			if BOT_OS == 'nt':
				delivery(u'Ошибку смотри по команде --> "ошибка %s" (Крэшфайл --> %s)' % (str(Number), filename))
			else:
				delivery(u'Ошибку смотри по командам --> "ошибка %s", "sh cat %s"' % (str(Number), filename))
		else:
			Print('\n\nCrash file --> %s\nError number --> %s' % (filename, str(Number)), color2)
	except:
		Print_Error()
		if ONLINE:
			delivery(error_body)
		else:
			(body, color) = retry_body(error_body, color2)
			Print(body, color)

################ list handlers #################################################################

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_stage0_init(instance):
	STAGE0_INIT.append(instance)
def register_stage1_init(instance):
	STAGE1_INIT.append(instance)
def register_stage2_init(instance):
	STAGE2_INIT.append(instance)
def register_stage3_init(instance):
	STAGE3_INIT.append(instance)

def register_command_handler(instance, command, category = [], access = 0, desc = None, syntax = None, examples = []):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMSTAT[command] = {'col': 0, 'users': []}
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

################ call & execut handlers ########################################################

def ThreadError():
	Error = str(sys.exc_info()[1])
	if Error == "can't start new thread":
		return True
	return False

def Try_Thr(Thread, number = 0):
	if number >= 4:
		raise RuntimeError, 'Thread try limit!'
	try:
		Thread.start()
	except:
		Try_Thr(Thread, (number + 1))

def Thread_Run(Thread, handler, command = None):
	try:
		Thread.start()
	except:
		if ThreadError():
			try:
				Try_Thr(Thread)
			except RuntimeError:
				try:
					Thread.run()
				except:
					lytic_crashlog(handler, command)
		else:
			lytic_crashlog(Thread_Run, command)

def execute_message_handler(message_handler, raw, type, source, body):
	try:
		message_handler(raw, type, source, body)
	except:
		lytic_crashlog(message_handler)

def call_message_handlers(raw, type, source, body):
	for handler in MESSAGE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_message_handler, 'inmsg-%d' % (INFO['thr']),(handler, raw, type, source, body,))
			Thread_Run(Thread, handler)

def execute_outmsg_handler(outgoing_message_handler, target, body, obody):
	try:
		outgoing_message_handler(target, body, obody)
	except:
		lytic_crashlog(outgoing_message_handler)

def call_outgoing_message_handlers(target, body, obody):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_outmsg_handler, 'outmsg-%d' % (INFO['thr']),(handler, target, body, obody,))
			Thread_Run(Thread, handler)

def execute_join_handler(join_handler, conf, nick, afl, role):
	try:
		join_handler(conf, nick, afl, role)
	except:
		lytic_crashlog(join_handler)

def call_join_handlers(conf, nick, afl, role):
	for handler in JOIN_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_join_handler, 'join-%d' % (INFO['thr']),(handler, conf, nick, afl, role,))
			Thread_Run(Thread, handler)

def execute_leave_handler(leave_handler, conf, nick, reason, code):
	try:
		leave_handler(conf, nick, reason, code)
	except:
		lytic_crashlog(leave_handler)

def call_leave_handlers(conf, nick, reason, code):
	for handler in LEAVE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_leave_handler, 'leave-%d' % (INFO['thr']),(handler, conf, nick, reason, code,))
			Thread_Run(Thread, handler)

def execute_iq_handler(iq_handler, iq):
	try:
		iq_handler(iq)
	except:
		lytic_crashlog(iq_handler)

def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_iq_handler, 'iq-%d' % (INFO['thr']),(handler, iq,))
			Thread_Run(Thread, handler)

def execute_presence_handler(presence_handler, prs):
	try:
		presence_handler(prs)
	except:
		lytic_crashlog(presence_handler)

def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			Thread = threading.Thread(None, execute_presence_handler, 'prs-%d' % (INFO['thr']),(handler, prs,))
			Thread_Run(Thread, handler)

def execut_stage_init(stage_handler, conf = None):
	try:
		if conf:
			stage_handler(conf)
		else:
			stage_handler()
	except:
		lytic_crashlog(stage_handler)

def call_stage0_init():
	for handler in STAGE0_INIT:
		execut_stage_init(handler)

def call_stage1_init(conf):
	for handler in STAGE1_INIT:
		execut_stage_init(handler, conf)

def call_stage2_init():
	for handler in STAGE2_INIT:
		execut_stage_init(handler)

def call_stage3_init():
	for handler in STAGE3_INIT:
		execut_stage_init(handler)

def execute_command_handler(commnad_handler, command, type, source, body):
	try:
		commnad_handler(type, source, body)
	except:
		lytic_crashlog(commnad_handler, command)

def call_command_handlers(command, type, source, body, callee):
	real_access = MACROS.get_access(callee, source[1])
	if real_access <= 0:
		real_access = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source[0], real_access, source[1]):
			with smph:
				handler = COMMAND_HANDLERS[command]
				INFO['thr'] += 1
				Thread = threading.Thread(None, execute_command_handler, 'command-%d' % (INFO['thr']),(handler, command, type, source, body,))
				Thread_Run(Thread, handler, command)
			COMMSTAT[command]['col'] += 1
			jid = handler_jid(source[0])
			if jid not in COMMSTAT[command]['users']:
				COMMSTAT[command]['users'].append(jid)
		else:
			reply(type, source, u'недостаточный доступ')

################ load pugins ###################################################################

def load_plugins():
	Print('\n\nLOADING PLUGINS:', color4)
	ltc, tal, Npl = [], [], []
	for Plugin in os.listdir(PLUGIN_DIR):
		Ext = Plugin[-3:].lower()
		if Ext == '.py':
			filename = '%s/%s' % (PLUGIN_DIR, Plugin)
			try:
				data = file(filename).read(20)
			except:
				data = '# |-| levaya shnyaga |-|'
			Plug = Plugin.split('_pl')
			if data.count('lytic'):
				try:
					execfile(filename, globals()); ltc.append(Plug[0])
				except:
					Npl.append(Plug[0])
			elif data.count('talis'):
				try:
					execfile(filename, globals()); tal.append(Plug[0])
				except:
					Npl.append(Plug[0])
			else:
				Npl.append(Plug[0])
	if ltc:
		lts = ', '.join(sorted(ltc))
		Print(('\n\nLoaded %d BlackSmith plugins:\n' % len(ltc))+lts, color3)
	if tal:
		ts = ', '.join(sorted(tal))
		Print(('\n\nLoaded %d Talisman plugins:\n' % len(tal))+ts, color1)
	if Npl:
		Ns = ', '.join(sorted(Npl))
		Print(('\n\nThere are %d unloadable plugins:\n' % len(Npl))+Ns, color2)
	else:
		Print('\n\nThere are not unloadable plugins!', color3)

################ other handlers ################################################################

def load_roster_config():
	if initialize_file(ROSTER_FILE, str(RSTR)):
		globals()['RSTR'] = eval(read_file(ROSTER_FILE))
	else:
		Print('\n\nError: roster config file is not exist!', color2)

def load_quests():
	if os.path.exists(QUESTIONS_FILE):
		globals()['QUESTIONS'] = eval(read_file(QUESTIONS_FILE))
	else:
		Print('\n\nError: questions file is not exist!', color2)

def read_pipe(command):
	try:
		pipe = os.popen(command)
		data = pipe.read()
		pipe.close()
		if BOT_OS == 'nt':
			data = data.decode('cp866')
	except:
		data = '(error)'
	return data

read_link = lambda link: urllib.urlopen(link).read()

def read_url(link, Browser = False):
	req = urllib2.Request(link)
	if Browser:
		req.add_header('User-agent', Browser)
	site = urllib2.urlopen(req)
	data = site.read()
	return data

def re_search(lt, key, key2):
	lt = lt[re.search(key, lt).end():]
	data = lt[:re.search(key2, lt).start()]
	return data.strip()

def handler_botnick(conf):
	if conf in BOT_NICKS:
		return BOT_NICKS[conf]
	return DEFAULT_NICK

def handler_jid(instance):
	if (type(instance) is types.InstanceType):
		instance = unicode(instance)
	list = string.split(instance, '/', 1)
	if (len(list) == 2) and GROUPCHATS.has_key(list[0]):
		return GROUPCHATS[list[0]].get(list[1], {'jid': list[0]})['jid']
	return list[0]

def save_conflist(conf, nick = None, code = None):
	if initialize_file(GROUPCHATS_FILE):
		list = eval(read_file(GROUPCHATS_FILE))
		if conf not in list:
			list[conf] = {'nick': nick, 'code': code}
		elif nick and conf and code:
			list[conf] = {'nick': nick, 'code': code}
		elif nick and conf:
			list[conf]['nick'] = nick
		elif code and conf:
			list[conf]['code'] = code
		elif conf:
			del list[conf]
		write_file(GROUPCHATS_FILE, str(list))
	else:
		Print('\n\nError: can`t append conference to chatrooms list file!', color2)

def memory_usage():
	PID, memory = str(BOT_PID), '0'
	if BOT_OS == 'posix':
		lines = read_pipe('ps -o rss -p %s' % (PID)).splitlines()
		if len(lines) >= 2:
			memory = lines[1].strip()
	elif BOT_OS == 'nt':
		lines = read_pipe('TASKLIST /FI "IMAGENAME eq python.exe').splitlines()
		for line in lines:
			slist = line.split()
			if len(slist) >= 6 and PID == slist[1].strip():
				memory = '%s%s' % (slist[4].strip(), slist[5].strip())
				break
	return (0 if not check_number(memory) else int(memory))

def command_Prefix(conf, command):
	if command in [u'хелп', u'комлист', u'команды', u'префикс', u'тест']:
		return command
	if PREFIX[conf] == command[:1]:
		return command[1:]
	return 'none_command'

def Prefix_state(combody, bot_nick):
	cmd_nick = combody.split()[0]
	for symbol in [':', ',', '>']:
		cmd_nick = cmd_nick.replace(symbol, '')
	if cmd_nick != bot_nick:
		return False
	return True

def check_number(number):
	try:
		answer = number.isdigit()
	except:
		answer = False
	return answer

def replace_all(retxt, list, data = False):
	for x in list:
		retxt = retxt.replace(x, data if data != False else list[x])
	return retxt

def that_day():
	return int(time.strftime('%Y%m%d', time.gmtime()))

Elist = [' %s' % (x) for x in [u'0 мес', u'0 дн', u'0 час', u'0 мин', u'0 сек']]

def timeElapsed(or_seconds):
	minutes, seconds = divmod(or_seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	months, days = divmod(days, 30)
	years, months = divmod(months, 12)
	text = u'%d сек' % (seconds)
	if or_seconds >= 60:
		text = u'%d мин %s' % (minutes, text)
	if or_seconds >= 3600:
		text = u'%d час %s' % (hours, text)
	if or_seconds >= 86400:
		text = u'%d дн %s' % (days, text)
	if or_seconds >= 2592000:
		text = u'%d мес %s' % (months, text)
	if or_seconds >= 31104000:
		text = u'%d лет %s' % (years, text)
	return replace_all(text, Elist, '')

def upkeep():
	try:
		threading.Timer(360, upkeep).start()
	except:
		delivery(u'Внимание! Командуй --> "exec threading.Timer(360, upkeep).start()"')
	sys.exc_clear()
	if BOT_OS == 'nt':
		import msvcrt; msvcrt.heapmin()
	gc.collect()
	if MEMORY_LIMIT and memory_usage() >= MEMORY_LIMIT:
		sys_exit('memory leak')

################ access handlers ###############################################################

def load_access_levels():
	if initialize_file(GLOBACCESS_FILE):
		globals()['GLOBACCESS'] = eval(read_file(GLOBACCESS_FILE))
	else:
		Print('\n\nError: access file is not exist!', color2)

def form_admins_list():
	if BOSS not in GLOBACCESS:
		GLOBACCESS[BOSS] = 100
	for jid in GLOBACCESS:
		if GLOBACCESS[jid] >= 80:
			ADLIST.append(jid)

def change_local_access(conf, jid, level = 0):
	if conf not in ACCBYCONF:
		ACCBYCONF[conf] = {}
	if level:
		ACCBYCONF[conf][jid] = level
	else:
		ACCBYCONF[conf][jid] = 0

def change_global_access(jid, level = 0):
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]
	write_file(GLOBACCESS_FILE, str(GLOBACCESS))

def user_level(source, conf):
	jid, level = handler_jid(source), 10
	if GLOBACCESS.has_key(jid):
		level = GLOBACCESS[jid]
	elif CONFACCESS.has_key(conf) and CONFACCESS[conf].has_key(jid):
		level = CONFACCESS[conf][jid]
	elif ACCBYCONF.has_key(conf) and ACCBYCONF[conf].has_key(jid):
		level = ACCBYCONF[conf][jid]
	return level

def has_access(source, level, conf):
	if user_level(source, conf) >= int(level):
		return True
	return False

################ join/leave & message send handlers ############################################

def send_join_presece(conf, nick, code = None):
	Presence = xmpp.protocol.Presence('%s/%s' % (conf, nick))
	Presence.setStatus(STATUS[conf]['message'])
	Presence.setShow(STATUS[conf]['status'])
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	Pres = Presence.setTag('x', namespace = xmpp.NS_MUC)
	Pres.addChild('history', {'maxchars': '0'})
	if code:
		Pres.setTagData('password', code)
	JCON.send(Presence)

def join_groupchat(conf, nick, code = None):
	call_stage1_init(conf)
	if conf not in GROUPCHATS:
		GROUPCHATS[conf] = {}
	if conf not in STATUS:
		STATUS[conf] = {'message': 'BlackSmith by WitcherGeralt', 'status': 'chat'}
	save_conflist(conf, nick, code)
	send_join_presece(conf, nick, code)

def leave_groupchat(conf, status = None):
	Presence = xmpp.Presence(conf, 'unavailable')
	if status:
		Presence.setStatus(status)
	JCON.send(Presence)
	if conf in GROUPCHATS:
		del GROUPCHATS[conf]
	save_conflist(conf)

def handler_rebody(target, body, ltype):
	col, all = 0, str(len(body) / PRIV_MSG_LIMIT + 1)
	while len(body) > PRIV_MSG_LIMIT:
		col = col + 1
		text = '[%d/%s] %s[...]' % (col, all, body[:PRIV_MSG_LIMIT])
		JCON.send(xmpp.Message(target, text.strip(), ltype))
		body = body[PRIV_MSG_LIMIT:]
		time.sleep(2)
	return '[%d/%s] %s' % ((col + 1), all, body)

def delivery(body):
	if not isinstance(body, unicode):
		body = body.decode('utf-8', 'replace')
	INFA['outmsg'] += 1
	try:
		JCON.send(xmpp.Message(BOSS, body, 'chat'))
	except:
		file_add('delivery.txt', body)

def msg(target, body):
	if not isinstance(body, unicode):
		body = body.decode('utf-8', 'replace')
	obody = body
	if GROUPCHATS.has_key(target):
		ltype = 'groupchat'
		if len(body) > CHAT_MSG_LIMIT:
			body = body[:CHAT_MSG_LIMIT]+(u'[...]\n\n>>> Лимит %d знаков! Продолжение по команде "далее".' % (CHAT_MSG_LIMIT))
	else:
		ltype = 'chat'
		if len(body) > PRIV_MSG_LIMIT:
			body = handler_rebody(target, body, ltype)
	JCON.send(xmpp.Message(target, body.strip(), ltype))
	INFA['outmsg'] += 1
	call_outgoing_message_handlers(target, body, obody)

def reply(ltype, source, body):
	if not isinstance(body, unicode):
		body = body.decode('utf-8', 'replace')
	if ltype == 'public':
		body = '%s: %s' % (source[2], body)
		msg(source[1], body)
	elif ltype == 'private':
		msg(source[0], body)

def send_unavailable(status):
	Presence = xmpp.Presence(typ = 'unavailable')
	Presence.setStatus(status)
	JCON.send(Presence)

def change_bot_status(conf, text, status):
	Presence = xmpp.protocol.Presence('%s/%s' % (conf, handler_botnick(conf)))
	Presence.setStatus(text)
	Presence.setShow(status)
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	JCON.send(Presence)

################ role/afl iq handlers ##########################################################

def handler_iq_send(conf, item_name, item, afrls, afrl, rsn = None):
	stanza = xmpp.Iq(to = conf, typ = 'set')
	INFA['outiq'] += 1
	stanza.setID('lytic_%d' % (INFA['outiq']))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	afl_role = query.addChild('item', {item_name: item, afrls: afrl})
	if rsn:
		afl_role.setTagData('reason', rsn)
	stanza.addChild(node = query)
	JCON.send(stanza)

def handler_unban(conf, jid):
	handler_iq_send(conf, 'jid', jid, 'affiliation', 'none')
def handler_banjid(conf, jid, reason):
	handler_iq_send(conf, 'jid', jid, 'affiliation', 'outcast', reason)
def handler_ban(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'affiliation', 'outcast', reason)
def handler_none(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'affiliation', 'none', reason)
def handler_member(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'affiliation', 'member', reason)
def handler_admin(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'affiliation', 'admin', reason)
def handler_owner(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'affiliation', 'owner', reason)
def handler_kick(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'role', 'none', reason)
def handler_visitor(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'role', 'visitor', reason)
def handler_participant(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'role', 'participant', reason)
def handler_moder(conf, nick, reason):
	handler_iq_send(conf, 'nick', nick, 'role', 'moderator', reason)

################ message handler & others ######################################################

def roster_check(instance, body):
	if instance not in ANSWER:
		QA = random.choice(QUESTIONS.keys())
		ANSWER[instance] = {'key': QUESTIONS[QA]['answer'], 'tryes': 0}
		msg(instance, u'Привет! Мне нужно убедиться что ты не бот, %s, У тебя три попытки и 1 минута!' % (QUESTIONS[QA]['question']))
		INFO['thr'] += 1
		try:
			threading.Timer(60, roster_timer,(instance,)).start()
		except:
			LAST['null'] += 1
	elif ANSWER[instance]['tryes'] >= 3:
		roster_ban(instance)
	elif ANSWER[instance]['key'] == body.lower():
		RSTR['AUTH'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Праильно! Вэлкам!')
		ROSTER.Authorize(instance)
		ROSTER.Subscribe(instance)
		ROSTER.setItem(instance, instance, ['USERS'])
		del ANSWER[instance]
		delivery(u'Контакт %s прошел IQ проверку и был добавлен в группу "USERS"!' % (instance))
	else:
		ANSWER[instance]['tryes'] += 1
		msg(instance, u'Включи мозг! Неправильно!')

def roster_ban(instance):
	if not instance.count('@conf'):
		RSTR['BAN'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Поздравляю ты в бане!')
		ROSTER.Unsubscribe(instance)
		if instance in ROSTER.getItems():
			ROSTER.delItem(instance)
		del ANSWER[instance]
		delivery(u'Контакт %s не прошел IQ проверку и был добавлен в ростер бан!' % (instance))

def roster_timer(roster_user):
	if roster_user not in (RSTR['AUTH'] + RSTR['BAN']):
		roster_ban(roster_user)

def feil_message(fromjid, instance, bot_nick, body, error):
	if error == '500':
		time.sleep(0.6)
		msg(fromjid, body)
	elif error == '406':
		send_join_presece(instance, bot_nick)
		time.sleep(0.6)
		msg(fromjid, body)

def kill_flooder(flooder, roster, nick, instance):
	change_global_access(flooder, -100)
	if roster:
		delivery(u'Внимание! %s флудит мне в ростер!' % (flooder))
	else:
		botnick = handler_botnick(instance)
		handler_kick(instance, nick, '%s: flooder!' % (botnick))
	try:
		threading.Timer(360, change_global_access,(flooder, -5)).start()
	except:
		LAST['null'] += 1

def flood_timer(fromjid, instance, nick):
	STOP['mto'] += 1
	if STOP['mto'] >= 4:
		if instance in GROUPCHATS or instance.count('@conf'):
			flooder, roster = handler_jid(fromjid), False
		else:
			flooder, roster = instance, True
		if flooder not in STOP['jids']:
			STOP['jids'][flooder] = 1
			time.sleep(6)
			STOP['jids'][flooder] -= 1
		else:
			STOP['jids'][flooder] += 1
			if flooder not in ADLIST and STOP['jids'][flooder] >= 4:
				if flooder.count('@') and flooder.count('.'):
					kill_flooder(flooder, roster, nick, instance)
					time.sleep(6)
					del STOP['jids'][flooder]
				else:
					botnick = handler_botnick(instance)
					handler_kick(fromjid, nick, '%s: flooder!' % (botnick))
					time.sleep(6)
					del STOP['jids'][flooder]
			else:
				time.sleep(6)
				STOP['jids'][flooder] -= 1
		STOP['mto'] -= 1
	else:
		time.sleep(4)
		STOP['mto'] -= 1

def MESSAGE_PROCESSING(client, stanza):
	fromjid = stanza.getFrom()
	INFO['msg'] += 1
	instance = fromjid.getStripped()
	if user_level(fromjid, instance) <= -100:
		return
	if instance in UNAVALABLE and not MSERVE:
		return
	if stanza.timestamp:
		return
	nick = fromjid.getResource()
	bot_nick = handler_botnick(instance)
	if bot_nick == nick:
		return
	body = stanza.getBody()
	if body:
		body = body.strip()
	if not body:
		return
	if instance not in GROUPCHATS and instance not in ADLIST:
		if not instance.count('@conf'):
			if instance in RSTR['BAN'] or RSTR['VN'] == 'off':
				return
			elif instance not in RSTR['AUTH'] and RSTR['VN'] == 'iq':
				INFO['thr'] += 1
				Thread = threading.Thread(None, roster_check, 'rIQ-%d' % (INFO['thr']),(instance, body,))
				Thread_Run(Thread, roster_check)
				return
	if len(body) > INC_MSG_LIMIT:
		body = body[:INC_MSG_LIMIT]+('[...] limit %d symbols' % (INC_MSG_LIMIT))
	ltype = stanza.getType()
	if ltype == 'groupchat':
		if instance in GROUPCHATS and nick in GROUPCHATS[instance]:
			GROUPCHATS[instance][nick]['idle'] = time.time()
		type = 'public'
	elif ltype == 'error':
		if instance in GROUPCHATS:
			feil_message(fromjid, instance, bot_nick, body, stanza.getErrorCode())
		return
	else:
		type = 'private'
	INFO['thr'] += 1
	try:
		threading.Thread(None, flood_timer, 'timer-%d' % (INFO['thr']),(fromjid, instance, nick,)).start()
	except:
		LAST['null'] += 1
	command, Parameters, cbody, rcmd, combody = '', '', '', '', body
	for key in [bot_nick+key for key in [':',',','>']]:
		combody = combody.replace(key, '')
	combody = combody.strip()
	if not combody:
		return
	if STOP['mto'] >= 4:
		return
	rcmd = combody.split()[0].lower()
	if instance in COMMOFF and rcmd in COMMOFF[instance]:
##		reply(type, [fromjid, instance, nick], u'команда "%s" здесь отключена' % (rcmd))
		return
	cbody = MACROS.expand(combody, [fromjid, instance, nick])
	if instance in MACROS.macrolist.keys():
		cmds = (MACROS.gmacrolist.keys() + MACROS.macrolist[instance].keys())
	else:
		cmds = MACROS.gmacrolist.keys()
	command = cbody.split()[0].lower()
	if instance in PREFIX and rcmd not in cmds:
		NotPfx = Prefix_state(body, bot_nick)
		if NotPfx or ltype == 'chat':
			if not COMMANDS.has_key(command) and command[:1] in ['!','@','#','.','*']:
				command = command[1:]
		else:
			command = command_Prefix(instance, command)
	if instance in COMMOFF and command in COMMOFF[instance]:
##		reply(type, [fromjid, instance, nick], u'команда "%s" здесь отключена' % (command))
		return
	if cbody.count(' '):
		Parameters = cbody[(cbody.find(' ') + 1):].strip()
	if COMMANDS.has_key(command):
		INFO['cmd'] += 1
		LAST['cmd'] = u'Помощь по команде "хелп" (последнее действие - "%s")' % (command)
		call_command_handlers(command, type, [fromjid, instance, nick], unicode(Parameters), rcmd)
		LAST['time'] = time.time()
	else:
		call_message_handlers(stanza, type, [fromjid, instance, nick], body)

################ presence handler & others #####################################################

def status_code_change(items, conf, nick):
	for item in items:
		try:
			del GROUPCHATS[conf][nick][item]
		except:
			LAST['null'] += 1

def error_join_timer(conf):
	if conf in GROUPCHATS:
		send_join_presece(conf, handler_botnick(conf))

def roster_subscribe(jid):
	if jid in ADLIST:
		ROSTER.Authorize(jid)
		ROSTER.setItem(jid, jid, ['ADMINS'])
	elif RSTR['VN'] == 'off':
		ROSTER.Unauthorize(jid)
		if jid in ROSTER.getItems():
			ROSTER.delItem(jid)
	elif jid not in RSTR['BAN'] and RSTR['VN'] in ['iq', 'on']:
		ROSTER.Authorize(jid)
		ROSTER.setItem(jid, jid, ['USERS'])

def moder_presence(conf):
	UNAVALABLE.remove(conf)
	msg(conf, u'Походу дали модера, перезахожу!')
	time.sleep(2)
	leave_groupchat(conf, 'Rejoin...')
	time.sleep(2)
	join_groupchat(conf, handler_botnick(conf))

def PRESENCE_PROCESSING(client, Prs):
	fromjid = Prs.getFrom()
	INFO['prs'] += 1
	conf = fromjid.getStripped()
	if not has_access(fromjid, -5, conf):
		return
	Ptype = Prs.getType()
	if Ptype == 'subscribe':
		roster_subscribe(conf)
	if GROUPCHATS.has_key(conf):
		nick = fromjid.getResource()
		if Ptype == 'unavailable':
			reason = Prs.getReason() or Prs.getStatus()
			if nick in GROUPCHATS[conf] and GROUPCHATS[conf][nick]['ishere']:
				GROUPCHATS[conf][nick]['ishere'] = False
			scode = Prs.getStatusCode()
			if scode == '303':
				full_jid = Prs.getJid()
				if not full_jid:
					full_jid = unicode(fromjid)
					jid = unicode(fromjid)
				else:
					full_jid = unicode(full_jid)
					jid = string.split(full_jid, '/', 1)[0]
				newnick = Prs.getNick()
				join_date = GROUPCHATS[conf].get(nick, {'join_date': [that_day(), time.gmtime()]})['join_date']
				joined = GROUPCHATS[conf].get(nick, {'joined': time.time()})['joined']
				GROUPCHATS[conf][newnick] = {'full_jid': full_jid, 'jid': jid, 'join_date': join_date, 'idle': time.time(), 'joined': joined, 'ishere': True}
				status_code_change(['idle','full_jid'], conf, nick)
			else:
				status_code_change(['idle','full_jid','joined'], conf, nick)
				call_leave_handlers(conf, nick, reason, scode)
		elif Ptype in ['available', None]:
			full_jid = Prs.getJid()
			if not full_jid:
				if MSERVE:
					if conf not in UNAVALABLE:
						UNAVALABLE.append(conf)
					full_jid = unicode(fromjid)
					jid = full_jid
				else:
					if conf not in UNAVALABLE:
						UNAVALABLE.append(conf)
						msg(conf, u'Отключаюсь до получения прав админа!')
						change_bot_status(conf, u'Отказываюсь работать без прав!', 'xa')
					return
			elif conf in UNAVALABLE:
				if MSERVE:
					UNAVALABLE.remove(conf)
					full_jid = unicode(full_jid)
					jid = string.split(full_jid, '/', 1)[0]
				else:
					moder_presence(conf)
					return
			else:
				full_jid = unicode(full_jid)
				jid = string.split(full_jid, '/', 1)[0]
			if nick in GROUPCHATS[conf] and GROUPCHATS[conf][nick]['jid'] == jid and GROUPCHATS[conf][nick]['ishere']:
				LAST['null'] += 1
			else:
				GROUPCHATS[conf][nick] = {'full_jid': full_jid, 'jid': jid, 'join_date': [that_day(), time.gmtime()], 'idle': time.time(), 'joined': time.time(), 'ishere': True}
				afl = Prs.getAffiliation()
				role = Prs.getRole()
				call_join_handlers(conf, nick, afl, role)
		elif Ptype == 'error':
			ecode = Prs.getErrorCode()
			if ecode:
				if ecode == '409':
					BOT_NICKS[conf] = '%s.' % (nick)
					send_join_presece(conf, handler_botnick(conf))
				elif ecode == '404':
					del GROUPCHATS[conf]
					delivery(u'Ошибка %s (сервер не найден) - конфа: "%s"' % (ecode, conf))
				elif ecode in ['301','307','401','403','405']:
					leave_groupchat(conf, u'Got %s error code!' % str(ecode))
					delivery(u'Ошибка %s, пришлось выйти из -> "%s"' % (ecode, conf))
				elif ecode == '503':
					try:
						threading.Timer(180, error_join_timer,(conf,)).start()
					except:
						LAST['null'] += 1
		call_presence_handlers(Prs)

################ iq handler ####################################################################

def IQ_PROCESSING(client, stanza):
	fromjid = stanza.getFrom()
	INFO['iq'] += 1
	instance = fromjid.getStripped()
	if user_level(fromjid, instance) <= -100:
		return
	Itype = stanza.getType()
	if Itype != 'error':
		if stanza.getTags('query', {}, xmpp.NS_VERSION):
			result = stanza.buildReply('result')
			query = result.getTag('query')
			query.setTagData('name', BOT_VERSION(BOT_VER, CORE_MODE))
			query.setTagData('version', BOT_REVISION(BOT_REV))
			PyVer = str(sys.version).split()[0]
			if BOT_OS == 'nt':
				os_name = read_pipe('ver').strip()
			elif BOT_OS == 'posix':
				os_name = os.uname()[0]
			else:
				os_name = 'Unknown[OS]'
			query.setTagData('os', '%s / PyVer[%s]' % (os_name, PyVer))
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif stanza.getTags('time', {}, 'urn:xmpp:time'):
			tzo = (lambda tup: tup[0]+"%02d:" % tup[1]+"%02d" % tup[2])((lambda t: tuple(['+' if t < 0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
			utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
			result = stanza.buildReply('result')
			repl = result.addChild('time', {}, [], 'urn:xmpp:time')
			repl.setTagData('tzo', tzo)
			repl.setTagData('utc', utc)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif stanza.getTags('query', {}, xmpp.NS_DISCO_INFO):
			ids = []
			ids.append({'category': 'client','type': 'bot','name': 'lytic'})
			features = [xmpp.NS_DISCO_INFO, xmpp.NS_DISCO_ITEMS, xmpp.NS_MUC, 'urn:xmpp:time', xmpp.NS_PING, xmpp.NS_VERSION, xmpp.NS_PRIVACY, xmpp.NS_ROSTER, xmpp.NS_VCARD, xmpp.NS_DATA, xmpp.NS_LAST, xmpp.NS_COMMANDS, xmpp.NS_TIME, xmpp.NS_MUC_FILTER]
			info = {'ids': ids,'features': features}
			pybr = xmpp.browser.Browser()
			pybr.PlugIn(JCON)
			pybr.setDiscoHandler({'items': [],'info': info})
		elif stanza.getTags('query', {}, xmpp.NS_LAST):
			last = time.time() - LAST['time']
			result = stanza.buildReply('result')
			query = result.getTag('query')
			query.setAttr('seconds', int(last))
			query.setData(LAST['cmd'])
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif stanza.getTags('query', {}, xmpp.NS_TIME):
			timedisp = time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.localtime())
			timeutc = time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
			result = xmpp.Iq('result')
			result.setTo(fromjid)
			result.setID(stanza.getID())
			query = result.addChild('query', {}, [], xmpp.NS_TIME)
			query.setTagData('utc', timeutc)
			query.setTagData('display', timedisp)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif stanza.getTags('ping', {}, xmpp.NS_PING):
			result = xmpp.Iq('result')
			result.setTo(stanza.getFrom())
			result.setID(stanza.getID())
			JCON.send(result)
			raise xmpp.NodeProcessed
	call_iq_handlers(stanza)

################ starting actions & lytic restart ##############################################

def starting_actions():
	load_access_levels()
	form_admins_list()
	load_roster_config()
	load_quests()
	load_plugins()

def col_minus():
	if DCNT['col']:
		DCNT['col'] += -1

def lytic_restart():
	DCNT['col'] += 1
	if DCNT['Yes!'] and DCNT['col'] >= 3:
		DCNT['Yes!'] = False
		globals()['ONLINE'] = False
		Print('\n\nDISCONNECTED', color2)
		call_stage3_init()
		Exit('\n\nRESTARTING...', 0, 30)
	try:
		threading.Timer(3, col_minus).start()
	except:
		LAST['null'] += 1

def Dispatch_handler():
	try:
		JCON.Process(8)
	except BadlyFormedStanza:
		LAST['null'] += 1
	except KeyboardInterrupt:
		sys_exit('INTERUPT (Ctrl+C)')

def sys_exit(exit_reason = 'SUICIDE'):
	Print('\n\n%s' % (exit_reason), color2)
	if ONLINE:
		send_unavailable(exit_reason)
	if time.time() - INFO['start'] >= 30:
		call_stage3_init()
	Exit('\n\nRESTARTING...\n\nPress Ctrl+C to exit', 0, 30)

################ Bot starting ##################################################################

def lytic():
	Print('\n\n--> BOT STARTED\n\n\nChecking PID...', color4)
	if os.path.exists(PID_FILE):
		CACHE = eval(read_file(PID_FILE))
		PID = CACHE['PID']
		if PID != BOT_PID:
			if BOT_OS == 'nt':
				kill = 'TASKKILL /PID %d /T /f' % (PID)
				os.system(kill)
			else:
				killed = 'PID: %d - has been killed!' % (PID)
				try:
					os.kill(PID, 9)
				except:
					killed = 'Last PID wasn`t detected!'
				Print(killed, color3)
			CACHE = {'PID': BOT_PID, 'START': time.time(), 'REST': []}
		else:
			CACHE['REST'].append(time.strftime('%d.%m.%Y (%H:%M:%S)', time.localtime()))
	else:
		CACHE = {'PID': BOT_PID, 'START': time.time(), 'REST': []}
	Print('\nBot`s PID: %d' % (BOT_PID), color4)
	write_file(PID_FILE, str(CACHE))
	globals()['RUNTIMES'] = {'START': CACHE['START'], 'REST': CACHE['REST']}
	Print('\n\nGENERAL CONFIG:\n\nBOT JID: %s@%s\nJID PASS: %s\nBOSS JID: %s\nBOSS PASS: %s' % (USERNAME, HOST, PASSWORD, BOSS, BOSS_PASS), color4)
	globals()['JCON'] = xmpp.Client(server = HOST, port = PORT, debug = [])
	starting_actions()
	Print('\n\nConnecting...', color4)
	if SECURE:
		CONNECT = JCON.connect(server = (SERVER, PORT), use_srv = False)
	else:
		CONNECT = JCON.connect(server = (SERVER, PORT), secure = 0, use_srv = True)
	if CONNECT:
		if SECURE and CONNECT != 'tls':
			Print('\nWarning: unable to estabilish secure connection - TLS failed!', color2)
		else:
			Print('\nConnection is OK', color3)
		Print('Using: %s' % str(JCON.isConnected()), color4)
	else:
		Exit('\nFucking Connect!!\nSleep for 30 seconds', 0, 30)
	Print('\nAuthentication plese wait...', color4)
	AUTHENT = JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if AUTHENT:
		if AUTHENT != 'sasl':
			Print('\nWarning: unable to perform SASL auth. Old authentication method used!', color2)
		else:
			Print('Auth is OK', color3)
	else:
		Auth_error = unicode(JCON.lastErr)
		Error_code = unicode(JCON.lastErrCode)
		Exit('\nAuth error!!!\nError: %s %s' % (Auth_error, Error_code), 0, 12)
	globals()['ONLINE'] = True
	globals()['ROSTER'] = JCON.getRoster()
	call_stage0_init()
	JCON.RegisterHandler('message', MESSAGE_PROCESSING)
	JCON.RegisterHandler('presence', PRESENCE_PROCESSING)
	JCON.RegisterHandler('iq', IQ_PROCESSING)
	JCON.RegisterDisconnectHandler(lytic_restart)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	JCON.sendInitPresence()
	Print('\n\nYahoo! I am online!', color3)
	if initialize_file(GROUPCHATS_FILE):
		CONFS = eval(read_file(GROUPCHATS_FILE))
		Print('\n\nThere are %d rooms in list:' % len(CONFS), color4)
		for conf in CONFS:
			list = ['Joined %s' % (conf), 'Joined conference!', 'Can`t join %s' % (conf), 'Unable conference!']
			if check_nosimbols(conf):
				Number = 0
			else:
				Number = 1
			BOT_NICKS[conf] = CONFS[conf]['nick']
			try:
				Fuck = join_groupchat(conf, handler_botnick(conf), CONFS[conf]['code'])
			except:
				Fuck = True
			if not Fuck:
				state, color =  list[Number], color3
			else:
				state, color =  list[Number + 2], color2
			Print(state, color)
	else:
		Print('\n\nError: unable to create chatrooms list file!', color2)
	Print('\n\nBlackSmith is ready to work!\n\n', color3)
	INFO['start'] = time.time()
	upkeep()
	call_stage2_init()
	CAN_LIVE = True
	while CAN_LIVE:
		try:
			Dispatch_handler()
		except:
			Dispatch_fail()
			INFO['errs'] += 1
			if INFO['errs'] >= 7:
				CAN_LIVE = False
	sys_exit('Dispatch Errors')

if __name__ == "__main__":
	while True:
		try:
			lytic()
		except KeyboardInterrupt:
			sys_exit('INTERUPT (Ctrl+C)')
		except:
			lytic_crashlog(lytic)
		try_sleep(30)

### end ########################################################################################