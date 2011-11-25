# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  google_plugin.py

# (c) Gigabyte
# http://jabbrik.ru

from urllib import urlencode
noBanSymbols = u"«—»qwertyuiop[]\|asdfghjkl;':\"zxcvbnm,./ \n\t\r\n`~1234567890-=+_)(*&^%$/\\йцукенгшщзхъфывапролджэячсмитьбю.<>,ё"#u"qwertyuiop[]asdfghjkl;'zxcvbnm,.Ю`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>Б~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ёйцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,.ю`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>б~»"
#'

def uHTML(text):
	from HTMLParser import HTMLParser
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def checkForBadSymbols(text):
	for x in text:
		if x.lower() not in noBanSymbols:
			return True
	return False

def google(type, source, body):
	if body:
		try:
			results = read_link('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (urlencode({'q': body.encode('utf-8')})))
			list = simplejson.loads(results)['responseData']['results']
			noh_title = uHTML(replace_all(list[0]['title'], {'<b>': u'«', '</b>': u'»'}))
			content = uHTML(replace_all(list[0]['content'], {'<b>': u'«', '</b>': u'»'}))
			text = '%s%s\n%s' % (noh_title, content, list[0]['unescapedUrl'])
			if not checkForBadSymbols(text):
				reply(type, source, text)
			else:
				reply(type, source, u"I can't use arabic symbols :(")
		except:
			reply(type, source, u'Текст "%s" - не найден!' % (body))
	else:
		reply(type, source, u'Пустой запрос!')

command_handler(google, 10, "google")
