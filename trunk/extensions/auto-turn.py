# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  auto_turn_plugin.py
#  Ver.5.1

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,.Ю`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>Б~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,.ю`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>б~"))
OBSCENE2 = u'бляд/ блят/ бля / блять / плять /хуй/ ибал/ ебал/ хуи/хуител/хуя/ хую/ хуе/ ахуе/ охуе/хуев/ хер /хер/ пох / нах /писд/пизд/рizd/ пздц / еб/ епана / епать / ипать / выепать / ибаш/ уеб/проеб/праеб/приеб/съеб/взъеб/взьеб/въеб/вьеб/выебан/перееб/недоеб/долбоеб/долбаеб/ ниибац/ неебац/ неебат/ ниибат/ пидар/ рidаr/ пидар/ пидор/педор/пидор/пидарас/пидараз/ педар/педри/пидри/ заеп/ заип/ заеб/ебучий/ебучка /епучий/епучка / заиба/заебан/заебис/ выеб/выебан/ поеб/ наеб/ наеб/сьеб/взьеб/вьеб/ гандон/ гондон/пахуи/похуис/ манда /мандав/залупа/ залупог'
SMILES = u''':Wooden Snivel:4*O:-)4*O=)4*:-)4*:)4*=)4*:-(4*:(4*;(4*;-)4*;)4*:-P4*8-)4*:-D4*:-[4*=-O4*:-*4*:-X4*:-x4*>:o4*:-|4*:-/4**JOKINGLY*4*]:->4*[:-}4**KISSED*4*:-!4**TIRED*4**STOP*4**KISSING*4*@}->--4**THUMBS UP*4**DRINK*4**IN LOVE*4*@=4**HELP*4*\m/4*%)4**OK*4**WASSUP*4**SUP*4**SORRY*4**BRAVO*4**ROFL*4**LOL*4**PARDON*4**NO*4**CRAZY*4**DONT_KNOW*4**UNKNOWN*',u'*DANCE*4**YAHOO*4**YAHOO!*4**HI*4**PREVED*4**PRIVET*4**HELLO*4**BYE*4**YES*4*;D4**ACUTE*4**WALL*4**DASH*4**WRITE*4**MAIL*4**SCRATCH*4**SECRET*4**secret*4**SECRET*',  u'*jokingly*4*:JOKINGLY:4*:jokingly:4**dntknw*4*:lol:4*:LOL:4*LOL4*lol4*ROTFL4*:P4*:p4*=P4**HM*4**hm*4*:HM:4*:hm:4**yes*4**YES*4**HAPPY*4**nose*4**horror*4*=:OO4*=;OO4*=:oOO4*(ok)4*(OK)4**ok*4**OK*4*:-O4*=-O4*:-o4*:O4*=:-O4*=:-o4*=O4*:-04*@}->-4*@};-4*(F)4*(f)4**BOUQUET*4*8(4*8-D4*3-|{4*;-|4**ermm*4*8-|4**ZAWTOROJ*4**LICK*4**FOOD*4**SMOKE*4*:-S',  u'<]4*:-@4**BOTAN*4*|-)4**STOP*4*>:-(4**RTFM*4**crazy*4**help*4**FUCK*4**FIGA*4**VICTORY*4*>:P4*:-?4**reads*4*:-]4*:-[4*:apple:'''
ATURN = {}

def check_obscene_words(body):
	body = ' %s ' % body.lower()
	for item in OBSCENE2.split('/'):
		if body.count(item):
			return True
	return False

def check_nosimbols__(Case):
	for Char in Case:
		if not ascii_tab.count(Char):
			return False
	return True

def handler_aturn(raw, type, source, body):
	if type == 'public' and source[2] != '':
		if ATURN[source[1]] != 'off':
			list = {}
			for nick in GROUPCHATS[source[1]].keys():
				if GROUPCHATS[source[1]][nick]['ishere']:
					for key in [nick+key for key in [':',',','>']]:
						if body.count(key):
							col = '*%s*' % str(len(list.keys()) + 1)
							list[col] = key
							body = body.replace(key, col)
				if body.count(nick):
					col2 = '*%s*' % str(len(list.keys()) + 1)
					list[col2] = nick
					body = body.replace(nick, col2)
			if check_nosimbols__(body):
				rebody2 = replace_all(body, list.keys(), '').strip()
				if rebody2 and not check_number(rebody2) and rebody2 not in SMILES.split('4*'):
					rebody = reduce(lambda x,y: en2ru_table.get(x,x)+en2ru_table.get(y,y), body)
					if not check_obscene_words(rebody):
						rebody = replace_all(rebody, list)
						msg(source[1], u'авто-turn\->\n%s» %s' % (source[2], rebody))
					else:
						reply(type, source, u'хрена ругаешся!?')

def handler_aturn_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/%s/aturn.txt' % (source[1])
			if body in [u'вкл', 'on', '1']:
				ATURN[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'авто-турн включен')
			elif body in [u'выкл', 'off', '0']:
				ATURN[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'авто-турн выключен')
			else:
				reply(type, source, u'читай помощь по команде')
		elif ATURN[source[1]] == 'off':
			reply(type, source, u'сейчас авто-turn выключен')
		else:
			reply(type, source, u'сейчас авто-turn включен')
	else:
		reply(type, source, u'только в чате мудак!')

def aturn_init(conf):
	if check_file(conf, 'aturn.txt', "'off'"):
		ATURN[conf] = eval(read_file('dynamic/%s/aturn.txt' % (conf)))
	else:
		ATURN[conf] = 'off'
		delivery(u'Внимание! Не удалось создать aturn.txt для "%s"!' % (conf))

register_message_handler(handler_aturn)
command_handler(handler_aturn_control, 20, "auto-turn")

register_stage1_init(aturn_init)
