# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  logger.py

# © 2011 simpleApps (http://simpleapps.ru)
# Thanks to: WitcherGeralt (WitcherGeralt@jabber.ru)

logConfigFile = "dynamic/logstate.txt"
logCacheFile = "logcache.txt"

LoggerCfg = {"theme": "LunnaCat", "enabled": False, "dir": "logs"}
logThemes = {}

Months, Days = (u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь"), (u"Понедельник", u"Вторник", u"Среда", u"Четверг", u"Пятница", u"Суббота", u"Воскресенье", u"Понедельник")

logAfl = {
	"none": u"посетитель",
	"member": u"зарегестрированный пользователь",
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
<h3><div class="shadowed">%(chat)s<hr></div></h3>
<div>
<tt>'''

def getLogFile(chat, Time):
	logDir = chkFile("%s/%s/%d/%d" % (LoggerCfg["dir"], chat, Time.tm_year, Time.tm_mon))
	if not os.path.isdir(logDir):
		try:
			os.makedirs(logDir)
		except:
			return False
	logFileName = "%s/%d.html" % (logDir, Time.tm_mday)
	if os.path.isfile(logFileName):
		logFile = open(logFileName, "a")
		INFA["fw"] += 1
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
		INFA["fcr"] += 1
		logFile.write(pattern % vars())
	return logFile

def logWrite(chat, state, body, nick = None):
	Time = time.gmtime()
	with logSynchronize[chat]:
		logFile = getLogFile(chat, Time)
		if logFile:
			timestamp = time.strftime("%H:%M:%S", Time)
			body = xmpp.XMLescape(body)
			body = re.sub("(https|http|ftp|svn)(\:\/\/[^\s<]+)", lambda obj: "<a href=\"{0}\">{0}</a>".format(obj.group(0)), body)
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
				logFile.write('<span class="{0}"><a id="t{1}" href="#t{1}">[{1}]</a></span>&nbsp;'.format(nick or state, timestamp))
				logFile.write('<span class="%s">%s</span><br />' % (nick or state, body))
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
		logWrite(source[1], ("subject" if stanza.getSubject() else "msg"), body, source[2])

def logWriteJoined(chat, nick, afl, role, status, text):
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		afl, role, status = logAfl.get(afl, ""), logRole.get(role, ""), logStatus.get(status, "")
		log = u"*** %(nick)s заходит как %(role)s и %(afl)s и теперь %(status)s"
		if text:
			log += " (%(text)s)"
		logWrite(chat, "join", log % vars())

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

def logWritePresence(Prs):
	fromjid = Prs.getFrom()
	chat = fromjid.getStripped()
	if GROUPCHATS.has_key(chat) and logCfg[chat]["enabled"]:
		nick = fromjid.getResource()
		pType = Prs.getType()
		if pType == 'unavailable':
			scode = Prs.getStatusCode()
			if scode == '303':
				logWrite(chat, "nick", u'*** %s меняет ник на %s' % (nick, Prs.getNick()))
		else:
			afl = logAfl.get(Prs.getAffiliation(), "")
			role = logRole.get(Prs.getRole(), "")
			status = logStatus.get(Prs.getShow(), "")
			reason = Prs.getReason()
			priority = Prs.getPriority()
			text = Prs.getStatus()
			log = u"*** %(nick)s (%(afl)s, %(role)s) теперь %(status)s"
			if text:
				log += " (%(text)s)"
			if priority:
				log += " [%s]" % priority
			if reason:
				log += " (Причина: %(reason)s)"
			logWrite(chat, ("role" if reason else "status"), log % vars())

def logFileInit(chat):
	cfg = {"theme": LoggerCfg["theme"], "enabled": False, "file": ""}
	if check_file(chat, logCacheFile, str(cfg)):
		cfg = eval(read_file("dynamic/%s/%s" % (chat, logCacheFile)))
	else:
		delivery(u"Внимание! Не удалось создать файл \"%s\"!" % (chat, logCacheFile))
	logCfg[chat] = cfg
	logNicks[chat] = {}
	logSynchronize[chat] = threading.Semaphore()
	if not os.path.isdir(chkFile("%s/%s/.theme" % (LoggerCfg["dir"], chat))) and logThemes.has_key(cfg["theme"]):
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
			register_stage1_init(logFileInit)
			register_join_handler(logWriteJoined)
			register_leave_handler(logWriteLeave)
			register_message_handler(logWriteMessage)
			register_presence_handler(logWritePresence)
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
				register_stage1_init(logFileInit)
				for conf in GROUPCHATS.keys():
					execute_handler(logFileInit, (conf,))
				register_join_handler(logWriteJoined)
				register_leave_handler(logWriteLeave)
				register_message_handler(logWriteMessage)
				register_presence_handler(logWritePresence)
				command_handler(logSetState, 30, "logger")
				reply(mType, source, u"Включил логгер.")
			else:
				reply(mType, source, u"Уже включено.")
		elif a0 in ("0", u"выкл"):
			if LoggerCfg["enabled"]:
				LoggerCfg["enabled"] = False
				write_file(logConfigFile, str(LoggerCfg))
				name = logWriteMessage.func_name
				for handler in MESSAGE_HANDLERS:
					if name == handler.func_name:
						MESSAGE_HANDLERS.remove(handler)
				name = logWritePresence.func_name
				for handler in PRESENCE_HANDLERS:
					if name == handler.func_name:
						PRESENCE_HANDLERS.remove(handler)
				name = logWriteJoined.func_name
				for handler in JOIN_HANDLERS:
					if name == handler.func_name:
						JOIN_HANDLERS.remove(handler)
				name = logWriteLeave.func_name
				for handler in LEAVE_HANDLERS:
					if name == handler.func_name:
						LEAVE_HANDLERS.remove(handler)
				name = logFileInit.func_name
				try:
					command = eval(read_file("help/logger").decode('utf-8'))[logSetState.func_name]["cmd"]
				except:
					delivery(u"Внимание! Не удалось загрузить файл помощи логгера.")
				else:
					del COMMAND_HANDLERS[command]
				for handler in STAGE1_INIT:
					if name == handler.func_name:
						STAGE1_INIT.remove(handler)
				logCfg.clear()
				logSynchronize.clear()
				reply(mType, source, u"Выключил логгер.")
			else:
 				reply(mType, source, u"Логгер вообще не включён.")
		else:
			reply(mType, source, u"Что-то не то...")
	elif LoggerCfg["enabled"]:
		reply(mType, source, u"Сейчас логгер включён.")
	else:
		reply(mType, source, u"Сейчас логгер выключен.")

def logSetState(mType, source, argv):
	if GROUPCHATS.has_key(source[1]):
		if argv:
			argv = argv.split()
			chat = source[1]
			a0 = (argv.pop(0)).lower()
			if a0 in ("1", u"вкл"):
				if not logCfg[source[1]]["enabled"]:
					logCfg[source[1]]["enabled"] = True
					write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
					reply(mType, source, u"Включил логирование «%s»." % source[1])
				else:
					reply(mType, source, u"Уже включено.")
			elif a0 in ("0", u"выкл"):
				if logCfg[source[1]]["enabled"]:
					logCfg[source[1]]["enabled"] = False
					write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
					reply(mType, source, u"Выключил логирование «%s»." % chat)
				else:
					reply(mType, source, u"«%s» не логируется.")
			elif a0 in (u"тема", "темы"):
				if argv:
					if logThemes.has_key(argv[1]):
						themeFile = chkFile("%s/%s/.theme/name.txt" % (LoggerCfg["dir"], chat))
						if os.path.isfile(themeFile) and argv[1] == read_file(themeFile):
							reply(mType, source, u"Тема «%s» уже используется плагином." % argv[1])
						else:
							logCfg[source[1]]["theme"] = argv[1]
							write_file("dynamic/%s/%s" % (chat, logCacheFile), str(logCfg[chat]))
							logThemeCopier(source[1], argv[1])
							reply(mType, source, u"Установил тему «%s». Она вступит в силу немедленно." % argv[1])
					else:
						reply(mType, source, u"Нет такой темы :(")
				else:
					ls = []
					for Numb, Theme in enumerate(logThemes.keys()):
						ls.append("%d. %s." % ((Numb + 1), Theme))
					reply(mType, source, str.join(chr(10), ls))
			else:
				reply(mType, source, u"пшел вон")
		elif logCfg[source[1]]["enabled"]:
			reply(mType, source, u"Сейчас логгер включён. Тема, используемая плагином в текущей конференции, называется «%s»." % logCfg[source[1]]["theme"])
		else:
			reply(mType, source, u"Сейчас комната не логируется.")

register_stage0_init(init_logger)
command_handler(logSetStateMain, 100, "logger")
