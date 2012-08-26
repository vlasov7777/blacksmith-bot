# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  distance_pugin.py

# © Evgen
# Modifications © mrDoctorWho

Site = "http://www.ati.su/Trace/default.aspx?EntityType=Trace&%s&%s&WithinCountry=false"

def Distance(type, source, body):
	try:
		body = body.encode("utf-8").split()
		if len(body)<2:
			reply(type, source, u'смотри хелп!')
			return
		data = read_url(Site % (urlencode({"City1": body[0]}),
									  urlencode({"City5": body[1]})))
		data = data.decode('windows-1251')
		data1 = data.split('<input name="ctl00$ctl00$main$PlaceHolderMain$City1$TextBox" type="text" value="')
		data1 = data1[1].split('" id="ctl00_ctl00_main_PlaceHolderMain_City1_TextBox" autocomplete="off"')
		data2 = data.split('<input name="ctl00$ctl00$main$PlaceHolderMain$City5$TextBox" type="text" value="')
		data2 = data2[1].split('" id="ctl00_ctl00_main_PlaceHolderMain_City5_TextBox" autocomplete="off"')
		if not data.count('<span id="ctl00_ctl00_main_PlaceHolderMain_atiTrace_lblTotalDistance">'):
			reply(type,source,u'расстояние не определено')
			return
		od = re.search('<span id="ctl00_ctl00_main_PlaceHolderMain_atiTrace_lblTotalDistance">',data)
		h = data[od.end():]
		h1 = h[:re.search('</font>',h).start()]
		h1=h1.replace('&nbsp;', ' ')
		h2 = u"Расстояние «%s» ― «%s» %s" % (data1[0], data2[0], h1)
		od = re.search('<span id="ctl00_ctl00_main_PlaceHolderMain_atiTrace_lblTotalTime">',h)
		h = h[od.end():]
		h1 = h[:re.search('</span>',h).start()]
		reply(type, source, u"%s Время в пути: %s" % (h2.replace("</span>",""), h1))
	except Exception, e:
		reply(type, source, `e`)

command_handler(Distance, 11, "distance")
