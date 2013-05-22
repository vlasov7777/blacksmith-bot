# caps / bot ver / core mode / bot revision / caps version

Caps = "http://simpleapps.ru/caps#blacksmith-m.1"
BOT_VER = 1
CORE_MODE = 61
BOT_REV = 165

if os.access(".svn/entries", os.R_OK):
	try:
		BOT_REV = int(file(".svn/entries").readlines()[3].strip())
	except Exception: 
		try:
			svnversion = os.popen("svnversion").read()
			if not "not found" in svnversion:
				if ":" in svnversion:
					BOT_REV = svnversion.split(":")[1]
				else:
					BOT_REV = svnversion
		except:
			pass
CapsVer = "%d.%d" % (BOT_VER, CORE_MODE)