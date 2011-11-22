# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  userinfa_plugin.py

# Idea:
#  40tman [40tman@qip.ru]
# Cded by:
#  Evgen [meb81@mail.ru]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

USERINFA = {}
IDS_USERINFA = []

def handler_userinfa(conf, nick, afl, role):
	if USERINFA[conf] != 'off' and afl == 'none':
		conf_nick = conf+'/'+nick
		user = handler_jid(conf_nick)
		if user not in ADLIST:
			vcard_iq = xmpp.Iq(to = conf_nick, typ = 'get')
			INFA['outiq'] += 1
			ID = 'userinfa_'+str(INFA['outiq'])
			IDS_USERINFA.append(ID)
			vcard_iq.addChild('vCard', {}, [], 'vcard-temp')
			vcard_iq.setID(ID)
			JCON.SendAndCallForResponse(vcard_iq, handler_userinfa_answer, {'conf': conf,'nick': nick})

def handler_userinfa_answer(coze, stanza, nick, conf):
	ID = stanza.getID()
	if ID in IDS_USERINFA:
		IDS_USERINFA.remove(ID)
		if stanza:
			if stanza.getType() == 'result':
				MASS = stanza.getChildren()
				if MASS:
					repl, nickname, url, email, desc, bday, orgname, orgunit, title, gender, given, family, country, region, locality, street, number, name, to_repl = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', {'&lt;': '<', '&amp;': '&', '&quot;': '"', '&gt;': '>'}
					Props = MASS[0].getChildren()
					for Pr in Props:
						Pr_Name = Pr.getName()
						if Pr_Name == 'NICKNAME':
							nickname = (Pr.getData()).strip()
						elif Pr_Name == 'FN':
							name = (Pr.getData()).strip()
						elif Pr_Name == 'URL':
							url = (Pr.getData()).strip()
						elif Pr_Name == 'EMAIL':
							email = (Pr.getData()).strip()
						elif Pr_Name == 'DESC':
							desc = (Pr.getData()).strip()
						elif Pr_Name == 'BDAY':
							bday = (Pr.getData()).strip()
						elif Pr_Name == 'GENDER':
							gender = (Pr.getData()).strip()
						elif Pr_Name == 'TITLE':
							title = (Pr.getData()).strip()
					Query = unicode(stanza)
					if Query.count('<GIVEN>'):
						given = replace_all(((Query.replace('</GIVEN>', '<GIVEN>')).split('<GIVEN>')[1]), to_repl).strip()
					if Query.count('<FAMILY>'):
						family = replace_all(((Query.replace('</FAMILY>', '<FAMILY>')).split('<FAMILY>')[1]), to_repl).strip()
					if Query.count('<ADR>'):
						ADR = Query.split('<ADR>')
						if len(ADR) >= 2:
							ADR = ADR[1]
							if ADR.count('<COUNTRY>'):
								country = replace_all(((ADR.replace('</COUNTRY>', '<COUNTRY>')).split('<COUNTRY>')[1]), to_repl).strip()
							if ADR.count('<LOCALITY>'):
								locality = replace_all(((ADR.replace('</LOCALITY>', '<LOCALITY>')).split('<LOCALITY>')[1]), to_repl).strip()
							if ADR.count('<REGION>'):
								region = replace_all(((ADR.replace('</REGION>', '<REGION>')).split('<REGION>')[1]), to_repl).strip()
							if ADR.count('<STREET>'):
								street = replace_all(((ADR.replace('</STREET>', '<STREET>')).split('<STREET>')[1]), to_repl).strip()
					if Query.count('<ORGNAME>'):
						orgname = replace_all(((Query.replace('</ORGNAME>', '<ORGNAME>')).split('<ORGNAME>')[1]), to_repl).strip()
					if Query.count('<ORGUNIT>'):
						orgunit = replace_all(((Query.replace('</ORGUNIT>', '<ORGUNIT>')).split('<ORGUNIT>')[1]), to_repl).strip()
					if Query.count('<TEL>'):
						tel = Query.split('<TEL>')
						for item in tel:
							if item.count('</NUMBER><HOME /></TEL>'):
								number = replace_all(((replace_all(item, {'<NUMBER>': '</NUMBER><HOME />', '</NUMBER><HOME /></TEL>': '</NUMBER><HOME />'})).split('</NUMBER><HOME />')[1]), to_repl).strip()
					if name in [family, given, '%s %s' % (given, family), '%s %s' % (family, given)]:
						name = ''
					if name:
						repl += u'\nИмя: '+name
					if nickname:
						repl += u'\nПсевдоним: '+nickname
					if given or family:
						repl += u'\nПолное имя: '+((given+' '+family).strip())
					if email:
						repl += u'\nEmail: '+email
					if country:
						repl += u'\nСтрана: '+country
					if region:
						repl += u'\nРегион: '+region
					if locality:
						repl += u'\nГород: '+locality
					if street:
						repl += u'\nАдрес: '+street
					if number:
						repl += u'\nТелефон: '+number
					if orgname:
						repl += u'\nКомпания: '+orgname
					if orgunit:
						repl += u'\nОтдел: '+orgunit
					if title:
						repl += u'\nДолжность: '+title
					if gender:
						gender = gender.lower()
						if gender == 'male':
							repl += u'\nПол: Мужской'
						if gender == 'female':
							repl += u'\nПол: Женский'
					if bday:
						repl += u'\nДнюха: '+bday
					if url:
						repl += u'\nСайт: '+url
					if desc:
						repl += u'\nИнфа: '+desc
					if repl != '':
						msg(conf, u'У нас новый участник '+nick+'!'+repl)

def handler_userinfa_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/userinfa.txt'
			if body in [u'вкл', 'on', '1']:
				USERINFA[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'Информация о новичках включена')
			elif body in [u'выкл', 'off', '0']:
				USERINFA[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'Информация о новичках отключена')
			else:
				reply(type, source, u'читай помощь по команде')
		elif USERINFA[source[1]] == 'off':
			reply(type, source, u'Информация о новичках отключена')
		else:
			reply(type, source, u'Информация о новичках включена')
	else:
		reply(type, source, u'только в чате мудак!')

def userinfa_init(conf):
	if check_file(conf, 'userinfa.txt', "'off'"):
		state = eval(read_file('dynamic/'+conf+'/userinfa.txt'))
	else:
		state = 'off'
		delivery(u'Внимание! Не удалось создать userinfa.txt для "%s"!' % (conf))
	USERINFA[conf] = state

register_join_handler(handler_userinfa)
command_handler(handler_userinfa_control, 20, "userinfa")

register_stage1_init(userinfa_init)
