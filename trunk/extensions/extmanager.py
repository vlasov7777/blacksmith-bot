# BS mark.1
# /* coding: utf-8 */

# BlackSmith Extension Manager
# (c) simpleApps, 2012.

svnUrl = "http://blacksmith-bot.googlecode.com/svn/proposed/%s/"

def extManager(mType, source, args):
	a = args.split()
	answer = str()
	afterA0 = args[(args.find(" ") + 1):].strip()
	extList = re.findall("\">(.*\.py)</a></li>", read_url(svnUrl % "extensions")) #"
	extList = [x[:-3] for x in extList]
	if a[0] in (u"лист", u"список"):
		for x, y in enumerate(extList):
			answer +=  u"%i. %s.\n" % (x + 1, y)
	elif a[0] in extList and len(a) > 1:
		if a[1] == u"инфо":
			pluginInfo = eval(read_url(svnUrl % ("help/" + a[0])).decode("utf-8"))
			commandList = [pluginInfo[x]["cmd"] for x in pluginInfo.keys()]
			answer =\
				"\nПлагин: %s.\nСодержит команды: %s." % (a[0], str.join(", ", commandList))
		elif a[1] == u"установить":
			import urllib, shutil
			fullName = a[0] + ".py"
			urllib.urlretrieve(svnUrl % "extensions/%s" % fullName, "extensions/%s" % fullName)
			urllib.urlretrieve(svnUrl % "help/" + a[0], "help/%s" % a[0])
			del urllib, shutil
			answer = u"Плагин %s успешно установлен! Возможно, понадобится перезапуск бота." % a[0]
	else:
		answer = u"Ошибка. Возможно, этого плагина нет в списке или вы указали несуществующий параметр."
	reply(mType, source, answer)

command_handler(extManager, 100, "extmanager")