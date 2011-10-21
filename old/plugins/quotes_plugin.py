# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  quotes_plugin.py

# Some of ideas and part of code:
#  Gigabyte (gigabyte@ngs.ru)
#  ferym (ferym@jabbim.org.ru)
# --> http://jabbrik.ru/
# Coded By:
#  WitcherGeralt (WitcherGeralt@jabber.ru)
#  *MAG* (admin@jabbon.ru)
# --> http://witcher-team.ucoz.ru/

strip_tags = re.compile(r'<[^<>]+>')

def url_dec(body):
	body = strip_tags.sub('', replace_all(body, {'<br />': ' ', '<br>': '\n'}))
	body = replace_all(body, {'&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"', '\t': '', '||||:]': '', '>[:\n': '', '&deg;': '°'})
	return body.strip()

def handler_bashorgru(type, source, body):
	try:
		if body:
			site = read_url('http://bash.org.ru/quote/%s' % (body), 'Mozilla/5.0')
		else:
			site = read_url('http://bash.org.ru/random', 'Mozilla/5.0')
		od = re.search(r'<div class="q">.*?<div class="vote">.*?</div>.*?<div>(.*?)</div>.*?</div>', site, re.DOTALL)
		b1 = strip_tags.sub('', re_search(site, '<div class="vote">', '</a>').replace('\n', ''))
		repl = replace_all('%s\n%s' % (b1, od.group(1)), {'&nbsp;': ' ', '<br />': '\n', '&lt;': '<', '&gt;': '>', '&quot;': '"', '\t': '', '||||:]': '', '>[:\n': '', '&deg;': '°', '<br>': '\n', '\n\n\n': '\n', '\n\n': '\n'}).strip()
		reply(type, source, 'http://bash.org.ru/quote/%s' % (unicode(repl, 'windows-1251')))
	except:
		reply(type, source, u'очевидно, они опять сменили разметку')

def handler_nyash(type, source, body):
	try:
		target = read_url('http://nya.sh/', 'Mozilla/5.0')
		b1 = re_search(target, '<div align="right" class="sm"><a href="/', '"><b>')
		post = random.randrange(1, int(b1.split('/')[1]))
		target = read_link('http://nya.sh/post/%d' % (post))
		b1 = re_search(target, '</a></div><div class="content">', '</div>')
		reply(type, source, u'Цитата #%d:\n%s' % (post, unicode(url_dec(b1), 'windows-1251')))
	except:
		reply(type, source, u'повторите запрос')

def handler_ithappens(type, source, body):
	try:
		target = read_url('http://ithappens.ru/', 'Mozilla/5.0')
		b1 = re_search(target, '<h3><a href="/', '">')
		post = random.randrange(1, int(b1.split('/')[1]))
		target = read_link('http://ithappens.ru/story%d' % (post))
		b1 = re_search(target, '<p class="text">', '</p>')
		reply(type, source, u'Цитата #%d:\n%s' % (post, unicode(url_dec(b1), 'windows-1251')))
	except:
		reply(type, source, u'повторите запрос')

def handler_sonnik(type, source, body):
	if body:
		try:
			target = read_url('http://sonnik.ru/search.php?key=%s' % (body.encode('windows-1251')), 'Mozilla/5.0')
			data = re_search(target, '</p><br><p class="smalltxt"><strong>', '<br><strong>')
			data1 = re_search(data, 'html">', '</a>')
			data2 = re_search(target, '<title>', '</title>')
			data3 = re_search(target, '<p id="main3">', '</p>')
			reply(type, source, u'Тема: %s\n%s\n%s' % (unicode(data1, 'windows-1251'), unicode(data2, 'windows-1251'), unicode(data3, 'windows-1251')))
		except:
			reply(type, source, u'Странные у тебя сны... Нет такого в соннике!')
	else:
		reply(type, source, u'введи слово')

def handler_anek(type, source, body):
	try:
		list = re_search(read_link('http://www.hyrax.ru/cgi-bin/an_java.cgi'), 'td aling=left><br>', '</td></tr></table>').split('<br><br><hr>')
		list.pop(3)
		anek = u'Анекдот:\n%s' % unicode(random.choice(list), 'windows-1251')
		reply(type, source, replace_all(anek, {'<br>': '', '&nbsp;&nbsp;&nbsp;&nbsp;': '\n', '&nbsp;': '', '\n\n': '\n'}).strip())
	except:
		reply(type, source, u'что-то сломалось...')

def handler_afor(type, source, body):
	try:
		data = re_search(read_url('http://skio.ru/quotes/humour_quotes.php', 'Mozilla/5.0'), '<form id="qForm" method="post"><div align="center">', '</div>')
		data = strip_tags.sub('', replace_all(data, {'<br />': '\n', '<br>': '\n'}))
		reply(type, source, unicode(data, 'windows-1251'))
	except:
		reply(type, source, u'что-то сломалось...')

def handler_pyorg(type, source, body):
	try:
		data = re_search(read_link('http://python.org/'), '<h2 class="news">', '</div>')
		data, repl = replace_all(strip_tags.sub('', data.replace('<br>','\n')), {'&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"', '<br />': '\n', '<li>': '\r\n'}).strip(), '\n'
		for line in data.splitlines():
			if line.strip():
				repl += '%s\r\n' % (line)
		reply(type, source, unicode(repl, 'koi8-r'))
	except:
		reply(type, source, u'что-то сломалось...')

HORO_SIGNS = {u'день': 0, u'овен': 1, u'телец': 2, u'близнецы': 3, u'рак': 4, u'лев': 5, u'дева': 6, u'весы': 7, u'скорпион': 8, u'стрелец': 9, u'козерог': 10, u'водолей': 11, u'рыбы': 12}

def handler_horo(type, source, body):
	if body:
		body, number = body.lower(), None
		if body in [u'хелп', 'help']:
			reply(type, source, '\n'+'\n'.join(sorted(['%s - %d' % (x, y) for x, y in HORO_SIGNS.iteritems()])))
		else:
			if HORO_SIGNS.has_key(body):
				number = HORO_SIGNS[body]
			elif check_number(body):
				chislo = int(body)
				if -1 < chislo < 13:
					number = chislo
			if number != None:
				try:
					data = re_search(read_link('http://www.hyrax.ru/cgi-bin/bn_html.cgi'), '<!-- %d --><b>' % (number), '<br><br>')
					horo = replace_all(data, [' </b><br>', '</b><br>'], ':')
					repl = unicode(horo, 'windows-1251')
				except:
					repl = u'что-то сломалось...'
				reply(type, source, repl)
			else:
				reply(type, source, u'не понимаю')
	else:
		reply(type, source, u'введи знак')

register_command_handler(handler_pyorg, 'питон', ['фан','все'], 10,'показывает последнии новости с http://python.org/', 'питон', ['питон'])
register_command_handler(handler_afor, 'афоризм', ['фан','все'], 10,'показывает случайный афоризм с ресурса skio.ru', 'афор', ['афор'])
register_command_handler(handler_anek, 'анек', ['все', 'фан'], 10, 'Отображает анекдоты с ресурса http://www.hyrax.ru/\nBy *MAG*', 'анек', ['анек'])
register_command_handler(handler_bashorgru, 'баш', ['фан','все'], 10, 'Показывает случайную цитату (или по номеру) с баш.орг', 'баш', ['баш','баш 3557'])
register_command_handler(handler_nyash, 'няш', ['фан','все'], 10, 'Показывает случайную цитату из НЯШа .', 'няш', ['няш'])
register_command_handler(handler_ithappens, 'ит', ['фан','все'], 10, 'Показывает случайную цитату с http://ithappens.ru/', 'ит', ['ит'])
register_command_handler(handler_sonnik, 'сон', ['фан','все'], 10, 'Сонник.', 'сон', ['сон вода'])
register_command_handler(handler_horo, 'хоро', ['фан','все'], 10, 'Гороскоп "на сегодня" с сайта http://www.hyrax.ru/\nЧтобы посмотреть общую характеристику дня используем параметр - "день"\nВместо знака можно вводить число (пишем: "хоро хелп")\nBy *MAG* & WitcherGeralt for http://witcher-team.ucoz.ru/', 'хоро [знак]', ['хоро 11','хоро день', 'хоро овен'])
