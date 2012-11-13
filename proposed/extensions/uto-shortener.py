# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
# Copyright Url Shortener (by service u.to) © simpleApps CodingTeam (Fri Oct 28 18:54:26 2011)
# This program published under Apache 2.0 license
# See LICENSE.txt for more details


#-extmanager-depends:twill.zip-#
#-extmanager-extVer:1.0-#
import re
sys.path.append("twill.zip")

## plugin settings.
cookies = {"save": True,
  		   "file": "dynamic/cook.me"} ## Cook Me!

cookies["load"] = os.path.exists(cookies["file"])
		
def uto_parse(code):
	data = re.search("#shurlout'\)\.val\('(.*)'\)\.show\(\)\.focus\(\)", code)
	if data:
		data = data.group(1)
	return data

def load_uagent(twill):
	uagent = twill.commands._agent_map[random.choice(twill.commands._agent_map.keys())]
	initialize_file("dynamic/user-agent.txt", uagent)
	return read_file("dynamic/user-agent.txt")

def url_shortener(mType, source, args):
	if args:
		import twill
		twill.commands.agent(load_uagent(twill))
		if cookies.get("load"):
			twill.commands.load_cookies(cookies.get("file"))
		if not chkUnicode(args):
			args = IDNA(args)
		twill.commands.go("http://u.to/")
		twill.commands.fv("2", "url", args)
		twill.commands.submit()
		if cookies.get("save"):
			open(cookies.get("file"), "w").close()
			twill.commands.save_cookies(cookies.get("file"))
		answer = uto_parse(twill.commands.browser.get_html()) or u"Какая-то проблема с получением результата." 
		del twill
	else:
		answer = u"Не нашёл URL."
	reply(mType, source, answer)

command_handler(url_shortener, 11, "uto-shortener")