# BS mark.1-55
# /* coding: utf-8 */
# © simpleApps, 2011 - 2012.


def AnecDote(mType, source, body):
	target = urlopen("http://anekdot.odessa.ua/rand-anekdot.php").read()
	data = re.search(">(.*)<a href=", target, 16)
	if data:
		data = uHTML(data.group(1).decode("cp1251")).strip()
	reply(mType, source, u"Анекдот: \n%s" % data)

def bashOrg(type, source, body):
	if body.isdigit():
		link = "http://bash.im/quote/%s" % body
	else:
		link = "http://bash.im/random"
	data = read_url(link, UserAgents["BlackSmith"])
	try:
		data = re.search('<span id="v\d+?" class="rating">(\d+?)</span>(?:.|\s)+?<a href="/quote/\d+?" class="id">#(\d+?)</a>\s*?</div>\s+?<div class="text">((?:.|\s)+?)</div>', data, 16)
		if data:
			rate, id, data = data.groups()
			answer = uHTML(u"Цитата: #%s (Рейтинг: %s)\n%s" % (id, rate, data.decode("cp1251")))
		else:
			answer = u"Ошибка."
		reply(type, source, answer)
	except Exception:
		reply(type, source, returnExc())


def itHappens(mType, source, body):
	if body and body.isdigit():
		url = "http://ithappens.ru/story/%s" % body
	else:
		url = "http://ithappens.ru/random"
	data = read_url(url, UserAgents["BlackSmith"])
	data = re.search("<div class=\"text\">(.*)</p>", data, 16)
	if data:
		data = data.group(1).decode("cp1251")
		data = stripTags(uHTML(data), " ")
	reply(mType, source, data)


## TODO: Fix it. Rewrite to RE. (mrDoctorWho)
def bashAbyss(type, source, args):
	try:
		target = read_url('http://bash.org.ru/abysstop', UserAgents["BlackSmith"])
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

def JQuotes(mType, source, body):
	if body and body.isdigit():
		url = "http://jabber-quotes.ru/api/read/?id=%d" % body
	else:
		url = "http://jabber-quotes.ru/api/read/?id=random"
	data = read_url(url, UserAgents["BlackSmith"])
	data = re.search("<id>(.*)</id>\n<author>(.*)</author>\n<quote>(.*)</quote>", data, 16)
	if data:
		iD, Author, Quote = data.groups()
	reply(mType, source, "\nЦитата: #%s | Автор: %s.\n%s" % (iD, Author, uHTML(Quote)))

def pyOrg(type, source, body):
	try:
		data = re_search(read_link('http://python.org/'), '<h2 class="news">', '</div>')
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
			 UserAgents["BlackSmith"]), '<form id="qForm" method="post"><div align="center">', '</div>')
		data = strip_tags.sub('', uHTML(data))
		reply(type, source, data.decode('cp1251'))
	except Exception:
		reply(type, source, returnExc())

# Coded by: Evgеn [email: meb81@mail.ru]
# http://witcher-team.ucoz.ru/
# TODO: Rewrite it to re (mrDoctorWho)

def Fomenko(mType, source, body):
	try:
		radky = read_link("http://www.fomenko.ru/foma/lenta/text.html").splitlines()
		if len(radky) >= 16:
			radky = radky[15].decode('windows-1251')
			if radky.find("<b>"):
				radky = radky.split('<b>')[1]
			else:
				radky = u'что-то левое с разметкой'
		else:
			radky = u'что-то левое с разметкой'
	except:
		radky = u'не могу пропарсить сайт'
	reply(mType, source, radky)

def command_Chuck(mType, source, body):
	if body and check_number(body):
		Ask = "/quote/%d" % int(body)
	else:
		Ask = "/random"
	try:
		data = read_url("http://chucknorrisfacts.ru/%s" % Ask, UserAgents["BlackSmith"])
	except urllib2.HTTPError, exc:
		answer = str(exc)
	except:
		answer = u"Не могу получить доступ к странице."
	else:
		data = data.decode("cp1251")
		comp = re.compile("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
		data = comp.search(data)
		if data:
			answer = stripTags(uHTML(u"Факт #%s:\n%s" % data.groups()))
		else:
			answer = u"Проблемы с разметкой..."
	reply(mType, source, answer)

command_handler(command_Chuck, 10, "quotes")
command_handler(Fomenko, 10, "quotes")
command_handler(JQuotes, 10, "quotes")
command_handler(pyOrg, 10, "quotes")
command_handler(bashOrg, 0, "quotes")
command_handler(itHappens, 10, "quotes")
command_handler(AnecDote, 10, "quotes")
# command_handler(bashAbyss, 0, "quotes")
command_handler(afor, 10, "quotes")
