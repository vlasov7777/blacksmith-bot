# /* coding: utf-8 */
# Conference Encoder.
# © WitcherGeralt, modifications by simpleApps

from string import digits
from string import ascii_letters


__exceptions = "-/.@_"
ascii_tab = tuple(digits + ascii_letters + __exceptions)

def chkFile(filename):
	if filename.count("/") > 1:
		if not chkUnicode(filename):
			filename = nameEncode(filename)
	return filename

def chkUnicode(body):
	for symbol in body:
		if symbol not in ascii_tab:
			return False
	return True

def nameEncode(filename):
	from base64 import b16encode
	encodedName = str()
	for name in filename.split("/"):
		if name.count("."):
			if name.count("@"):
				_list = name.split("@", 1)
				chatname = b16encode(_list[0].encode("utf-8"))
				encodedName += "%s@%s/" % (chatname[(len(chatname) / 2):].decode("utf-8"), _list[1])
			else:
				encodedName += name
		else:
			encodedName += u"%s/" % (name)
	del b16encode
	return encodedName
	
del digits, ascii_letters, __exceptions