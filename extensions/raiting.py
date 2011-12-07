# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  raiting_plugin.py

# Idea: 40tman (40tman@qip.ru)
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)

from urllib import urlencode
compile_st = re.compile("<[^<>]+?>")

def uHTML(text):
	from HTMLParser import HTMLParser
	text = text.replace("<br>", "\n ").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def decodeHTML(data):
	data = compile_st.sub("", data)
	return uHTML(data.strip())

def command_jc_search(typ, source, body):
	if body:
		cName = body.lower()
		if cName.count('@conf'):
			cName = (cName.split('@conf'))[0].encode('utf-8')
	else:
		cName = (source[1].split('@conf'))[0].encode('utf-8')
	try:
		cName = urlencode({"search": cName})
		data = read_url("http://jc.jabber.ru/search.html?%s" % (cName), 'Mozilla/5.0')
		jc = re.compile("<li>((?:.|\s)+?)</li>", 16).findall(data)
		if jc:
			answer = str()
			for x,y in enumerate(jc):
				answer += "\n%d. %s" % (x + 1, y))
			answer = decodeHTML(answer)
		else:
			answer = u'Ничего не найдено...'
	except:
		answer = u'Сервис недоступен.'
	reply(typ, source, answer)

command_handler(command_jc_search, 10, "raiting")