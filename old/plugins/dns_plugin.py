#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  dns_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

import socket

def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(query)
		except socket.gaierror:
			return u'не нахожу что-то'
		return ', '.join(ipaddrlist)
	else:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		except socket.herror:
			return u'не нахожу что-то'
		return hostname+' '+string.join(aliaslist)+' '+string.join(aliaslist)

def handler_dns_dns(type, source, body):
	if body:
		result = dns_query(body)
		reply(type, source, unicode(result))
	else:
		reply(type, source, u'что это было?')

register_command_handler(handler_dns_dns, 'днс', ['инфо','все'], 10, 'Показывает ответ от DNS для определённого хоста или IP адреса.', 'днс <хост/IP>', ['днс jabber.aq', 'днс 127.0.0.1'])
