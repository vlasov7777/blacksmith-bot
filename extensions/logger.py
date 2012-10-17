# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  logger.py

# © 2011-2012 simpleApps (http://simpleapps.ru)
# Thanks to: WitcherGeralt (alkorgun@gmail.com)

logConfigFile = "dynamic/logstate.txt"
logCacheFile = "logcache.txt"

logThemes = {}

Months, Days = ("", u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь"), (u"Понедельник", u"Вторник", u"Среда", u"Четверг", u"Пятница", u"Суббота", u"Воскресенье", u"Понедельник")

logAfl = {
	"none": u"посетитель",
	"member": u"зарегистрированный пользователь",
	"admin": u"администратор",
	"owner": u"владелец"
			}

logRole = {
	"visitor": u"гость",
	"moderator": u"модератор",
	"participant": u"участник"
			}

logStatus = {
	None: u"доступен",
	"xa": u"недоступен",
	"dnd": u"не беспокоить",
	"away": u"отсутствую",
	"chat": u"готов поболтать"
			}

logCfg = {}
logNicks = {}
logSynchronize = {}

DefaultLogHeader = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
<head>
<title>%(date)s — %(chat)s</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<link type="text/css" rel="StyleSheet" href="../../.theme/logger.css" />
</head>

<body>
<div class="shadowed" align="right"><a href="http://simpleapps.ru/">BlackSmith Bot log file</a></div>
<div class="shadowed" align="center"><a href="xmpp:%(chat)s?join" title="Join to %(chat)s">%(chat)s</a><hr></div></hr>
<h3><div class="shadowed">%(date)s<hr></div></h3>
<div>
<tt>'''

LoggerCfg = {"theme": "LunnaCat", "enabled": False, "timetype": "local", "dir": "logs"}

Subjs = {}

def getLogFile(chat, Time):
	mon = str(Time.tm_mon) if (Time.tm_mon > 9) else ("0%d" % Time.tm_mon)
	logDir = chkFile("%s/%s/%d/%s" % (LoggerCfg["dir"], chat, Time.tm_year, mon))
	if not os.path.isdir(logDir):
		try:
			os.makedirs(logDir)
		except:
			return False
	prev, next = (Time.tm_mday - 1, Time.tm_mday  + 1)
	if prev <= 9:
		prev = "0%d" % prev
	if next <= 9:
		next = "0%d" % next
	day = str(Time.tm_mday) if (Time.tm_mday > 9) else ("0%d" % Time.tm_mday)
	logFileName = "%s/%s.html" % (logDir, day)
	if os.path.isfile(logFileName):
		logFile = open(logFileName, "a")
		INFO["fw"] += 1
	else:
		date = time.strftime("{0}, {1} %d, %Y".format(Days[Time.tm_wday], Months[Time.tm_mon]), Time)
		themeFile = chkFile("%s/%s/.theme/pattern.html" % (LoggerCfg["dir"], chat))
		if os.path.isfile(themeFile):
			pattern = read_file(themeFile)
		else:
			pattern = DefaultLogHeader
		exfile = logCfg[chat]["file"]
		if logFileName != exfile:
			if exfile and os.path.isfile(exfile):
				 write_file(exfile, "\n</tt>\n</div>\n</body>\n</html>", "a")
			logCfg[chat]["file"] = logFileName
		logFile = open(logFileName, "w")
		INFO["fcr"] += 1
		logFile.write(pattern % vars())
		if Subjs[chat]['time'] and Subjs[chat]['body']:
			Time = time.time()
			if (Time - Subjs[chat]['time']) > 20:
				Subjs[chat]['time'] = Time
				logFile.write('<span class="topic">%s</span><br>' % Subjs[chat]['body'].replace("\n", "<br>"))
	return logFile

def logWrite(chat, state, body, nick = None):
	if LoggerCfg["timetype"].lower() == "gmt": 
		Time = time.gmtime()
	elif LoggerCfg["timetype"].lower() == "local":
		Time = time.localtime()
	with logSynchronize[chat]:
		logFile = getLogFile(chat, Time)
		if logFile:
			timestamp = time.strftime("%H:%M:%S", Time)
			body = xmpp.XMLescape(body)
			body = re.sub(r"(www\.(?!\.)|[a-z][a-z0-9+.-]*://)[^\s<>'\"]+[^!,\.\s<>\)'\"\]]", lambda obj: "<a href=\"{0}\">{0}</a>".format(obj.group(0)), body) #'
			body = body.replace(chr(10), "<br/>")
			logFile.write(chr(10))
			if state == "subject":
				logFile.write('<span class="topic">%s</span><br />' % body)
			elif state == "msg":
				if nick:
					nickColor = "nick%d" % coloredNick(chat, nick)
					if body.startswith("/me"):
						logFile.write('<span class="{0}"><a id="t{1}" href="#t{1}">[{1}]</a>&nbsp;*{2}&nbsp;{3}</span><br />'.format(nickColor, timestamp, nick, body[3:]))
					else:
						logFile.write('<span class="{0}"><a id="t{1}" href="#t{1}">[{1}]</a>&nbsp;&lt;{2}&gt;</span>&nbsp;<span class="text">{3}</span><br />'.format(nickColor, timestamp, nick, body))
				else:
					logFile.write('<span class="status"><a id="t{0}" href="#t{0}">[{0}]</a></span>&nbsp;'.format(timestamp))
					logFile.write('<span class="status">*** %s</span><br />' % (body))
			else:
				logFile.write('<span class="{0}"><a id="t{1}" href="#t{1}">[{1}]</a></span>&nbsp;'.format(state, timestamp))
				logFile.write('<span class="%s">%s</span><br />' % (state, body))
			logFile.close()

def coloredNick(chat, nick):
	if logNicks[chat].has_key(nick):
		return logNicks[chat][nick]
	if len(logNicks[chat]) < 20:
		ls = range(1, 21)
		for x in logNicks[chat].values():
			ls.remove(x)
		logNicks[chat][nick] = x = random.choice(ls)
	else:
		logNicks[chat][nick] = x = random.randrange(1, 21)
	return x

def logWriteMessage(stanza, mType, source, body):
	if GROUPCHATS.has_key(source[1]) and mType == "public" and logCfg[source[1]]["enabled"]:
		if stanza.getSubject():
			Time = time.time()
			if (Time - Subjs[source[1]]['time']) > 20:
				Subjs[source[1]] = {'body': body, 'time': Time}
				logWrite(source[1], "subject", body)
		else:
			logWrite(source[1], "msg", body, source[2])

def logWriteJoined(chat, nick, afl, role, status, text):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		log = u"*** %(nick)s заходит как %(role)s"
		if afl != "none":
			log += u" и %(afl)s"
		log += u" и теперь %(status)s"
		afl, role, status = logAfl.get(afl, ""), logRole.get(role, ""), logStatus.get(status, "")
		if text:
			log += " (%(text)s)"
		logWrite(chat, "join", log % vars())

def logWriteARole(chat, nick, aRole, reason):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		role, afl = aRole
		log = u"*** %(nick)s теперь %(role)s"
		if afl != "none":
			log += u" и %(afl)s"
		if reason:
			log += u" (%(reason)s)"
		afl, role = logAfl.get(afl, ""), logRole.get(role, "")
		logWrite(chat, "role", log % vars())

def logWriteNickChange(stanza, chat, oldNick, nick):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		logWrite(chat, "nick", u'*** %s меняет ник на %s' % (oldNick, nick))
		
def logWriteStatusChange(chat, nick, status, priority, text):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		log = u"*** %(nick)s теперь %(status)s"
		if text:
			log += " (%(text)s)"
		if priority:
			log += " [%s]" % priority
		status = logStatus.get(status, "")
		logWrite(chat, "status", log % vars())		

def logWriteLeave(chat, nick, reason, code):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		if code:
			if code == "307":
				if reason:
					logWrite(chat, "kick", u"*** %s выгнали из конференции (%s)" % (nick, reason))
				else:
					logWrite(chat, "kick", u"*** %s выгнали из конференции" % nick)
			elif code == "301":
				if reason:
					logWrite(chat, "ban", u"*** %s запретили входить в данную конференцию (%s)" % (nick, reason))
				else:
					logWrite(chat, "ban", u"*** %s запретили входить в данную конференцию" % nick)
		elif reason:
			logWrite(chat, "leave", u"*** %s выходит из конференции (%s)" % (nick, reason))
		else:
			logWrite(chat, "leave", u"*** %s выходит из конференции" % nick)

def logFileInit(chat):
	cfg = {"theme": LoggerCfg["theme"], "enabled": False, "file": ""}
	Subjs[chat] = {'body': '', 'time': 0}
	if check_file(chat, logCacheFile, str(cfg)):
		cfg = eval(read_file("dynamic/%s/%s" % (chat, logCacheFile)))
	else:
		delivery(u"Внимание! Не удалось создать файл \"dynamic/%s/%s\"!" % (chat, logCacheFile))
	logCfg[chat] = cfg
	logNicks[chat] = {}
	logSynchronize[chat] = threading.Semaphore()
	if not os.path.isdir(chkFile("%s/%s/.theme" % (LoggerCfg["dir"], chat))) and logThemes.has_key(cfg["theme"]):
		if logCfg[chat]["enabled"]:
			logThemeCopier(chat, cfg["theme"])

def init_logger():
	if initialize_file(logConfigFile, str(LoggerCfg)):
		LoggerCfg.update(eval(read_file(logConfigFile)))
		if LoggerCfg["enabled"]:
			if not os.path.isdir(LoggerCfg["dir"]):
				try:
					os.makedirs(LoggerCfg["dir"])
				except:
					pass
			Dir = "static/logger/themes"
			for Theme in os.listdir(Dir):
				path = "%s/%s" % (Dir, Theme)
				if os.path.isdir(path):
					if "logger.css" in os.listdir(path):
						logThemes[Theme] = path
			handler_register("01si", logFileInit)
			handler_register("04eh", logWriteJoined)
			handler_register("05eh", logWriteLeave)
			handler_register("01eh", logWriteMessage)
			handler_register("07eh", logWriteARole)
			handler_register("06eh", logWriteNickChange)
			handler_register("08eh", logWriteStatusChange)
			command_handler(logSetState, 30, "logger")
	else:
		Print("\nCan't init lostate.txt, logger was disabled.", color2)

def logThemeCopier(chat, theme):
	import shutil
	themeDir = chkFile("%s/%s/.theme" % (LoggerCfg["dir"], chat))
	if os.path.exists(themeDir):
		shutil.rmtree(themeDir)
	shutil.copytree(logThemes[theme], themeDir)
	del shutil

def logSetStateMain(mType, source, argv):
	if argv:
		argv = argv.split()
		a0 = (argv.pop(0)).lower()
		if a0 in ("1", u"вкл"):
			if not LoggerCfg["enabled"]:
				LoggerCfg["enabled"] = True
				write_file(logConfigFile, str(LoggerCfg))
				handler_register("01si", logFileInit)
				for chat in GROUPCHATS.keys():
					execute_handler(logFileInit, (chat,))
				handler_register("04eh", logWriteJoined)
				handler_register("05eh", logWriteLeave)
				handler_register("01eh", logWriteMessage)
				handler_register("07eh", logWriteARole)
				handler_register("06eh", logWriteNickChange)
				handler_register("08eh", logWriteStatusChange)
				command_handler(logSetState, 30, "logger")
				reply(mType, source, u"Включил логгер.")
			else:
				reply(mType, source, u"Уже включено.")
		elif a0 in ("0", u"выкл"):
			if LoggerCfg["enabled"]:
				LoggerCfg["enabled"] = False
				write_file(logConfigFile, str(LoggerCfg))
				name = logWriteMessage.func_name
				for handler in Handlers["01eh"]:
					if name == handler.func_name:
						Handlers["01eh"].remove(handler)
				name = logWriteNickChange.func_name
				for handler in Handlers["06eh"]:
					if name == handler.func_name:
						Handlers["06eh"].remove(handler)
				name = logWriteStatusChange.func_name
				for handler in Handlers["08eh"]:
					if name == handler.func_name:
						Handlers["08eh"].remove(handler)
				name = logWriteARole.func_name
				for handler in Handlers["07eh"]:
					if name == handler.func_name:
						Handlers["07eh"].remove(handler)
				name = logWriteJoined.func_name
				for handler in Handlers["04eh"]:
					if name == handler.func_name:
						Handlers["04eh"].remove(handler)
				name = logWriteLeave.func_name
				for handler in Handlers["05eh"]:
					if name == handler.func_name:
						Handlers["05eh"].remove(handler)
				name = logFileInit.func_name
				try:
					command = eval(read_file("help/logger").decode('utf-8'))[logSetState.func_name]["cmd"]
				except:
					delivery(u"Внимание! Не удалось загрузить файл помощи логгера.")
				else:
					del COMMAND_HANDLERS[command]
				for handler in Handlers["01si"]:
					if name == handler.func_name:
						Handlers["01si"].remove(handler)
				logCfg.clear()
				logSynchronize.clear()
				reply(mType, source, u"Выключил логгер.")
			else:
 				reply(mType, source, u"Логгер вообще не включён.")
		elif a0 in (u"тема", "темы"):
			if argv:
				if logThemes.has_key(argv[0]):
					themeFile = "static/logger/themes/%s/name.txt" % LoggerCfg["theme"]
					if os.path.isfile(themeFile) and argv[0] == read_file(themeFile):
						reply(mType, source, u"Тема «%s» уже используется плагином." % argv[0])
					else:
						LoggerCfg["theme"] = argv[0]
						write_file(logConfigFile, str(LoggerCfg))
						reply(mType, source, u"Установил «%s» стандартной темой." % argv[0])
				else:
					reply(mType, source, u"Нет такой темы :(")
			else:
				ls = []
				for Numb, Theme in enumerate(logThemes.keys()):
					ls.append("%d. %s." % ((Numb + 1), Theme))
				reply(mType, source, str.join(chr(10), ls))
		elif a0 == u"папка":
			if argv:
				LoggerCfg["dir"] = argv[0]
				logThemeCopier(source[1], "LunnaCat")
				write_file(logConfigFile, str(LoggerCfg))
				repl = u"Теперь логи будут храниться в папке «%s»." % argv[0]
			else:
				repl = u"Сейчас логи хрянятся в «%s»." % LoggerCfg["dir"]
			reply(mType, source, repl)
		elif a0 == u"время":
			if argv:
				if argv[0] in ("gmt", "local"):
					LoggerCfg["timetype"] = argv[0]
					write_file(logConfigFile, str(LoggerCfg))
					repl = u"Установил тип записи времени на «%s»." % argv[0]
					logWrite(source[1], "status", u"*** Установлен тип записи времени: %s" % argv[0])				
				else:
					repl = u"Недопустимый тип. Доступные: local, gmt."
			else:
				repl = u"Сейчас установлен тип записи времени «%s»." % LoggerCfg["timetype"]
			reply(mType, source, repl)
		else:
			reply(mType, source, u"Что-то не то...")
	elif LoggerCfg["enabled"]:
		reply(mType, source, u"Сейчас логгер включён.")
	else:
		reply(mType, source, u"Сейчас логгер выключен.")

def logSetState(mType, source, argv):
	if GROUPCHATS.has_key(source[1]):
		chat = source[1]
		if argv:
			argv = argv.split()
			a0 = (argv.pop(0)).lower()
			if a0 in ("1", u"вкл"):
				if not logCfg[chat]["enabled"]:
					logCfg[chat]["enabled"] = True
					write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
					reply(mType, source, u"Включил логирование «%s»." % chat)
				else:
					reply(mType, source, u"Уже включено.")
			elif a0 in ("0", u"выкл"):
				if logCfg[chat]["enabled"]:
					logCfg[chat]["enabled"] = False
					write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
					logWrite(chat, "status", u"*** Логирование конференции приостановлено")
					reply(mType, source, u"Выключил логирование «%s»." % chat)
				else:
					reply(mType, source, u"«%s» не логируется.")
			elif a0 in (u"тема", "темы"):
				if argv:
					if logThemes.has_key(argv[0]):
						themeFile = chkFile("%s/%s/.theme/name.txt" % (LoggerCfg["dir"], chat))
						if os.path.isfile(themeFile) and argv[0] == read_file(themeFile):
							reply(mType, source, u"Тема «%s» уже используется плагином." % argv[0])
						else:
							logCfg[chat]["theme"] = argv[0]
							write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
							logThemeCopier(chat, argv[0])
							repl = u"Установил тему «%s». Она вступит в силу "
							if os.path.exists(chkFile("%s/%s/.theme/pattern.html" % (LoggerCfg["dir"], chat))):
								repl += u"с завтрашнего дня."
							else:
								repl += u"немедленно."
							reply(mType, source, repl % argv[0])
					else:
						reply(mType, source, u"Нет такой темы :(.")
				else:
					repl = str()
					for num, thm in enumerate(logThemes.keys()):
						repl += "%d. %s.\n" % (num + 1, thm)
					reply(mType, source, repl)
			else:
				reply(mType, source, u"Нет такого параметра.")
		elif logCfg[chat]["enabled"]:
			reply(mType, source, u"Сейчас логгер включён. Тема, используемая плагином в текущей конференции, называется «%s»." % logCfg[chat]["theme"])
		else:
			reply(mType, source, u"Сейчас комната не логируется.")

handler_register("00si", init_logger)
command_handler(logSetStateMain, 100, "logger")