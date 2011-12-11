# BS mark.1
# /* coding: utf-8 */
# Author: WithcerGeralt
# Ported from BlackSmith m.2 
# (c) simpleApps, 2011

compile_st = re.compile("<[^<>]+?>")

def e_sb(co):
	co = co.groups()[0]
	if co.startswith("#"):
		if chr(120) == co[1].lower():
			Char, c06 = co[2:], 16
		else:
			Char, c06 = co[1:], 10
		try:
			Numb = int(Char, c06)
			assert (-1 < Numb < 65535)
			Char = unichr(Numb)
		except:
			Char = edefs.get(Char, "&%s;" % co)
	else:
		Char = edefs.get(co, "&%s;" % co)
	return Char

def get_text(body, s0, s2, s1 = "(?:.|\s)+"):
	comp = re.compile("%s(%s?)%s" % (s0, s1, s2), 16)
	body = comp.search(body)
	if body:
		body = (body.group(1)).strip()
	return body

def decodeHTML(data):
	data = compile_st.sub("", data)
	data = uHTML(data)
	return data.strip()

def gismeteo(mType, source, body):
	if body:
		ls = body.split()
		Numb = ls.pop(0)
		if ls and Numb.isdigit():
			City = body[(body.find(Numb) + len(Numb) + 1):].strip()
			Numb = int(Numb)
		else:
			Numb, City = (None, body)
		if -1 < Numb < 13 or not Numb:
			try:
				data = read_url("http://m.gismeteo.ru/citysearch/by_name/?" +\
									 urlencode({"gis_search": City.encode("utf-8")}), uagent)
			except:
				answer = u"Не могу получить доступ к странице."
			else:
				data = data.decode("utf-8")
				data = data = get_text(data, "<a href=\"/weather/", "/(1/)*?\">", "\d+")
				if data:
					if Numb != None:
						data = str.join(chr(47), [data, str(Numb) if Numb != 0 else "weekly"])
					try:
						data = read_url("http://m.gismeteo.ru/weather/%s/" % data, uagent)
					except:
						answer = u"Не могу получить доступ к странице."
					else:
						data = data.decode("utf-8")
						mark = get_text(data, "<th colspan=\"2\">", "</th>")
						if Numb != 0:
							comp = re.compile('<tr class="tbody">\s+?<th.*?>(.+?)</th>\s+?<td.+?/></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>\s+?</tr>\s+?<tr class="dl">\s+?<td>&nbsp;</td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl bottom"><td class="left">(.+?)</td><td>(.+?)</td></tr>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("{0}:\n\t{2}, {1}\n\t{3} {4}\n\t{5} {6}\n\t{7} {8}".format(*data))
								answer = decodeHTML(str.join(chr(10), ls)) + "\n*** Погода предоставлена сайтом GisMeteo.ru"
							else:
								answer = AllwebAnsBase[1]
						else:
							comp = re.compile('<tr class="tbody">\s+?<td class="date" colspan="3"><a.+?>(.+?)</a></td>\s+?</tr>\s+?<tr>\s+?<td rowspan="2"><a.+?/></a></td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("{0}:\n\t{1}, {2}".format(*data))
								answer = decodeHTML(str.join(chr(10), ls)) + "\n*** Погода предоставлена сайтом GisMeteo.ru"
							else:
								answer = u"Проблемы с разметкой..."
				else:
					answer = u"Ничего не найдено..."
		else:
			answer = "SyntaxError: Invalid Syntax"
	else:
		answer = u"Недостаточно параметров."
	reply(mType, source, answer)

command_handler(gismeteo, 10, "gismeteo")