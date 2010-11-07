# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  ya_plugin.py

# Idea: ferym [ferym@jabbim.org.ru]
# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]

ya_tags = '''<p class="b-phone">
</p>
<div class="www">'''

def handler_yandex(type, source, body):
	if body:
		try:
			body = replace_all(body, {' ': '%20', '@': '%40'}).encode('utf-8')
			site = read_url('http://yandex.ru/msearch?s=all&query=%s' % (body), 'Mozilla/5.0')
			data = re_search(site, '<li>', '</li>')
			repl = '\n'+replace_all(data, {'<a href="': 'link: ', ya_tags: '', '" target="_blank">': '\n', '</a>': '', '</div>': '', '<b>': '', '</b>': '', '<br/>': ' ', '<br>': ' ', '<div class="info">': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"'}).strip()
			reply(type, source, unicode(repl, 'UTF-8'))
		except:
			reply(type, source, u'По вашему запросу ничего не найдено')
	else:
		reply(type, source, u'а что искать то?')

register_command_handler(handler_yandex, 'яндекс', ['все','инфо'], 10, 'Поиск в yandex', 'яндекс <запрос>', ['яндекс jabbrik'])
