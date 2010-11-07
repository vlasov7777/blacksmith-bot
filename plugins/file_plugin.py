# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  file_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_file_create(type, source, body):
	if body:
		args = body.split()
		filename = args[0].strip()
		if filename.count('.'):
			filename = encode_filename(filename)
			if check_nosimbols(filename):
				if initialize_file(filename):
					if len(args) >= 2:
						text = body[(body.find(' ') + 1):].strip()
						try:
							data = unicode(text).encode('utf-8')
							write_file(filename, data)
							reply(type, source, u'Файл был успешно записан!')
						except:
							reply(type, source, u'Файл не был записан!')
					else:
						reply(type, source, u'Записал со стандарной data -> "{}"')
				else:
					reply(type, source, u'Не удалось создать файл, перебор директорий или системная ошибка!')
			else:
				reply(type, source, u'Содержание кириллических символов разрешается только если директорией является конференция!')
		else:
			reply(type, source, u'Необходимо установить расширение, например ".txt"')
	else:
		reply(type, source, u'Инвалид синтакс!')

register_command_handler(handler_file_create, 'файл', ['суперадмин','все'], 100, 'Создаёт файл в заданной директории с заданным именем и заранным расширением, при указании второго параметра он будет записан в файл, без него фал будет создан со стандартной data -> "{}"\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'файл <директория>/<директория>/<имя файла>.<расширение>', ['файл static/superstatic/megastatic.txt','файл dynamic/x.py','файл dynamic/flood.txt {"witcher@conference.jabber.ru": "off"}'])
