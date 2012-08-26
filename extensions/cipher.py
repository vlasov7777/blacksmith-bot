# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  cipher_plugin.py

# Author: ferym (ferym@jabbim.org.ru)
# http://jabbrik.ru
# ReCoded by: WitcherGeralt (WitcherGeralt@jabber.ru)

strip_tags = re.compile(r'<[^<>]+>')

def handler_shifr(type, source, body):
	if body:
		if len(body) >= 4 or len(body) <= 10:
			body = body.lower()
			try:
				data = read_url('http://combats.stalkers.ru/?a=analiz_nick&word=%s' % (body.encode('windows-1251')), 'Mozilla/5.0')
				repl = re_search(data, "<tr><td><div style='text-align:center;'><b>", '</b></div></td></tr></table><center>')
				repl = strip_tags.sub('', replace_all(repl, {'<br />': '\n', '<br>': '\n'}))
				reply(type, source, unicode(repl, 'windows-1251'))
			except:
				reply(type, source, u'что-то сломалось...')
		else:
			reply(type, source, u'слово должно содержать от 4 до 10 букв')
	else:
		reply(type, source, u'а что расшифровать-то?')

command_handler(handler_shifr, 10, "cipher")
