# caps\bot ver\core mod\bot rev\caps ver

Caps = 'http://simpleapps.ru/caps#blacksmith-m.1'
BOT_VER = 1
CORE_MODE = 48
BOT_REV = 121

if os.access('.svn/entries', os.R_OK):
	try:
		BOT_REV = int(file('.svn/entries').readlines()[3].strip())
	except: 
		pass
		
CapsVer = '%d.%d' % (BOT_VER, CORE_MODE)