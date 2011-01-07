# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  admin_plugin.py

# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

BLACK_TAGS = {'<br>': '', '&nbsp;&nbsp;&nbsp;&nbsp;': '\t', '&lt;': '<', '&gt;': '>', '<b>': u'«', '</b>': u'»', '&quot;': '"', '&#39;': "'", '&nbsp;': ' ', '&amp;': '&'}

def blacksmith_svn(type, source, body):
	if body:
		body, call, rlist = body.split(), 0, {}
		req = body[0].strip().lower()
		if req in [u'ласт', 'last']:
			try:
				repl = u'Последнее доступное обновление BlackSmith -> r%s' % re_search(read_link('http://blacksmith-bot.googlecode.com/svn/'), 'Revision', ': /') 
			except:
				repl = u'Аблом, не достучался до репозитория.'
			reply(type, source, repl)
		elif req in [u'инфо', 'info']:
			if len(body) >= 2:
				call = body[1].strip()
				if check_number(call):
					call = int(call)
			try:
				lines = re_search(read_link('http://blacksmith-bot.googlecode.com/svn/tags/'), '<ul>', '</ul>').split('<li>')
				for line in lines:
					if line.strip():
						rev_html = re_search(line, '">', '</a>')
						if rev_html.count('-'):
							number = rev_html.split('-')[1].replace('.html', '')
							if check_number(number):
								rlist[int(number)] = rev_html
				if call:
					if call in [u'лист', 'list']:
						revision = -100
					elif rlist.has_key(call):
						revision = call
					else:
						revision = -200
				else:
					revision = max(rlist.keys())
				if revision == -100:
					revs = ''
					for x in rlist.keys():
						if revs:
							revs += ', %d' % (x)
						else:
							revs = str(x)
					repl = u'Есть инфа о ревизиях: %s' % (revs)
				elif revision == -200:
					repl = u'Нет инфы о такой ревизии...'
				else:
					repl = '\n'+replace_all(unicode(re_search(read_link('http://blacksmith-bot.googlecode.com/svn/tags/%s' % (rlist[revision])), '<div>', '</div>'), 'windows-1251'), BLACK_TAGS)
			except:
				repl = u'Аблом, не достучался до репозитория.'
			reply(type, source, repl)
		else:
			reply(type, source, u'что?')
	else:
		reply(type, source, u'мм?')

register_command_handler(blacksmith_svn, 'свн', ['инфо','все'], 10, 'Выдаёт инфу об обновлениях BlackSmith в SVN', 'свн [ласт/last/инфо/info] [№ ревизии/лист]', ['свн ласт', 'свн инфо 40'])
