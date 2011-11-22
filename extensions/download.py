# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  download_plugin.py

# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

sByte = [' %s' % (x) for x in ['0 bytes', '0 kb', '0 mb', '0 gb']]

def build_filename(DIR, name):
	name_ = '%s/%s' % (DIR, name)
	if not os.path.exists(name_):
		return name_
	name = 'copy_%s' % (name)
	return build_filename(DIR, name)

def Bytes2Tbytes(or_bytes):
	kbytes, bytes = divmod(or_bytes, 1024)
	mbytes, kbytes = divmod(kbytes, 1024)
	gbytes, mbytes = divmod(mbytes, 1024)
	tbytes, gbytes = divmod(gbytes, 1024)
	text = u'%d bytes' % (bytes)
	if or_bytes >= 1024:
		text = u'%d kb %s' % (kbytes, text)
	if or_bytes >= 1048576:
		text = u'%d mb %s' % (mbytes, text)
	if or_bytes >= 1073741824:
		text = u'%d gb %s' % (gbytes, text)
	if or_bytes >= 1099511627776:
		text = u'%d tb %s' % (tbytes, text)
	return replace_all(text, sByte, '')

def download_handler(type, source, body):
	if body:
		DIR, list = "Downloads", body.split()
		if not os.path.exists(DIR):
			os.mkdir(DIR, 0755)
		link = list[0].strip()
		if len(list) >= 2:
			name = list[1].strip()
		else:
			names = link.split('/')
			name = names[len(names) - 1]
		reply(type, source, u'Ждите окончания загрузки %s\nЭто может занять несколько минут...' % (name))
		Jid = handler_jid(source[0])
		if Jid not in [BOSS, BOSS.lower()]:
			delivery(u'Внимание! Качаю --> %s' % (link))
		dname = build_filename(DIR, name)
		try:
			from urllib import urlretrieve
			downloaded = urlretrieve(link, dname)
			del urlretrieve
		except:
			downloaded = False
		if downloaded and os.path.exists(dname):
			if len(downloaded) >= 2:
				try:
					size = int(downloaded[1].get('Content-Length', '0'))
				except:
					size = 0
			else:
				size = 0
			if size:
				repl = u'Файл "%s" (%s) успешно скачан --> %s' % (name, Bytes2Tbytes(size), dname)
			else:
				repl = u'Файл "%s" успешно скачан --> %s' % (name, dname)
			reply(type, source, repl)
		else:
			reply(type, source, u'не качается...')
	else:
		reply(type, source, u'чё качать то?')

command_handler(download_handler, 100, "download")
