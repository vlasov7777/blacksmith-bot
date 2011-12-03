#===istalismanplugin===
# /* coding: utf-8 */
# © simpleApps Unofficial.

strip_tags = re.compile(r'<[^<>]+>')

uagent = "Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.13337/724; U; ru)"

def uHTML(text):
	from HTMLParser import HTMLParser
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def joke(type, source, parameters):
	from xml.dom import minidom
	target = urlopen("http://anekdot.odessa.ua/rand-anekdot.php").read()
	od = re.search(">", target)
	text = target[od.end():]
	text = text[:re.search("<a href=", text).start()]
	reply(type ,source, u"Анекдот: %s" % uHTML(text.decode("cp1251")))


def bashOrg(type, source, parameters):
	if not parameters:
		target = urlopen('http://bash.org.ru/random').read()
	else:
		target = urlopen('http://bash.org.ru/quote/'+parameters.strip()).read()
	try:
		od = re.search('<div class="vote">',target)
		b1 = target[od.end():]
		b1 = b1[:re.search('</a>',b1).start()]
		b1 = strip_tags.sub('', b1.replace('\n', '').replace(chr(9), ""))
		b1 = 'http://bash.org.ru/quote/'+b1+'\n'
		od = re.search(r'<div class="q">.*?<div class="vote">.*?</div>.*?<div>(.*?)</div>.*?</div>', target, re.DOTALL)
		message = b1+od.group(1)
		reply(type,source, uHTML(message.decode('cp1251')))
	except Exception:
		reply(type, source, returnExc())


def itHappens(type, source, parameters):
	main = urlopen("http://ithappens.ru/random").read()
	od = re.search("<h3>#", main)
	id = main[od.end():]
	id = id[:re.search(":", id).start()].strip()
	od = re.search('id="story_%s">' % id, main)
	text = main[od.end():]
	text = text[:re.search("</p>", text).start()]
	reply(type,source, u"Цитата #%s:\n%s" % (id, uHTML(text.decode("cp1251"))))


def bashAbyss(type, source, args):
	try:
		target = read_url('http://bash.org.ru/abysstop', uagent)
		id=`random.randrange(1, 25)`
		od = re.search('<b>'+id+':',target)
		q1 = target[od.end():]
		q1 = q1[:re.search('\n</div>',q1).start()]
		od = re.search('<div>',q1)
		message = q1[od.end():]
		message = message[:re.search('</div>',message).start()]	         
		reply(type,source, uHTML(message.decode('cp1251')))
	except:
		reply(type,source, returnExc())

def jQuotes(type, source, body):
	if body:
		body = body.lower()
	if body in (u'ранд', 'rand'):
		link = 'http://jabber-quotes.ru/random'
	elif body in (u'топ20', 'top20'):
		link = 'http://jabber-quotes.ru/up'
	else:
		link = 'http://jabber-quotes.ru/'
	try:
		List = read_link(link).split('<blockquote>')
		List.pop(0)
		quote = random.choice(List).split('</blockquote>')[0].decode('cp1251')
		quote = uHTML(quote)
		quote = quote.replace('\n\n\n', '\n\n')
		reply(type, source, quote)
	except Exception:
		import traceback
		reply(type, source, `traceback.format_exc()`)

def pyOrg(type, source, body):
	try:
		data = re_search(read_link('http://python.org/'), 
			'<h2 class="news">', '</div>')
		data, repl = strip_tags.sub('', uHTML(data)), "\n"
		for line in data.splitlines():
			if line.strip():
				repl += '%s\n' % (line)
		reply(type, source, repl.decode('koi8-r'))
	except Exception:
		reply(type, source, returnExc())

def afor(type, source, body):
	try:
		data = re_search(read_url('http://skio.ru/quotes/humour_quotes.php',
			 uagent), '<form id="qForm" method="post"><div align="center">', '</div>')
		data = strip_tags.sub('', uHTML(data))
		reply(type, source, data.decode('cp1251'))
	except Exception:
		reply(type, source, returnExc())


command_handler(jQuotes, 10, "quotes")
command_handler(pyOrg, 10, "quotes")
command_handler(bashOrg, 0, "quotes")
command_handler(itHappens, 10, "quotes")
command_handler(joke, 10, "quotes")
command_handler(bashAbyss, 0, "quotes")
command_handler(afor, 10, "quotes")
