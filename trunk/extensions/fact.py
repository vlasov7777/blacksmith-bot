#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  fact_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

TLD_FILE = 'static/tlds.txt'

def fact_tld(query):
	fl = open(TLD_FILE, 'r')
	while True:
		line = fl.readline()
		if not line:
			return u'не нашёл'
		(key, value) = line.split(': ', 1)
		if query.lower().strip() == key.lower().strip():
			return value.strip()

def handler_fact_tld(type, source, body):
	reply(type, source, fact_tld(body))

command_handler(handler_fact_tld, 10, "fact")
