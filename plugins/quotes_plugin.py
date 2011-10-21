#===istalismanplugin===
# /* coding: utf-8 */
# © simpleApps Unofficial.

strip_tags = re.compile(r'<[^<>]+>')

def uHTML(text):
	from HTMLParser import HTMLParser 
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def returnExc():
	from sys import exc_info
	if exc_info()[0] or exc_info()[1]:
		error = "error: %s" % \
			str(exc_info()[0])+" - "+str(exc_info()[1])
	else:
		return None
	del exc_info
	return error

def joke(type, source, parameters):
	from xml.dom import minidom
	target = urlopen("http://anekdot.odessa.ua/rand-anekdot.php").read()
	od = re.search(">", target)
	text = target[od.end():]
	text = text[:re.search("<a href=", text).start()]
	reply(type ,source, u"Анекдот: %s" % uHTML(text.decode("cp1251")))


def bashorg(type, source, parameters):
	if parameters.strip()=='':
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
	except:
		reply(type,source, returnExc())
        

def ithappens(type, source, parameters):
	main = urlopen("http://ithappens.ru/random").read()
	od = re.search("<h3>#", main)
	id = main[od.end():]
	id = id[:re.search(":", id).start()].strip()
	od = re.search('id="story_%s">' % id, main)
	text = main[od.end():]
	text = text[:re.search("</p>", text).start()]
	reply(type,source, u"Цитата #%s:\n%s" % (id, uHTML(text.decode("cp1251"))))


def bashAbyss(type, source, args):
	if not args:
		target = urlopen('http://bash.org.ru/abysstop').read()
		try:
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


register_command_handler(bashorg, 'баш', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org.ru). Также может по заданному номеру вывести.', 'бгг', ['бгг 223344','бгг'])
register_command_handler(ithappens, 'ит', ['фан','граббер','все'], 10, 'Показывает случайную цитату ithappens (http://ithappens.ru).', 'ит', ['ит'])
register_command_handler(joke, 'анек', ['все', 'new'], 10, 'Показывает случайный анекдот с ресурса http://anekdot.odessa.ua/', 'анекдот', ['анекдот'])
register_command_handler(bashAbyss, 'борб', ['фан','инфо','все'], 0, 'Показывает случпйную цитату из бездны бора (bash.org.ru).', 'борб', ['борб'])
