#!/usr/bin/python
# -*- coding: utf-8 -*-

#  BlackSmith module
#  enconf.py

# Author: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

RUSIMBOLS = 'а/б/в/г/д/е/ё/ж/з/и/й/к/л/м/н/о/п/р/с/т/у/ф/х/ц/ч/ы/ъ/ь/ш/щ/э/ю/я/№'.decode('utf-8')

from base64 import b64encode as encode_conf

def check_nosimbols(item):
	item = item.lower()
	for simbol in RUSIMBOLS.split('/'):
		if item.count(simbol):
			return False
	return True

def encode_filename(filename):
	return_filename = ''
	for name in filename.split('/'):
		if name.count('.'):
			if name.count('@'):
				splname = name.split('@')
				chatname = encode_conf(splname[0].encode('utf-8'))
				return_filename += chatname[(len(chatname) / 2):].decode('utf-8')+'@'+splname[1]+'/'
			else:
				return_filename += name
		else:
			return_filename += name+'/'
	return return_filename
