# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  raiting_plugin.py

# Idea: 40tman (40tman@qip.ru)
# Coded by: Evgen (evgenadm@qip.ru)
# Part of code (the most stupid part):
# --> WitcherGeralt (WitcherGeralt@jabber.ru)

def handler_jc(type, source, body):
	if body:
		conf = body.lower()
		if conf.count('@conf'):
			conf = (conf).split('@conf')[0]
	else:
		conf = (source[1]).split('@conf')[0]
	try:
		list = {u'№': '%E2%84%96', u'ю': '%D1%8E', u'б': '%D0%B1', u'ь': '%D1%8C', u'т': '%D1%82', u'и': '%D0%B8', u'м': '%D0%BC', u'ч': '%D1%87', u'я': '%D1%8F', u'э': '%D1%8D', u'ж': '%D0%B6', u'д': '%D0%B4', u'р': '%D1%80', u'п': '%D0%BF', u'в': '%D0%B2', u'ы': '%D1%8B', u'ф': '%D1%84', u'е': '%D0%B5', u'к': '%D0%BA', u'у': '%D1%83', u'с': '%D1%81', u'а': '%D0%B0', u'л': '%D0%BB', u'о': '%D0%BE', u'й': '%D0%B9', u'ё': '%D1%91', u'ц': '%D1%86', u'н': '%D0%BD', u'г': '%D0%B3', u'щ': '%D1%89', u'ш': '%D1%88', u'з': '%D0%B7', u'х': '%D1%85', u'ъ': '%D1%8A'}
		if not check_nosimbols(conf):
			for symbol in list:
				if conf.count(symbol):
					conf = conf.replace(symbol, list[symbol])
		data = read_url('http://jc.jabber.ru/search.html?search=%s' % (conf), 'Mozilla/5.0')
		od = re.search('<div align="left">', data)
		text = data[od.end():]
		number = text.count('<font color="blue">')
		if number:
			repl, col = '\r', 1
			while col <= number:
				text = text[re.search('<font color="blue">', text).end():]
				body = text[:re.search('<br><br>', text).start()]
				body = replace_all(body, {'\r': '', '</font>': '', '&nbsp;': ' ', '<br>': '\n', '</a>': '', '<b>': '', '</b>': '', '<font color="gray">': '', '\n\n': '\n'}).strip()
				repl += '%d) %s\n\n' % (col, body)
				col += 1
			reply(type, source, repl)
		else:
			reply(type, source, (text[:re.search('</div>', text).start()]))
	except:
		reply(type, source, u'По вашему запросу ничего не найдено!')

register_command_handler(handler_jc, 'рейтинг', ['все','инфо'], 10, 'Поиск конференций в рейтинге jc. Без параметров покажет рейтинг текущей конференции. ', 'рейтинг [конфа]', ['рейтинг','рейтинг Witcher'])
