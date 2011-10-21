"""
enconf module. by WitcherGeralt (AlKorgun@gmail.com)

BlacSmith bot's module.
Normalize unsupported chat's path to base16.
"""

from os.path import supports_unicode_filenames, sep as os_dsep

AsciiSys = (not supports_unicode_filenames)

del supports_unicode_filenames

from base64 import b16encode as encode_name

__all__ = [
	"AsciiSys",
	"CharCase",
	"AsciiTab",
	"encode_name",
	"cefile",
	"check_nosimbols",
	"encode_filename"
			]

__version__ = "2.5"

CharCase = [
	"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
	"abcdefghijklmnopqrstuvwxyz",
	"0123456789",
	'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
			]

AsciiTab = tuple(str.join("", CharCase))

def cefile(path):
	path = path.replace("\t", "\\t")
	path = path.replace("\n", "\\n")
	path = path.replace("\r", "\\r")
	if (path.count(chr(47)) > 1):
		if not check_nosimbols(path):
			path = encode_filename(path)
	return path

def check_nosimbols(Case):
	if AsciiSys:
		for Char in Case:
			if not AsciiTab.count(Char):
				return False
	return True

def encode_filename(dpath):
	encodedName = []
	for Name in dpath.split(chr(47)):
		At = chr(64)
		if Name.count(At):
			list = Name.split(At, 1)
			chatName = encode_name(list[0].encode("utf-8"))
			encodedName.append("%s@%s" % (chatName[(len(chatName) / 2):], list[1]))
		else:
			encodedName.append(Name)
	return os_dsep.join(encodedName)
