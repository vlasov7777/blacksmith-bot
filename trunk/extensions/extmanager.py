# BS mark.1-55
# /* coding: utf-8 */

# BlackSmith Extension Manager
# This plugin distributed under Apache 2.0 license.
# (c) simpleApps, 2012.

## NOTICE: 
##			All plugins that depend from another plugins or files (not help files that placed in help dir)
##			Must be contain this code: #-extmanager-depends:depend1;depend2;depend3-#
##			Where depend1, depend2 and depend3 are depends of this plugin.
import urllib

svnUrl = "http://blacksmith-bot.googlecode.com/svn/proposed/%s/"
extFile = "extensions.txt"

def urlsplit(url):
	if url and url.count("/"):
		strippedUrl = url.rstrip("/")
		tailIndex = strippedUrl.rfind("/")
		head = strippedUrl[:tailIndex]
		tail = strippedUrl[tailIndex:]
		url = (head, tail)
	return url
	
def getSize(url):
	request = urllib.urlopen(url)
	return int(request.headers.get("Content-Length"))
	
def getDepsSize(depList):
	size = int()
	for dep in depList:
		size += getSize(svnUrl % dep)
	return size
	
def saveDeps(path):
	Dir = os.path.split(path)[0]	
	if Dir and not os.path.exists(Dir):
		os.makedirs(Dir)
	return path
	
def getDeps(depList = [], plugin = None):
	if plugin:
		depList = findDeps(read_url(svnUrl % "extensions/%s" % plugin))
	if depList:
		for dep in depList:
			if dep.endswith(".dir"):
				Dir = dep[:-4]
				if not os.path.exists(Dir):
					os.makedirs(Dir)
			else:
				urllib.urlretrieve(svnUrl % dep, saveDeps(dep)) 

def findDeps(data, join = None):
	match = re.search("#-extmanager-depends:(.*)-#", data)
	if match:
		dep = match.group(1)
		depList = dep.split(";")
		if join:
			return str.join(join, depList)
		return depList

def findExtVer(data):
	match = re.search("#-extmanager-extVer:(.*)-#", data)
	if match:
		ver = match.group(1)
		return ver
	return "1.0"

def extManager(mType, source, args):
	if args:
		answer = str()
		a = args.split()
		name, fullName = a[0], a[0] + ".py"
		afterA0 = args[(args.find(" ") + 1):].strip()
		extList = re.findall("\">(.*\.py)</a></li>", read_url(svnUrl % "extensions")) #"
		extList = [x[:-3] for x in extList]

		if a[0] == u"лист":
			for x, y in enumerate(extList):
				answer +=  u"%i. %s;\n" % (x + 1, y)

		elif a[0] in extList and len(a) > 1:
			if a[1] in (u"лист", u"инфо", "установить"):
				depList = findDeps(read_url(svnUrl % "extensions/%s" % fullName))
				if a[1] == u"инфо":
					pluginInfo = eval(read_url(svnUrl % ("help/" + a[0])).decode("utf-8"))
					commandList = [pluginInfo[x]["cmd"] for x in pluginInfo.keys()]
					if depList:
						jDepList = str.join(", ", depList)
						sizeOf = byteFormat(getDepsSize(depList) + getSize(svnUrl % "extensions/%s" % fullName))
					commandList = str.join(", ", commandList)
					answer =\
						"\nПлагин: %(name)s.\nСодержит команды: %(commandList)s."
					if depList:
						answer +=\
							"\nДля плагина требуется: %(jDepList)s, после установки будет занятно примерно %(sizeOf)s."
					answer = answer % vars()
	
				elif a[1] == u"установить":
					extensions = eval(read_file("dynamic/%s" % extFile))
					urllib.urlretrieve(svnUrl % "extensions/%s" % fullName, "extensions/%s" % fullName)
					urllib.urlretrieve(svnUrl % "help/" + a[0], "help/%s" % a[0])
					getDeps(depList)
					extensions[fullName] = findExtVer(read_url(svnUrl % "extensions/%s" % fullName))
					write_file("dynamic/%s" % extFile, str(extensions))
					answer = u"Плагин «%s» успешно установлен"
					try:
						execfile("./extensions/%s" % fullName, globals())
						answer += " и подгружен. Возможно, понадобится перезапуск бота."
					except:
						answer += u", однако подгрузка не удалась: \n%s" % (returnExc())
					answer = answer % name

			elif a[1] == u"удалить":
				if os.path.exists("./extensions/%s" % fullName):
					size = 0
					extensions = eval(read_file("dynamic/%s" % extFile))
					depList = findDeps(read_file("./extensions/%s" % fullName))
					try:
						for x in ("./extensions/%s" % fullName, "./help/%s" % name):
							size += os.path.getsize(x)
							os.remove(x)
						answer += u"Плагин «%(name)s» успешно удалён."
						if fullName in extensions.keys():
							del extensions[fullName]
							write_file("dynamic/%s" % extFile, str(extensions))
					except:
						answer += u"Удаление плагина «%(name)s» не удалось."
							
					if depList:
						for dep in depList:
							if os.path.exists(dep):
								size += os.path.getsize(dep)
								if not os.path.isdir(dep):
									os.remove(dep)
						depList = str.join(", ", depList)
						answer += u" Также были удалены: %(depList)s."
					size = byteFormat(size)
					answer += " Освобождённое место: %(size)s."
				else:
					answer = u"Плагин «%(name)s» не найден!"
			else:
				answer = u"Ошибка. Возможно, этого плагина нет в списке или вы указали несуществующий параметр."

		elif a[0] == u"upgrade":
			extensions = eval(read_file("dynamic/%s" % extFile))
			toUpdate = dict()
			for ext in extensions.keys():
				localVer = "7"#extensions[ext]
				remoteVer = findExtVer(read_url(svnUrl % "extensions/%s" % ext))
				if localVer != remoteVer:
					toUpdate[ext] = remoteVer
			if toUpdate:
				answer = "\nОбновлено %d плагинов: " % len(toUpdate) + str.join(", ", toUpdate)
				jDepList = []
				for ext in toUpdate.keys():
					name = ext[:-3]
					depList = findDeps(read_url(svnUrl % "extensions/%s" % ext))
					if depList:
						jDepList.extend(depList)
					urllib.urlretrieve(svnUrl % "extensions/%s" % ext, "extensions/%s" % ext)
					urllib.urlretrieve(svnUrl % "help/" + name, "help/%s" % name)
					getDeps(depList)
					extensions[ext] = toUpdate[ext]
				if jDepList:
					jDepList = str.join(", ", jDepList)
					answer += "\nТакже были установлены следующие зависимости: %(jDepList)s"
				answer = answer % vars()
				write_file("dynamic/%s" % extFile, str(extensions))
			
		reply(mType, source, answer % vars())

def extmanager_init(chat):
	if check_file("", extFile, str(dict())):
		pass
	else:
		delivery(u"Внимание! Не удалось создать extmanager.txt!")

command_handler(extManager, 100, "extmanager")

handler_register("01si", extmanager_init)