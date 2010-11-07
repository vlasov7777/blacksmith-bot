# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  bs64dec_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_bs64_decode(type, source, body):
	if body:
		try:
			code = base64.b64decode(body)
		except:
			code = u'Невозможно раскодировать!'
		reply(type, source, code)
	else:
		reply(type, source, u'чё декодить то?')

def handler_bs64_encode(type, source, body):
	if body:
		try:
			code = base64.b64encode(body.encode('utf-8'))
		except:
			code = u'Невозможно закодировать!'
		reply(type, source, code)
	else:
		reply(type, source, u'чё кодировать то?')

def handler_bs64_decode_write(type, source, filename):
	if filename:
		if os.path.exists(filename.encode('utf-8')):
			split_filename = filename.split('/')
			name = 'decoded_files/'+split_filename[len(split_filename) - 1].split('.')[0]+'.py'
			if initialize_file(name):
				try:
					data = base64.b64decode(read_file(filename))
					write_file(name, data)
					reply(type, source, name)
				except:
					reply(type, source, u'Невозможно раскодировать!')
			else:
				reply(type, source, u'системная ошибка, не удалось создать файл')
		else:
			reply(type, source, u'нет такого файла')
	else:
		reply(type, source, u'чё кодировать то?')

def handler_bs64_encode_write(type, source, filename):
	if filename:
		if os.path.exists(filename.encode('utf-8')):
			split_filename = filename.split('/')
			name = 'files_md5/'+split_filename[len(split_filename) - 1].split('.')[0]+'.md5'
			if initialize_file(name):
				try:
					data = base64.b64encode(read_file(filename))
					write_file(name, data)
					reply(type, source, name)
				except:
					reply(type, source, u'Невозможно закодировать!')
			else:
				reply(type, source, u'системная ошибка, не удалось создать файл')
		else:
			reply(type, source, u'нет такого файла')
	else:
		reply(type, source, u'чё кодировать то?')

register_command_handler(handler_bs64_decode_write, 'декод*', ['суперадмин','все'], 100, 'Декодирует текст (код) заданного файла (base64) и записывает его', 'декод [файл]', ['декод mods/boltalka.md5'])
register_command_handler(handler_bs64_decode, 'декод', ['суперадмин','все'], 80, 'Декодирует заданное выдажение (base64)', 'декод [выражение]', ['декод dzffsf'])
register_command_handler(handler_bs64_encode_write, 'энкод*', ['суперадмин','все'], 100, 'Кодирует текст (код) заданного файла (в base64) и записывает его', 'энкод [файл]', ['энкод plugins/boltalka_plugin.py'])
register_command_handler(handler_bs64_encode, 'энкод', ['суперадмин','все'], 80, 'Кодирует заданное выдажение (в base64)', 'энкод [выражение]', ['энкод def handler_...'])
