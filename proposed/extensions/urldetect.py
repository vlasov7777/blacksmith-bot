# BS mark.1-55
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# RC-1!
#-extmanager-extVer:2.5-#
import re
import urllib2

comp_link = re.compile("(http[s]?://[^\s'\"<>]+)")
comp_charset = re.compile("(.+);[ ]?charset=(.+)")
comp_charset_alt = re.compile("charset=['\"]?(.+?)[\s'\"/>]+?")

urlDetect = []

def contentTypeParser(opener, data):
	Charset, Type = None, opener.headers.get("Content-Type")
 	try:
		if Type and Type.count(";"):
			Type, Charset = comp_charset.search(Type).groups()
			Charset = Charset.strip("'\"").lower()
			if Charset == "unicode":
				Charset = "utf-8"
			if Charset.count("."):
				Charset = Charset.split(".")[1]
		elif (not Charset and Type == "text/html") or opener.url.endswith((".html", ".htm")):
			Charset = comp_charset_alt.search(data)
			if Charset:
				Charset = Charset.group(1)
	except:
		lytic_crashlog(contentTypeParser, "", u"During the search encoding on %s." % opener.url)
	if not Charset:
		Charset = "utf-8"
	return (Type, Charset) 

def ChrReplacer(text):
	for character in xrange(32):
		if character not in (9, 10, 13):
			text = text.replace(unichr(character), "")
	return text

def urlWatcher(raw, mType, source, body):
	if mType == "public" and (source[1] in urlDetect) and has_access(source[0], 11, source[1]):
		if len(body) < 500:
			try:
				url = comp_link.search(body)
				if url:
					url = url.group(1).strip("'.,\\)\"")
					if not chkUnicode(url):
						protocol, _ = url.split("://")
						raw = _.split("/", 1)
						if len(raw) > 1:
							domain, page = raw
							page = "/" + page
						else:
							domain, page = raw[0], ""
						if not chkUnicode(domain):
							domain = IDNA(domain)
						if not chkUnicode(page, "~#?%&=,:;*|-"):
							page = urllib.quote(str(page))
						url = u"%s://%s%s" % (protocol, domain, page)
					reQ = urllib2.Request(url)
					reQ.add_header("User-agent", UserAgents["BlackSmith"])
					opener = urllib2.urlopen(reQ)
					headers  = opener.headers
					if "text/html" in headers.get("Content-Type") or url.endswith((".html", ".htm")):
						data = opener.read(4500)
						Type, Charset = contentTypeParser(opener, data)
						title = getTag("title", data)
						title = title.decode(Charset)
						answer = u"Заголовок: %s" % uHTML(title).replace("\n", "").encode("utf-8")
					else:
						Type = headers.get("Content-Type") or ""
						Size = byteFormat(int(headers.get("Content-Length") or 0))
						Date = headers.get("Last-Modified") or ""
						if Date: 
							Date = "; последнее изменение файла: %s." % Date
						answer = u"Тип: %(Type)s, размер: %(Size)s%(Date)s" % vars()
					msg(source[1], ChrReplacer(answer))
			except (urllib2.HTTPError, urllib2.URLError) as e:
				msg(source[1], str(e))
			except: 
				lytic_crashlog(urlWatcher, "", u"While parsing \"%s\"." % locals().get("url"))

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
		answer = u"Что?"
	reply(mType, source, answer)

def urlWatcherConfig_load():
	if initialize_file("dynamic/urlWatcher.txt", "[]"):
		globals()["urlDetect"] = eval(read_file("dynamic/urlWatcher.txt"))

handler_register("01eh", urlWatcher)

command_handler(urlWatcherConfig, 20, "urldetect")

handler_register("00si", urlWatcherConfig_load)
