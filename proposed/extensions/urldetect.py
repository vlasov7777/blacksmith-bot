# BS mark.1-55
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# RC-3!
#-extmanager-extVer:2.7.4-#
import re
import urllib2

comp_link = re.compile("(http[s]?://[^\s'\"<>]+)")
comp_charset = re.compile("(.+);[ ]?charset=(.+)")
comp_charset_alt = re.compile("charset=['\"]?(.+?)[\s'\"/>]+?")

urlDetect = []
unAllowedChars = (unichr(x) for x in xrange(32) if x not in (9, 10, 13))

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

def urlParser(body, TitleMSG = "%s"):
	url = comp_link.search(body)
	answer = ""
	if url:
		try:
			url = url.group(1).strip("'.,\\]\"")
			if not chkUnicode(url):
				protocol, _ = url.split("://")[:2]
				raw = _.split("/", 1)
				if len(raw) > 1:
					domain, page = raw
					page = "/" + page
				else:
					domain, page = raw[0], ""
				if not chkUnicode(domain):
					domain = IDNA(domain)
				if not chkUnicode(page, "(~#?%&+=,:;*|)"):
					page = urllib.quote(str(page))
				url = u"%s://%s%s" % (protocol, domain, page)
			reQ = urllib2.Request(url)
			reQ.add_header("User-agent", UserAgents["BlackSmith"])
			opener = urllib2.urlopen(reQ)
			headers  = opener.headers
			cType = headers.get("Content-Type", "")
			if ("text/html" in cType) or ("application/xhtml+xml" in cType) or url.endswith((".html", ".htm")):
				data = opener.read(4500)
				Type, Charset = contentTypeParser(opener, data)
				title = getTagData("title", data)
				title = title.decode(Charset)
				if title:
					answer = TitleMSG % uHTML(title).replace("\n", "").encode("utf-8")
			else:
				Type = headers.get("Content-Type", "")
				Size = int(headers.get("Content-Length", 0))
				Date = headers.get("Last-Modified") or headers.get("Date") or ""
				if Type:
					answer += u"Тип: %s" % Type
				if Size:
					answer += u", размер: %s" % byteFormat(Size)
				if Date: 
					answer += "; последнее изменение файла: %s." % Date
				if answer:
					answer = answer % vars()
				answer = replace_all(answer, unAllowedChars, "")
		except (urllib2.HTTPError, urllib2.URLError, urllib2.socket.error) as e:
			answer = "%s: %s" % (e.__class__.__name__, e.message or str(e))
		except: 
			lytic_crashlog(urlWatcher, "", u"While parsing \"%s\"." % locals().get("url"))
	return answer


def urlWatcher(raw, mType, source, body):
	if mType == "public" and (source[1] in urlDetect) and has_access(source[0], 11, source[1]):
		if len(body) < 500:
			answer = urlParser(body, u"Заголовок: %s")
			if answer:
				msg(source[1], answer)

			
def urlWatcherConfig(mType, source, args):
	if args:	
		args = args.strip()[:500]
		argv = args.split()
		answer = ""
		if args in ("1", "0"):
			if has_access(source[0], 20, source[1]):
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
				answer = "Недостаточный доступ."
		else:
			argv = argv[:10]
			for link in argv:
				answer += "\n%s ­— %s" % (link, urlParser(link))
	reply(mType, source, answer)

def urlWatcherConfig_load():
	if initialize_file("dynamic/urlWatcher.txt", "[]"):
		globals()["urlDetect"] = eval(read_file("dynamic/urlWatcher.txt"))

def urlWatcher_04si(chat):
	if chat in urlDetect:
		urlDetect.remove(chat)
		write_file("dynamic/urlWatcher.txt", str(urlDetect))

handler_register("01eh", urlWatcher)

command_handler(urlWatcherConfig, 11, "urldetect")

handler_register("00si", urlWatcherConfig_load)
handler_register("04si", urlWatcher_04si)