# BS mark.1
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# BETA! 
import re

urlDetect = []

def contentTypeParser(opener, data):
	ContentType = opener.headers.get("Content-Type")
	Type, Charset = ContentType, None
	try:
		if ContentType.count(";"):
			Type, Charset = re.findall("(.*); charset=(.*)", ContentType)[0]
			Charset = Charset.lower()
			if Charset == "unicode": Charset = "utf-8"
		if not Charset and Type == "text/html":
			Charset = re.findall("/?charset=[\"|']?(.+?)['|\"|\>|\/]/?", data)[0]
	except:
		lytic_crashlog(contentTypeParser, "", u"During the search encoding on %s." % opener.url)
		Charset = "utf-8"
	return (Type, Charset) 
		
	
def urlWatcher(raw, mType, source, body):
	if mType == "public" and (source[1] in urlDetect) and has_access(source[0], 11, source[1]):
		if len(body) < 500:
			try:
				url = re.findall(r'(http[s]?://.*)', body)
				if url:
					url = url[0].split()[0]
					if not chkUnicode(url): url = "http://" + IDNA(url)
					url = urllib.urlopen(url)
					data = url.read()[:4500]
					Type, Charset = contentTypeParser(url, data)
					data = data.decode(Charset)
					if Type != "text/html": return
					title = getTag("title", data)
					msg(source[1], u"Заголовок: %s" % title)
			except (IOError, UnicodeError):
				pass
			except: 
				lytic_crashlog(urlWatcher)

def urlWatcherConfig(mType, source, args):
	if args:
		args = args.strip()
		if args == "1":
			if source[1] in urlDetect:
				answer = u"Уже включено."
			else:
				urlDetect.append(source[1])
				write_file("dynamic/urlWatcher.txt", str(urlDetect))
				answer = u"Включил автодетект ссылок."
		elif args == "0":
			if source[1] in urlDetect:
				urlDetect.remove(source[1])
				write_file("dynamic/urlWatcher.txt", str(urlDetect))
				answer = u"Выключил автодетек ссылок."
			else:
				 answer = u"Не включено."
		else:
			answer = u"Неизвестный параметр."
	else:
		answer = u"что?"
	reply(mType, source, answer)

def urlWatcherConfig_load():
	if initialize_file("dynamic/urlWatcher.txt", str(list())):
		globals()["urlDetect"] = eval(read_file("dynamic/urlWatcher.txt"))

register_message_handler(urlWatcher)
register_stage0_init(urlWatcherConfig_load)
command_handler(urlWatcherConfig, 20, "urldetect")