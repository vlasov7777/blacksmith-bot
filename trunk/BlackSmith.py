#! /usr/bin/env python
# /* coding: utf-8 */

#  BlackSmith Bot Core
#  BlackSmith.py

#  Thanks to:
#    Als [Als@exploit.in]
#    Evgen [meb81@mail.ru]
#    dimichxp [dimichxp@gmail.com]
#    Boris Kotov [admin@avoozl.ru]
#    Mike Mintz [mikemintz@gmail.com]

#  This program distributed under Apache 2.0 license.
#  See license.txt for more details.
#  © WitcherGeralt, based on Talisman by Als (Neutron by Gh0st)
#  The new bot life © simpleApps.

## Imports.
from __future__ import with_statement
from urllib2 import urlopen
from traceback import format_exc, print_exc
import gc, os, re, sys, time, random, threading

## Set "sys.path".
if not (hasattr(sys, "argv") and sys.argv and sys.argv[0]):
	sys.argv = [__file__]
	
os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, "library.zip")

from enconf import *
import xmpp, macros, simplejson

## Stats.
INFO = {'start': 0, 'msg': 0, 'prs': 0, 'iq': 0, 'cmd': 0, 'thr': 0, 'errs': 0}
INFA = {'outmsg': 0, 'outiq': 0, 'fr': 0, 'fw': 0, 'fcr': 0, 'cfw': 0}
RSTR = {'AUTH': [], 'BAN': [], 'VN': 'off'}
LAST = {'time': 0, 'cmd': 'start'}
DCNT = {'col': 0, 'Yes!': True}
STOP = {'mto': 0, 'jids': {}}

## Colored stdout.
color0 = chr(27) + "[0m"
color1 = chr(27) + "[33m"
color2 = chr(27) + "[31;1m"
color3 = chr(27) + "[32m"
color4 = chr(27) + "[34;1m"
colored = xmpp.debug.colors_enabled

def retry_body(x, y):
	try: body = unicode(x)
	except: color = False
	return (body, color)

def text_color(text, color):
	if colored:
		text = color+text+color0
	return text

def Print(text, color = False):
	try:
		if color:
			text = text_color(text, color)
		print text
	except:
		pass

## Increase convenience.
def try_sleep(slp):
	try:
		time.sleep(slp)
	except KeyboardInterrupt:
		os._exit(0)

def Exit(text, exit, slp):
	Print(text, color2); try_sleep(slp)
	if exit:
		os._exit(0)
	else:
		os.execl(sys.executable, sys.executable, os.path.abspath(sys.argv[0]))

## Configuration.
GENERAL_CONFIG_FILE = 'static/source.py'
GLOBACCESS_FILE = 'dynamic/access.txt'
GROUPCHATS_FILE = 'dynamic/chats.txt'
QUESTIONS_FILE = 'static/veron.txt'
ROSTER_FILE = 'dynamic/roster.txt'
PLUGIN_DIR = 'extensions'
PID_FILE = 'PID.txt'

BOT_OS, BOT_PID = os.name, os.getpid()

def PASS_GENERATOR(codename, Number):
	symbols = "".join(ascii_tab)
	for Numb in xrange(Number):
		codename += random.choice(symbols)
	return codename

try:
	execfile(GENERAL_CONFIG_FILE)
	execfile('static/versions.py')
	reload(sys).setdefaultencoding('utf-8')
except Exception, e:
	Print('\n\nError: %s' % `e`, color2)

if BOT_OS == 'nt':
	os.system('Title BlackSmith - %s' % (Caps))

MEMORY_LIMIT = (24576 if MEMORY_LIMIT and MEMORY_LIMIT <= 24576 else MEMORY_LIMIT)

## Lists of handlers.
IQ_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
MESSAGE_HANDLERS = []
COMMAND_HANDLERS = {}
PRESENCE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []

STAGE0_INIT = []
STAGE1_INIT = []
STAGE2_INIT = []
STAGE3_INIT = []

## Dictionaries, lists.
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

MACROS = macros.Macros()

wsmph, smph = threading.Semaphore(), threading.Semaphore(60)

from sTools import *
## os info.
if os.name == "nt":
	if not ntDetect().lower().count("windows"):
		isOS = ntDetect()
	else:
		isOS = "Windows"
	from platform import win32_ver
	os_name = " ".join([isOS, win32_ver()[0], win32_ver()[2]])
	del win32_ver

elif os.name == "posix":
	from platform import dist
	if dist()[0]:
		os_name = "POSIX (%s with %s, %s)" % (dist()[0], 
											  os.uname()[0], os.uname()[2])
	else:
		os_name = "POSIX (%s, %s)" % (os.uname()[0], os.uname()[2])
	if os.uname()[0].lower().count("darwin"):
		print "#! Warning: The Darwin kernel poorly maintained."
	del dist
else:
	os_name = os.name.upper()
os_name = os_name.strip() + " " + getArchitecture()
del ntDetect, getArchitecture

## File workers.
def check_file(conf = None, file = None, data = "{}"):
	if conf:
		filename = chkFile('dynamic/%s/%s' % (conf, file))
	else:
		filename = 'dynamic/%s' % (file)
	return initialize_file(filename, data)

def initialize_file(name, data = "{}"):
	name = chkFile(name)
	if len(name.split('/')) >= 4:
		return False
	if os.path.exists(name):
		return True
	try:
		folder = os.path.dirname(name)
		if folder and not os.path.exists(folder):
			os.makedirs(folder, 0755)
		write_file(name, data)
		INFA['fcr'] += 1
	except:
		lytic_crashlog(initialize_file)
		return False
	return True

def read_file(name):
	fl = open(chkFile(name), "r")
	text = fl.read()
	INFA['fr'] += 1
	fl.close()
	return text

def write_file(name, data, mode = "w"):
	with wsmph:
		fl = open(chkFile(name), mode)
		fl.write(data)
		fl.close()
		INFA['fw'] += 1

## Crashfile writers.
def Dispatch_fail():
	crashfile = open('__main__.crash', 'a')
	print_exc(limit = None, file = crashfile)
	print "\n\n#-# Dispatch Error!"
	crashfile.close()

def lytic_crashlog(handler, command = None):
	DIR, handler, Number, error_body = "feillog", handler.func_name, (len(ERRORS.keys()) + 1), format_exc()
	ERRORS[Number] = error_body
	text = str()
	if JCON.isConnected():
		if command:
			error = u'команды "%s" (%s)' % (command, handler)
		else:
			error = u'процесса "%s"' % (handler)
		text += u'При выполнении %s --> произошла ошибка!' % (error)
	else:
		Print('\n\nError: can`t execute "%s"!' % (handler), color2)
	filename = (DIR+'/error[%s]%s.crash') % (str(INFA['cfw'] + 1), time.strftime('[%H.%M.%S][%d.%m.%Y]'))
	try:
		if not os.path.exists(DIR):
			os.mkdir(DIR, 0755)
		crashfile = open(filename, 'w')
		INFA['cfw'] += 1
		print_exc(limit = None, file = crashfile)
		crashfile.close()
		if JCON.isConnected():
			if BOT_OS == 'nt':
				delivery(text + u' Ошибку смотри по команде --> "ошибка %s" (Крэшфайл --> %s)' % (str(Number), filename))
			else:
				delivery(text + u' Ошибку смотри по командам --> "ошибка %s", "sh cat %s"' % (str(Number), filename))
		else:
			Print('\n\nCrash file --> %s\nError number --> %s' % (filename, str(Number)), color2)
	except:
		print_exc()
		if JCON.isConnected():
			delivery(error_body)
		else:
			(body, color) = retry_body(error_body, color2)
			Print(body, color)

## Handlers register.
def register_message_handler(instance):
	name = instance.func_name
	for handler in MESSAGE_HANDLERS:
		if name == handler.func_name:
			MESSAGE_HANDLERS.remove(handler)
	MESSAGE_HANDLERS.append(instance)

def register_outgoing_message_handler(instance):
	name = instance.func_name
	for handler in OUTGOING_MESSAGE_HANDLERS:
		if name == handler.func_name:
			OUTGOING_MESSAGE_HANDLERS.remove(handler)
	OUTGOING_MESSAGE_HANDLERS.append(instance)

def register_join_handler(instance):
	name = instance.func_name
	for handler in JOIN_HANDLERS:
		if name == handler.func_name:
			JOIN_HANDLERS.remove(handler)
	JOIN_HANDLERS.append(instance)

def register_leave_handler(instance):
	name = instance.func_name
	for handler in LEAVE_HANDLERS:
		if name == handler.func_name:
			LEAVE_HANDLERS.remove(handler)
	LEAVE_HANDLERS.append(instance)

def register_iq_handler(instance):
	name = instance.func_name
	for handler in IQ_HANDLERS:
		if name == handler.func_name:
			IQ_HANDLERS.remove(handler)
	IQ_HANDLERS.append(instance)

def register_presence_handler(instance):
	name = instance.func_name
	for handler in PRESENCE_HANDLERS:
		if name == handler.func_name:
			PRESENCE_HANDLERS.remove(handler)
	PRESENCE_HANDLERS.append(instance)

def register_stage0_init(instance):
	name = instance.func_name
	for handler in STAGE0_INIT:
		if name == handler.func_name:
			STAGE0_INIT.remove(handler)
	STAGE0_INIT.append(instance)

def register_stage1_init(instance):
	name = instance.func_name
	for handler in STAGE1_INIT:
		if name == handler.func_name:
			STAGE1_INIT.remove(handler)
	STAGE1_INIT.append(instance)

def register_stage2_init(instance):
	name = instance.func_name
	for handler in STAGE2_INIT:
		if name == handler.func_name:
			STAGE2_INIT.remove(handler)
	STAGE2_INIT.append(instance)

def register_stage3_init(instance):
	name = instance.func_name
	for handler in STAGE3_INIT:
		if name == handler.func_name:
			STAGE3_INIT.remove(handler)
	STAGE3_INIT.append(instance)

## Old plugins compability.
def register_command_handler(instance, command, category = [], access = 0, desc = None, syntax = None, examples = []):
	command = command.decode('utf-8')
	if not COMMSTAT.has_key(command):
		COMMSTAT[command] = {'col': 0, 'users': []}
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'access': access, 'desc': desc.decode('utf-8'), 'syntax': syntax.decode('utf-8'), 'examples': [ex.decode('utf-8') for ex in examples]}
	
## New command handler.
def command_handler(instance, access = 0, plug = "default"):
	try:
		command = eval(read_file("help/%s" % plug).decode('utf-8'))[instance.func_name]["cmd"]
	except:
		print_exc()
		Print("\nPlugin \"%s\" has no help." % plug, color2)
		command = instance.func_name
	if not COMMSTAT.get(command):
		COMMSTAT[command] = {'col': 0, 'users': []}
	if COMMANDS.get(command) or COMMAND_HANDLERS.get(command):
		Print("\nCommands in \"%s\" and \"%s\" are repeated." % (plug, COMMANDS[command].get("plug")), color2)
		command = instance.func_name
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'plug': plug, 'access': access}

## Call, execute handlers.
def Try_Thr(Thr, Number = 0):
	if Number >= 4:
		raise RuntimeError("exit")
	try:
		Thr.start()
	except threading.ThreadError:
		Try_Thr(Thr, (Number + 1))
	except:
		lytic_crashlog(Thr.start)

def Thread_Run(Thr, handler, command = None):
	try:
		Thr.start()
	except threading.ThreadError:
		if (str(sys.exc_info()[1]) == "can't start new thread"):
			try:
				Try_Thr(Thr)
			except RuntimeError:
				try:
					Thr.run()
				except KeyboardInterrupt:
					raise KeyboardInterrupt("Interrupt (Ctrl+C)")
				except:
					lytic_crashlog(handler, command)
		else:
			lytic_crashlog(Thread_Run, command)
	except:
		lytic_crashlog(Thread_Run, command)

def execute_handler(handler_instance, list = (), command = None):
	try:
		handler_instance(*list)
	except (KeyboardInterrupt, SystemExit):
		pass
	except:
		lytic_crashlog(handler_instance, command)

def get_Thr_id(handler):
	INFO['thr'] += 1
	return '%s-%d' % (handler.func_name, INFO['thr'])

def call_message_handlers(stanza, typ, source, body):
	for handler in MESSAGE_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (stanza, typ, source, body,),))
			Thread_Run(Thr, handler)

def call_outgoing_message_handlers(target, body, obody):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (target, body, obody,),))
			Thread_Run(Thr, handler)

def call_join_handlers(conf, nick, afl, role):
	for handler in JOIN_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (conf, nick, afl, role,),))
			Thread_Run(Thr, handler)

def call_leave_handlers(conf, nick, reason, code):
	for handler in LEAVE_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (conf, nick, reason, code,),))
			Thread_Run(Thr, handler)

def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (iq,),))
			Thread_Run(Thr, handler)

def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		with smph:
			Thr = threading.Thread(None, execute_handler, get_Thr_id(handler), (handler, (prs,),))
			Thread_Run(Thr, handler)

def call_stage_init(num, conf = None):
	for handler in eval("STAGE%d_INIT" % num):
		if conf:
			execute_handler(handler, (conf,))
		else:
			execute_handler(handler)

def call_command_handlers(command, typ, source, body, callee):
	real_access = MACROS.get_access(callee, source[1])
	if real_access <= 0:
		real_access = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source[0], real_access, source[1]):
			handler = COMMAND_HANDLERS[command]
			with smph:
				Thr = threading.Thread(target = execute_handler, args = (handler, (typ, source, body), command,))
				Thread_Run(Thr, handler)
			COMMSTAT[command]['col'] += 1
			jid = handler_jid(source[0])
			if jid not in COMMSTAT[command]['users']:
				COMMSTAT[command]['users'].append(jid)
		else:
			reply(typ, source, u'недостаточный доступ.')

## Plugins loader.
def load_plugins():
	Print('\n\nLOADING PLUGINS:', color4)
	ltc, tal, Npl = [], [], []
	for Plugin in os.listdir(PLUGIN_DIR):
		if Plugin.endswith('.py'):
			filename = '%s/%s' % (PLUGIN_DIR, Plugin)
			try:
				data = file(filename).read(20)
			except:
				data = str()
			Plug = Plugin.split('.')
			if data.count("# BS mark.1"):
				try:
					execfile(filename, globals()); ltc.append(Plug[0])
				except:
					print_exc()
					Npl.append(Plug[0])
			elif data.count('talis'):
				try:
					execfile(filename, globals()); tal.append(Plug[0])
				except:
					print_exc()
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
	del tal, ltc, Npl

## Other.
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
		if BOT_OS == "posix":
			pipe = os.popen(command.encode("utf8"))
			out = pipe.read()
		elif BOT_OS == "nt":
			pipe = os.popen("%s" % command.encode("cp1251"))
			out = pipe.read().decode("cp866")
		pipe.close()
	except:
		out = returnExc()
	return out

def returnExc():
	exc = sys.exc_info()
	if any(exc):
		error = "\n%s: %s " % (exc[0].__name__, exc[1])
	else:
		error = `None`
	return error

read_link = lambda link: urlopen(link).read()

def read_url(link, Browser = False):
	from urllib2 import Request
	req = Request(link)
	if Browser:
		req.add_header('User-agent', Browser)
	site = urlopen(req)
	data = site.read()
	del Request
	return data

def re_search(body, s0, s2, s1 = "(?:.|\s)+"):
	comp = re.compile("%s(%s?)%s" % (s0, s1, s2), 16)
	body = comp.search(body)
	if body:
		body = (body.group(1)).strip()
	else:
		raise KeyError
	return body

def handler_botnick(conf):
	if conf in BOT_NICKS:
		return BOT_NICKS[conf]
	return DEFAULT_NICK

def handler_jid(instance):
	instance = unicode(instance)
	List = instance.split('/', 1)
	chat = List[0].lower()
	if (len(List) == 2) and GROUPCHATS.has_key(chat):
		if GROUPCHATS[chat].has_key(List[1]):
			return GROUPCHATS[chat][List[1]]['jid']
	return chat

def save_conflist(conf, nick = None, code = None):
	if initialize_file(GROUPCHATS_FILE):
		try:
			list = eval(read_file(GROUPCHATS_FILE))
		except:
			list = {}
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
	PID, memory = `BOT_PID`, `0`
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
		return int(number)
	except:
		return False

def replace_all(retxt, list, data = False):
	for x in list:
		retxt = retxt.replace(x, data if data != False else list[x])
	return retxt

def that_day():
	return int(time.strftime('%Y%m%d', time.gmtime()))

Elist = [' %s' % (x) for x in [u'0 мес', u'0 дн', u'0 час', u'0 мин', u'0 сек']]

def formatWord(Numb, ls):
	ls = "{2}/{0}/{1}/{1}/{1}/{2}/{2}/{2}/{2}/{2}/{2}/{2}/{2}/{2}".format(*ls)
	ls = ls.split(chr(47))
	if Numb in xrange(15):
		x = ls[Numb]
	else:
		x = ls[int(str(Numb)[-1])]
	return x

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
	while True:
		sys.exc_clear()
		gc.collect()
		try_sleep(60)
		if MEMORY_LIMIT and memory_usage() >= MEMORY_LIMIT:
			sys_exit('memory leak')

## Access handlers.
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

## MUC & Roster handlers.
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
	call_stage_init(1, conf)
	if conf not in GROUPCHATS:
		GROUPCHATS[conf] = {}
	if conf not in STATUS:
		STATUS[conf] = {'message': 'BlackSmith, XMPP BOT, is ready to work.', 'status': 'chat'}
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
		text = u'[%d/%s] %s[...]' % (col, all, body[:PRIV_MSG_LIMIT])
		JCON.send(xmpp.Message(target, text.strip(), ltype))
		body = body[PRIV_MSG_LIMIT:]
		time.sleep(2)
	return u'[%d/%s] %s' % ((col + 1), all, body)

def delivery(body):
	if not isinstance(body, unicode):
		body = body.decode('utf-8', 'replace')
	INFA['outmsg'] += 1
	if not INFO.get("creporter"): return
	try:
		JCON.send(xmpp.Message(BOSS, body, 'chat'))
	except:
		write_file('delivery.txt', body, 'a')

## We are so sorry for blocking arabic.
from unicodedata import name as uName
def detectSymbols(symbol):
#	print u"%s: %s, %s, %s" % (uName(unicode(symbol)), symbol, str(ord(symbol)), str(symbol.isalpha()))
	if symbol in [chr(9), chr(10), chr(13)]:
		return False
	try:
		name = uName(unicode(symbol))
		return name.count("ARABIC") or name.count("WIDTH NO-BREAK")
	except:
#		print "'%s'" % symbol
		return True

def checkArabic(text):
	arabic = False
	for x in text:
		if detectSymbols(x):
			arabic = True
			break
	return arabic

def replaceArabic(text):
	for x in text:
		if detectSymbols(x):
			text = text.replace(x, u"*")
	return u"%s\n\n*** Text contains unavailable symbols." % text

def msg(target, body):
	if not isinstance(body, unicode):
		body = body.decode('utf-8', 'replace')
	obody = body
	jid = str(target).split("/")[0]
	if jid.endswith("xmpp.ru") or jid.endswith("jabber.ru"):
		if checkArabic(body):
			body = replaceArabic(body)
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
	Presence = xmpp.Presence(None, 'unavailable')
	Presence.setStatus(status)
	JCON.send(Presence)

def change_bot_status(conf, text, status):
	Presence = xmpp.protocol.Presence('%s/%s' % (conf, handler_botnick(conf)))
	Presence.setStatus(text)
	Presence.setShow(status)
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	JCON.send(Presence)

def handler_iq_send(conf, item_name, item, afrls, afrl, rsn = None):
	stanza = xmpp.Iq(to = conf, typ = 'set')
	INFA['outiq'] += 1
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

def roster_check(instance, body):
	if instance not in ANSWER:
		QA = random.choice(QUESTIONS.keys())
		ANSWER[instance] = {'key': QUESTIONS[QA]['answer'], 'tryes': 0}
		msg(instance, u'Привет! Мне нужно убедиться, что ты не бот: %s. У тебя три попытки и 1 минута!' % (QUESTIONS[QA]['question']))
		INFO['thr'] += 1
		try:
			threading.Timer(60, roster_timer,(instance,)).start()
		except:
			pass
	elif ANSWER[instance]['tryes'] >= 3:
		roster_ban(instance)
	elif ANSWER[instance]['key'] == body.lower():
		RSTR['AUTH'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Правильно!')
		JCON.Roster.Authorize(instance)
		JCON.Roster.Subscribe(instance)
		JCON.Roster.setItem(instance, instance, ['USERS'])
		del ANSWER[instance]
		delivery(u'Контакт %s прошел IQ проверку и был добавлен в группу "USERS"!' % (instance))
	else:
		ANSWER[instance]['tryes'] += 1
		msg(instance, u'Включи мозг! Неправильно!')

def roster_ban(instance):
	if not instance.count('@conf'):
		RSTR['BAN'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Поздравляю, ты в бане!')
		JCON.Roster.Unsubscribe(instance)
		if instance in JCON.Roster.getItems():
			JCON.Roster.delItem(instance)
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
		pass

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
	instance = fromjid.getStripped().lower()
	if user_level(fromjid, instance) <= -100:
		return
	if instance in UNAVALABLE and not MSERVE:
		return
	if stanza.timestamp:
		return
	bot_nick, nick = handler_botnick(instance), fromjid.getResource()
	if bot_nick == nick:
		return
	body = stanza.getBody() or ""
	if body:
		body = body.strip()
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
		pass
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
			if not COMMANDS.has_key(command) and command[:1] in ["!", "@", "#", ".", "*", "?", "`"]:
				command = command[1:]
		else:
			command = command_Prefix(instance, command)
	if instance in COMMOFF and command in COMMOFF[instance]:
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

def status_code_change(items, conf, nick):
	for item in items:
		try:
			del GROUPCHATS[conf][nick][item]
		except:
			pass

def error_join_timer(conf):
	if conf in GROUPCHATS:
		send_join_presece(conf, handler_botnick(conf))

def roster_subscribe(jid):
	if jid in ADLIST:
		JCON.Roster.Authorize(jid)
		JCON.Roster.Subscribe(jid)
		JCON.Roster.setItem(jid, jid, ['ADMINS'])
	elif RSTR['VN'] == 'off':
		JCON.Roster.Unauthorize(jid)
		if jid in JCON.Roster.getItems():
			JCON.Roster.delItem(jid)
	elif not RSTR['BAN'].get(jid) and RSTR['VN'] in ['iq', 'on']:
		JCON.Roster.Authorize(jid)
		JCON.Roster.Subscribe(jid)
		JCON.Roster.setItem(jid, jid, ['USERS'])

def PRESENCE_PROCESSING(client, Prs):
	fromjid = Prs.getFrom()
	INFO['prs'] += 1
	conf = fromjid.getStripped().lower()
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
			if scode in ['301', '307'] and nick == handler_botnick(conf):
				leave_groupchat(conf, u'Got %s code!' % str(scode))
				text = (u'забанили' if scode == '301' else u'кикнули')
				delivery(u'Меня %s в "%s" и я оттуда вышел.' % (text, conf))
				return
			elif scode == '303':
				full_jid = Prs.getJid()
				if not full_jid:
					full_jid = unicode(fromjid)
					jid = unicode(fromjid)
				else:
					full_jid = unicode(full_jid)
					jid = full_jid.split('/')[0].lower()
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
					jid = full_jid = unicode(fromjid)
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
					jid = full_jid.split("/", 1)[0].lower()
				else:
					if nick == handler_botnick(conf) and Prs.getAffiliation() in ['admin','owner']:
						UNAVALABLE.remove(conf)
						msg(conf, u'Походу дали админа, перезахожу!')
						time.sleep(2)
						leave_groupchat(conf, 'Rejoin...')
						time.sleep(2)
						join_groupchat(conf, handler_botnick(conf))
					return
			else:
				full_jid = unicode(full_jid)
				jid = full_jid.split("/", 1)[0].lower()
			if nick in GROUPCHATS[conf] and GROUPCHATS[conf][nick]['jid'] == jid and GROUPCHATS[conf][nick]['ishere']:
				pass
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
				elif ecode in ['401', '403', '405']:
					leave_groupchat(conf, u'Got %s error code!' % str(ecode))
					delivery(u'Ошибка %s, пришлось выйти из -> "%s"' % (ecode, conf))
				elif ecode in ['404', '503']:
					try:
						ThrName = "rejoin-%s" % (conf.decode("utf-8"))
						if ThrName not in [x._Thread__name for x in threading._active.values()]:
							Thr = threading.Timer(360, error_join_timer, (conf,))
							Thr.name(ThrName)
							Thr.start()
					except:
						pass
		if GROUPCHATS.has_key(conf):
			call_presence_handlers(Prs)

def IQ_PROCESSING(client, iq):
	INFO["iq"] += 1
	fromjid = iq.getFrom()
	if user_level(fromjid, fromjid.getStripped().lower()) <= -100:
		return
	if iq.getType() == "get":
		nsType = iq.getQueryNS()
		result = iq.buildReply("result")
		query = result.getTag("query")
		if nsType == xmpp.NS_VERSION:
			query.setTagData("name", "BlackSmith mark.1")
			query.setTagData("version", "%d (r.%d)" % (CORE_MODE, BOT_REV))
			query.setTagData("os", os_name)
		elif nsType == xmpp.NS_URN_TIME:
			tzo = (lambda tup: tup[0]+"%02d:" % tup[1]+"%02d" % tup[2])((lambda t: tuple(['+' if t < 0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
			utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
			repl = result.addChild('time', {}, [], 'urn:xmpp:time')
			repl.setTagData('tzo', tzo)
			repl.setTagData('utc', utc)
		elif nsType == xmpp.NS_DISCO_INFO:
			ids = [{'category': 'client', 'type': 'bot', 'name': 'BlackSmith'}]
			features = [xmpp.NS_DISCO_INFO, xmpp.NS_DISCO_ITEMS, xmpp.NS_MUC, xmpp.NS_URN_TIME, xmpp.NS_PING, xmpp.NS_VERSION, xmpp.NS_ROSTER, xmpp.NS_VCARD, xmpp.NS_DATA, xmpp.NS_LAST, xmpp.NS_TIME]
			info = {'ids': ids, 'features': features}
			pybr = xmpp.browser.Browser()
			pybr.PlugIn(JCON)
			pybr.setDiscoHandler({'items': [], 'info': info})
		elif nsType == xmpp.NS_LAST:
			last = time.time() - LAST['time']
			query.setAttr('seconds', int(last))
			query.setData(LAST['cmd'])
		elif nsType == xmpp.NS_TIME:
			LocTime = time.strftime("%a, %d %b %Y %H:%M:%S")
			GMTime = time.strftime("%Y%m%dT%H:%M:%S (GMT)", time.gmtime())
			tz = time.strftime("%Z")
			if BOT_OS == "nt":
				tz = tz.decode("cp1251")
			query.setTagData("utc", GMTime)
			query.setTagData("tz", tz)
			query.setTagData("display", LocTime)
		client.send(result)
		raise xmpp.NodeProcessed
	call_iq_handlers(iq)

## actions start.
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
		Print('\n\nDISCONNECTED', color2)
		call_stage_init(3)
		Exit('\n\nRESTARTING...', 0, 30)
	try:
		threading.Timer(3, col_minus).start()
	except:
		pass

def Dispatch_handler(Timeout = 8):
	try:
		JCON.Process(Timeout)
	except xmpp.Conflict:
		Print('\n\nError: XMPP Conflict!', color2)
		call_stage_init(3)
		os._exit(0)
	except xmpp.StreamError:
		pass
	except xmpp.simplexml.xml.parsers.expat.ExpatError:
		pass
	except KeyboardInterrupt:
		sys_exit('Interrupt (Ctrl+C)')

def sys_exit(exit_reason = 'SUICIDE'):
	Print('\n\n%s' % (exit_reason), color2)
	if JCON.isConnected():
		send_unavailable(exit_reason)
	if (time.time() - INFO['start']) >= 30:
		call_stage_init(3)
	Exit('\n\nRESTARTING...\n\nPress Ctrl+C to exit', 0, 30)

## Main.
def main():
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
			CACHE['REST'].append(time.strftime('%d.%m.%Y (%H:%M:%S)'))
	else:
		CACHE = {'PID': BOT_PID, 'START': time.time(), 'REST': []}
	Print('\nBot`s PID: %d' % (BOT_PID), color4)
	write_file(PID_FILE, str(CACHE))
	globals()['RUNTIMES'] = {'START': CACHE['START'], 'REST': CACHE['REST']}
	globals()['JCON'] = xmpp.Client(HOST, PORT, [])
	starting_actions()
	Print('\n\nConnecting...', color4)
	if SECURE:
		CONNECT = JCON.connect((SERVER, PORT), None, None, False)
	else:
		CONNECT = JCON.connect((SERVER, PORT), None, False, True)
	if CONNECT:
		if SECURE and CONNECT != 'tls':
			Print('\nWarning: unable to estabilish secure connection - TLS failed!', color2)
		else:
			Print('\nConnection is OK', color3)
		Print('Using: %s' % str(JCON.isConnected()), color4)
	else:
		Exit("\nCan't Connect.\nSleep for 30 seconds", 0, 30)
	Print('\nAuthentication plese wait...', color4)
	AUTHENT = JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if AUTHENT:
		if AUTHENT != 'sasl':
			Print('\nWarning: unable to perform SASL auth. Old authentication method used!', color2)
		else:
			Print('Auth is OK', color3)
	else:
		Exit('\nAuth Error: %s %s\nMaybe, incorrect jid or password?' % (`JCON.lastErr`, `JCON.lastErrCode`), 0, 12)
	call_stage_init(0)
	JCON.sendInitPresence()
	JCON.RegisterHandler('message', MESSAGE_PROCESSING)
	JCON.RegisterHandler('presence', PRESENCE_PROCESSING)
	JCON.RegisterHandler('iq', IQ_PROCESSING)
	JCON.RegisterDisconnectHandler(lytic_restart)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	Print('\n\nYahoo! I am online!', color3)
	if initialize_file(GROUPCHATS_FILE):
		try:
			CONFS = eval(read_file(GROUPCHATS_FILE))
		except:
			CONFS = {}
			lytic_crashlog(read_file)
			Print("\nChatrooms file corrupted! Load failed.", color2)
		if len(CONFS): 
			Print('\n\nThere are %d rooms in list:' % len(CONFS), color4)
			for conf in CONFS:
				BOT_NICKS[conf] = CONFS[conf]['nick']
				try:
					muc = join_groupchat(conf, handler_botnick(conf), CONFS[conf]['code'])
					Print(u"Joined in %(conf)s" % vars(), color3)
				except:
					Print(u"Failed join in %(conf)s" % vars(), color2)
	else:
		Print('\n\nError: unable to create chatrooms list file!', color2)
	Print('\n\nBlackSmith is ready to work!\n\n', color3)
	INFO['start'] = time.time()
	call_stage_init(2)
	Timeout = ((len(GROUPCHATS.keys())+1) / 6) + 1
	while True:
		try:
			Dispatch_handler(Timeout)
		except Exception:
			Dispatch_fail()
			INFO['errs'] += 1
			if INFO['errs'] >= 7:
				sys_exit('Fatal exception: %s' % returnExc())
				break

if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			sys_exit('Interrupt (Ctrl+C)')
		except xmpp.HostUnknown:
			Print('\n\nError: host unknown!', color2)
		except:
			lytic_crashlog(main)
		try_sleep(5)

## That is all...