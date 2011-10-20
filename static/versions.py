# caps\bot ver\core mod\bot rev\caps ver

Caps = 'http://witcher-team.ucoz.ru/'
BOT_VER = 1
CORE_MODE = 39
BOT_REV = 64
CapsVer = '%d.%d' % (BOT_VER, CORE_MODE)

BOT_REV = 64
if os.access('.svn/entries', os.R_OK):
	try:
		BOT_REV = read_file('.svn/entries').readlines()[3].strip()
	except: 
		pass