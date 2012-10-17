# BS mark.1-55
# /* coding: utf-8 */

# (c) simpleApps CodingTeam, 2012.

#-extmanager-depends:twill.zip-#
#-extmanager-extVer:0.99-#

import re
if not "module.zip" in sys.path:
	sys.path.append("module.zip")

strip_tags = re.compile(r'<[^<>]+>')
whatColorSite = "http://xml.yandex.net/cgi/color-search.pl"

def uHTML(text):
	from HTMLParser import HTMLParser
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def load_uagent(twill):
	uagent = twill.commands._agent_map[random.choice(twill.commands._agent_map.keys())]
	initialize_file("dynamic/user-agent.txt", uagent)
	return read_file("dynamic/user-agent.txt")

def whatColor_parser(data):
	pattern = re.compile("<td width='16%'/><td>(.+?)</td></tr>", 16)
	data = pattern.search(data)
	if data:
		data = uHTML(data.group(1))
	return data

def whatColorFill(mType, source, key):
	if key:
		try:
			if len(key) > 15:
				key = key[:15]
			import twill # We think that it is valid choice because our lovin parser have many dependies :(
			twill.commands.agent(load_uagent(twill))  # :( and we so lazy for write POST-request by standart python urils
			twill.commands.go(whatColorSite)
			twill.commands.fv("1", "query", key)
			twill.commands.submit()
			answer = whatColor_parser(twill.commands.browser.get_html())
			answer = strip_tags.sub('', answer)
			del twill
		except:
			answer = u"Ошибка."
	else:
		answer = u"Что?"
	reply(mType, source, answer)
	
command_handler(whatColorFill, 11, "whatscolor")
