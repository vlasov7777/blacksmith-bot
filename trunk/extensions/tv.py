# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  tv_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_tv_ya(type, source, channel):
	if channel:
		if check_number(channel):
			try:
				lines, repl = read_url('http://tv.yandex.ru/?mode=print&channel=%s' % (channel), 'Mozilla/5.0').splitlines(), ''
				for line in lines:
					if line.find('<div>') != -1:
						if re.search('<.*?>\d', line):
							repl += '\n'+replace_all(line, ['\n', '<div>', '<b>', '</div>', '</b>'], '')
				if not repl:
					repl = u'Нет программы на сегодня!'
				else:
					repl = unicode(repl, 'UTF-8')
			except:
				repl = u'Не вышло...'
		else:
			repl = u'Пиши номер канала в листе (команда: "тв_лист")'
	else:
		repl = u'Программа какого канала нужна?'
	reply(type, source, repl)

def handler_tvlist(type, source, body):
	try:
		list, repl = read_url('http://tv.yandex.ru/', 'Mozilla/5.0').splitlines(), ''
		for channel in list:
			if channel.find('<option value="') != -1:
				repl += '\n'+replace_all(channel, {'">': '.', '<option value="': '', '\n': '', '\t': '', '\r': '', '</option>': '', '</select>': '', '</td>': '', '&amp;': ' '})
		if repl:
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, unicode(repl, 'UTF-8'))
		else:
			reply(type, source, u'не могу достать список')
	except:
		reply(type, source, u'не вышло')

command_handler(handler_tv_ya, 10, "tv")
command_handler(handler_tvlist, 10, "tv")
