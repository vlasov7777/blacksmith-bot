# /* encoding: utf-8 */
# Copyright sTools © simpleApps CodingTeam (Tue Oct 13 22:14:13 2011)
# This program published under GPL v3 license
# See LICENSE.GPL for more details

## ZLIB.
def ZLIBEncoder(__x__):
	try:
		if type(__x__) != str:
			return type(__x__)(repr(x.encode("zlib")) for x in __x__)
		return repr(__x__.encode("zlib"))
	except:
		crashlog("ZLIBEncoder")
		return __x__
		
def ZLIBDecoder(__x__):
	try:
		if type(__x__) != str:
			return type(__x__)(repr(x.decode("zlib")) for x in __x__)
		return repr(__x__.decode("zlib"))
	except:
		crashlog("ZLIBDecoder")
		return __x__

# OS.
def getArchitecture():
	from struct import calcsize
	is_amd64 = (calcsize("P") is 8)
	if is_amd64:
		return "[amd64]"
	elif calcsize("P") != 4:
		from platform import processor
		return processor()
	return "[i386]"

def ntDetect():
	try:
		from os import popen
		pipe = popen("ver")
		osMain = pipe.read()
		try: osMain = osMain.decode("cp866")
		except: pass
		pipe.close()
	except:
		crashlog("ntDetect")
		osMain = "NT"
	del popen
	return osMain