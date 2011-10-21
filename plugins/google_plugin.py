# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  google_plugin.py

# (c) Gigabyte
# http://jabbrik.ru

from urllib import urlencode

def uHTML(text):
	from HTMLParser import HTMLParser 
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def google(type, source, body):
	if body:
		try:
			results = read_link('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (urlencode({'q': body.encode('utf-8')})))
			list = simplejson.loads(results)['responseData']['results']
			noh_title = uHTML(replace_all(list[0]['title'], {'<b>': u'«', '</b>': u'»'}))
			content = uHTML(replace_all(list[0]['content'], {'<b>': u'«', '</b>': u'»'}))
			reply(type, source, '%s%s\n%s' % (noh_title, content, list[0]['unescapedUrl']))
		except:
			reply(type, source, u'Текст "%s" - не найден!' % (body))
	else:
		reply(type, source, u'Пустой запрос!')

register_command_handler(google, 'гугл', ['все','инфо'], 10, 'Ищет текст через Google', 'гугл', ['гугл что то'])
