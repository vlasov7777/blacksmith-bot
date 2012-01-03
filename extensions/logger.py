# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  logger_plugin.py

# Initial Сopyright © Anaлl Verrier (elghinn@free.fr)
# Modifications Copyright © 2010 - 2011 simpleApps (http://simpleapps.ru)
# Other bots copavility: False. Please, do not try to port it.


logConfigFile = "static/logger/logstate.txt"
logCacheFile = "dynamic/logcache.txt"
logEnabled = False
gLogDir = "logs"

try: execfile(logConfigFile)
except: Print("\n\nError: unable to load logger config!\nPlugin was turned off...", color2)

logFileNames = {}

logConfig = {"theme": LoggerTheme,
				 "chats": []}

Months 	 = {"January":   u"Январь",
	     	    "February":  u"Февраль",
		  	 	 "March": 	   u"Март",
		  		 "April": 	   u"Апрель",
		  		 "May": 		   u"Май",
		  		 "June": 	   u"Июнь",
 		  		 "July": 	   u"Июль",
 		  		 "August":    u"Август",
 		  		 "September": u"Сентябрь",
 		  		 "October":   u"Октябрь",
 		  		 "November":  u"Ноябрь",
		  		 "December":  u"Декабрь"}

Days 		 = {"Monday": 	u"Понедельник",
				"Tuesday": 	u"Вторник",
				"Wednesday":u"Среда",
				"Thursday": u"Четверг",
				"Friday": 	u"Пятница",
				"Saturday": u"Суббота",
				"Sunday": 	u"Воскресенье"}

logAfl 	 = {"none":   u"посетитель",
		    	 "member": u"зарегестрированный пользователь",
		    	 "admin":  u"администратор",
		    	 "owner":  u"владелец"}

logRole 	 =	{"visitor": 	 u"гость",
		    	 "moderator": 	 u"модератор",
		    	 "participant": u"участник"}

logStatus = {None:   u"доступен",
			 	 "xa":   u"недоступен",
		   	 "dnd":  u"не беспокоить",
		 		 "away": u"отсутствую",
		 		 "chat": u"готов поболтать"}

logNicks  = {}
logThemes = {}

def DateTimeReplacer(time):
	for x in Months.keys():
		time = time.replace(x, Months[x])
	for x in Days.keys():
		time = time.replace(x, Days[x])
	return time

def logHeader(logFile, chat, times):
	if not chkUnicode(chat):
		chat = chat.encode("utf-8")
	date = DateTimeReplacer(time.strftime("%A, %B %d, %Y", times))
	if os.path.exists("%s/.theme/pattern.html" % gLogDir):
		pattern = read_file("%s/.theme/pattern.html" % gLogDir)
	else:
		pattern = \
"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
<head>
<title>%(chat)s - %(date)s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link type="text/css" rel="StyleSheet" href="../../../.theme/logger.css" />
</head>
<body>
<div class="shadowed" align="right"><a href="http://simpleapps.ru/">BlackSmith Bot logger file</a></div>
<div class="shadowed" align="center"><a href="xmpp:%(chat)s?join" title="Join to %(chat)s">%(chat)s</a><hr></div></hr>
<h3><div class="shadowed">%(date)s<hr></div></h3>
<div>
<tt>
"""
	logFile.write(pattern % vars())

def logFileWorker(chat, (year, month, day, hour, minute, second, weekday, yearday)):
	logDir = chkFile("/".join([gLogDir, chat, str(year), str(month)]))
	logFileName = "%s/%s.html" % (logDir, day)
	if not os.path.exists(logDir):
		try: os.makedirs(logDir)
		except: return False
	if logFileNames.has_key(chat):
		xfile = logFileNames[chat]
		if xfile != logFileName:
			if os.path.exists(xfile):
				 write_file(xfile, "\n</tt>\n</div>\n</body>\n</html>", "a")
		if os.path.exists(logFileName):
			logFile = open(logFileName, "a")
			return logFile
	else:
		if os.path.exists(logFileName):
			logFileNames[chat] = logFileName
			write_file(logCacheFile, str(logFileNames))
			logFile = open(logFileName, "a")
			return logFile
		else:
			logFileNames[chat] = logFileName
			write_file(logCacheFile, str(logFileNames))
			logFile = open(logFileName, "a")
			INFA['fcr'] += 1
			logHeader(logFile, chat, (year, month, day, hour, minute, second, weekday, yearday, 0))
			return logFile

def regexUrl(matchobj):
	return "<a href=\"%s\">%s</a>" % ((matchobj.group(0),) * 2)

def logWrite(body, nick = 0, chat = 0, source = 0, subject = 0):
	(year, month, day, hour, minute, second, weekday, yearday) = time.localtime()[:8]
	body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	body = re.sub("(https|http|ftp|svn)(\:\/\/[^\s<]+)", regexUrl, body).replace("\n", "<br/>")
	jid = None
	if source:
		chat, nick = source[1:]
		jid = handler_jid(source[0])
	body, nick = body.encode("utf-8"), nick.encode("utf-8")
	timestamp = "%.2i:%.2i:%.2i" % (hour, minute, second)
	logFile = logFileWorker(chat, (year, month, day, hour, minute, second, weekday, yearday))
	if logFile:
		if not nick:
			if subject:
				logFile.write(u'<span class="topic">%s</span><br />\n' % body)
			else:
				logFile.write('<span class="status"><a id="t%s" href="#t%s">[%s]</a></span> ' % (timestamp, timestamp, timestamp))
				logFile.write(u'<span class="status">*** %s</span><br />\n' % (body))
		elif body[:3].lower() == "/me":
			nickColor = "nick%d" % coloredNick(chat, nick)
			logFile.write('<span class="%s"><a id="t%s" href="#t%s">[%s]</a> *%s %s</span><br />\n' % (nickColor, timestamp, timestamp, timestamp, nick, body[3:]))
		elif nick in ("leave", "join", "status", "kick", "ban", "nick", "role"):
			logFile.write('<span class="%s"><a id="t%s" href="#t%s">[%s]</a></span> ' % (nick, timestamp, timestamp, timestamp))
			logFile.write(u'<span class="%s">%s</span><br />\n' % (nick, body))
		else:
			nickColor = "nick%d" % coloredNick(chat, nick)
			logFile.write('<span class="%s"><a id="t%s" href="#t%s">[%s]</a> &lt;%s&gt;</span> <span class="text">%s</span><br />\n' % (nickColor, timestamp, timestamp, timestamp, nick, body))

def coloredNick(chat, nick):
	if not logNicks.get(chat):
		logNicks[chat] = {}
	if logNicks[chat].get(nick):
		return logNicks[chat].get(nick)
	num = random.randrange(1, 21)
	if num not in logNicks[chat].values():
		logNicks[chat][nick] = num
		return num
	elif len(logNicks[chat].keys()) > 19:
		return num
	else:
		coloredNick(chat, nick)

def logWriteMessage(raw, mType, source, body):
###	print raw.getStatusCode() - a new xmpppy feature
	if source[1] in logConfig["chats"] and mType == "public":
		logWrite(body, 0, 0, source, raw.getSubject())

def logWriteJoined(chat, nick, afl, role, status, text):
	if chat in logConfig["chats"]:
		afl, role, status = logAfl.get(afl, ""), logRole.get(role, ""), logStatus.get(status, "")
		log = u"*** %(nick)s заходит как %(role)s и %(afl)s и теперь %(status)s"
		if text:
			log += " (%(text)s)"
		logWrite(log % vars(), "join", chat)

def logWriteLeave(chat, nick, reason, code):
	if chat in logConfig["chats"]:
		if code:
			if code == "307":
				if reason:
					logWrite(u"*** %s выгнали из конференции (%s)" % (nick, reason), "kick", chat)
				else:
					logWrite(u"*** %s выгнали из конференции" % nick, "kick", chat)
			elif code == "301":
				if reason:
					logWrite(u"*** %s запретили входить в данную конференцию (%s)" % (nick, reason), "ban", chat)
				else:
					logWrite(u"*** %s запретили входить в данную конференцию" % nick, "ban", chat)
		else:
			if reason:
				logWrite(u"*** %s выходит из конференции (%s)" % (nick, reason), "leave", chat)
			else:
				logWrite(u"*** %s выходит из конференции" % nick, "leave", chat)

def logWritePresence(Prs):
	fromjid = Prs.getFrom()
	chat = fromjid.getStripped()
	if chat in logConfig["chats"]:
		nick = fromjid.getResource()
		pType = Prs.getType()
		if pType == 'unavailable':
			scode = Prs.getStatusCode()
			if scode == '303':
				logWrite(u'*** %s меняет ник на %s' % (nick, Prs.getNick()), "nick", chat)
				return
		else:
			afl = logAfl.get(Prs.getAffiliation(), "")
			role = logRole.get(Prs.getRole(), "")
			status = logStatus.get(Prs.getShow(), "")
			reason = Prs.getReason()
			text = Prs.getStatus()
			log = u"*** %(nick)s (%(afl)s, %(role)s) теперь %(status)s"
			if text:
				log += " (%(text)s)"
			if reason:
				log += " (Причина: %(reason)s)"
			logWrite(log % vars(), ("role" if reason else "status"), chat)


def logCacheFileInit():
	if initialize_file(logCacheFile):
		try:
			logFileNames = eval(read_file(logCacheFile))
		except Exception:
			write_file(logCacheFile, "{}")
	else:
		Print("\n\nError: can`t create logcache.txt!")

def logFileInit(chat):
	if check_file(None, "logger_cfg.txt", str(logConfig)):
		globals()["logConfig"] = eval(read_file(u"dynamic/logger_cfg.txt"))
	else:
		delivery(u"Внимание! Не удалось создать файл \"logstate.txt\"!" % (chat))

def findThemes():
	for x in os.listdir("static/logger/themes"):
		if os.path.isdir("static/logger/themes/%s" % x):
			if os.listdir("static/logger/themes/%s" % x).count("logger.css"):
				logThemes[x] = "static/logger/themes/%s" % x

def logThemeCopier(theme):
	import shutil
	if os.path.exists(u"%s/.theme" % gLogDir):
		shutil.rmtree(u"%s/.theme" % gLogDir)
	shutil.copytree(u"static/logger/themes/%s" % theme, u"%s/.theme" % gLogDir)
	del shutil

def logSetState(mType, source, argv):
	if argv:
		if mType == "public":
			argv = argv.split()
			if argv[0] in ("1", u"вкл"):
				if not logConfig["chats"].count(source[1]):
					logConfig["chats"].append(source[1])
					write_file(u"dynamic/logger_cfg.txt", str(logConfig))
					reply(mType, source, u"Включил логирование «%s»." % source[1])
				else:
					reply(mType, source, u"Уже включено.")
			elif argv[0] in ("0", u"выкл"):
				if logConfig["chats"].count(source[1]):
					logConfig["chats"].remove(source[1])
					write_file(u"dynamic/logger_cfg.txt", str(logConfig))
					reply(mType, source, u"Выключил логирование «%s»." % source[1])
				else:
					reply(mType, source, u"«%s» не логируется.")
			elif argv[0] in (u"тема", "темы"):
				if len(argv) > 1:
					if	has_access(source[0], 100, source[1]):
						if argv[1] in logThemes.keys():
							if os.path.exists("%s/.theme/name.txt" % gLogDir):
								if argv[1] == read_file("%s/.theme/name.txt" % gLogDir):
									reply(mType, source, u"Тема «%s» уже используется плагином." % argv[1])
									return
							logConfig["theme"] = argv[1]
							write_file(u"dynamic/logger_cfg.txt", str(logConfig))
							logThemeCopier(argv[1])
							reply(mType, source, u"Установил тему «%s». Она вступит в силу немедленно." % argv[1])
						else:
							reply(mType, source, u"Нет такой темы :(.")
					else:
						reply(mType, source, u"Доступа не хватает...")
				else:
					answer = str()
					for x, y in enumerate(logThemes.keys()):
						answer +=  u"%i. %s.\n" % (x + 1, y)
					reply(mType, source, answer)
	else:
		if source[1] in logConfig["chats"]:
			reply(mType, source, u"Сейчас логгер включён. Тема, используемая плагином, называется «%s»." % logConfig["theme"])
		else:
			reply(mType, source, u"Сейчас комната не логируется.")

if logEnabled:
	register_stage0_init(logCacheFileInit)
	register_stage1_init(logFileInit)
	register_join_handler(logWriteJoined)
	register_leave_handler(logWriteLeave)
	register_message_handler(logWriteMessage)
	register_presence_handler(logWritePresence)
	command_handler(logSetState, 30, "logger")
	findThemes()
