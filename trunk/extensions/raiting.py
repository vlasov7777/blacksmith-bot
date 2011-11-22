# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  raiting_plugin.py

# Idea: 40tman (40tman@qip.ru)
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)

from urllib import urlencode
def handler_jc(typ, source, body):
	if body:
		cName = body.lower()
		if cName.count('@conf'):
			cName = (cName.split('@conf'))[0].encode('utf-8')
	else:
		cName = (source[1].split('@conf'))[0].encode('utf-8')
	try:
		cName = urlencode({"search": cName})
		data = read_url("http://jc.jabber.ru/search.html?%s" % (cName), 'Mozilla/5.0')
		compile_ = re.compile('<font color="blue">(.+?)</font></a><br>\n(.+?)<br><font color="gray">(.+?)</font>')
		list = compile_.findall(data)
		if list:
			answer = "\n"
			Var = 0
			for JID, Name, Desc in list:
				body = uHTML("%s\n%s\n%s" % (JID, Name, Desc))
				body = replace_all(body, {"<b>": "", "&copy;": u"©", "</b>": "", "\r": ""})
				Var += 1
				answer += '%d) %s\n\n' % (Var, body.strip())
		else:
			answer = u'Ничего не найдено...'
	except:
		answer = u'Сервис недоступен.'
	reply(typ, source, answer)

command_handler(handler_jc, 10, "raiting")
