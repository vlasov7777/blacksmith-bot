# BS mark.1-55
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# BETA!
#-extmanager-extVer:1.5-#
import re
import urllib2

def contentTypeParser(opener, data):
	ContentType = opener.headers.get("Content-Type")
	Type, Charset = ContentType, None
 	try:
		if ContentType.count(";"):
			Type, Charset = re.findall("(.*);[ ]?charset=(.*)", ContentType)[0]
			Charset = Charset.lower()
			if Charset == "unicode": Charset = "utf-8"
		if not (Charset and Type == "text/html") or opener.url.endswith((".html", ".htm")):
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
					url = url[0].split()[0].strip(".,\\)\"")
					if not chkUnicode(url): url = "http://" + IDNA(url)
					reQ = Request(link)
					reQ.add_header("User-agent", UserAgents["BlackSmith"])
					opener = urllib2.urlopen(reQ)
					headers  = opener.headers
					if "text/html" in headers.get("Content-Type") or url.endswith(".html"):
						data = opener.read(4500)
						Type, Charset = contentTypeParser(opener, data)
						title = getTag("title", data)
						title = title.decode(Charset)
						answer = u"Заголовок: %s" % uHTML(title).replace("\n", "")
					else:
						Type = headers.get("Content-Type") or ""
						Size = byteFormat(int(headers.get("Content-Length") or 0))
						Date = headers.get("Last-Modified") or ""
						answer = u"Тип: %s, размер: %s; последнее изменение файла: %s." % (Type, Size, Date)
					msg(source[1], answer)
			except: 
				lytic_crashlog(urlWatcher, "", u"While parsing \"%s\"." % locals().get("url"))

def urlWatcherConfig(mType, source, args):
	if args:
		if mType == "public":
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
			answer = u"Только для чатов."
	else:
		answer = u"что?"
	reply(mType, source, answer)

def urlWatcherConfig_load():
	if initialize_file("dynamic/urlWatcher.txt", str(list())):
		globals()["urlDetect"] = eval(read_file("dynamic/urlWatcher.txt"))

handler_register("01eh", urlWatcher)

command_handler(urlWatcherConfig, 20, "urldetect")

handler_register("00si", urlWatcherConfig_load)
