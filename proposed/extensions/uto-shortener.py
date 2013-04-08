# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
# Copyright Url Shortener (by service u.to) © simpleApps CodingTeam (Fri Oct 28 18:54:26 2011)
# This program published under Apache 2.0 license
# See LICENSE.txt for more details

#-extmanager-extVer:2.0-#

def uto_parse(code):
  data = re.search("#shurlout'\)\.val\('(.*)'\)\.show\(\)\.focus\(\)", code)
  if data:
	data = data.group(1)
  return data

def url_shortener(mType, source, args):
	if args:
		if not chkUnicode(args):
			args = IDNA(args)
		headers = {"Accept": "application/xml, text/xml */*",
				   "Accept-Language": "ru-ru,ru; q=0.5",
				   "Accept-Encoding": "deflate",
				   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				   "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:21.0) Gecko/20130309 Firefox/21.0"}
		data = urllib.urlencode(dict(a = "add", url = args))
		request = urllib2.Request("http://u.to/", data, headers)
		resp = urllib2.urlopen(request)
		answer = uto_parse(resp.read()) or u"Какая-то проблема с получением результата." 
	else:
		answer = u"Не нашёл URL."
	reply(mType, source, answer)

command_handler(url_shortener, 11, "uto-shortener")
