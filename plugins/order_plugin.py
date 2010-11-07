#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  order_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

OBSCENE = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']
ORDERS = {'time': 1, 'presence': 1, 'len': 1, 'like': 0, 'caps': 0, 'prsstlen': 1, 'obscene': 0, 'excess': {'cond': 0, 'mode': 'kick'}, 'kicks': {'cond': 1, 'cnt': 2}, 'fly': {'cond': 1, 'mode': 'ban', 'time': 60}, 'idle': {'cond': 0, 'time': 3600}}

ORDER_STATS = {}
ORDER = {}

def order_check_obscene_words(body):
	body = body.lower()
	for item in OBSCENE:
		if body.count(item):
			return True
	return False

def order_check_time_flood(conf, jid, nick):
	lastmsg = ORDER_STATS[conf][jid]['msgtime']
	if lastmsg and time.time() - lastmsg <= 2.2:
		ORDER_STATS[conf][jid]['msg'] += 1
		if ORDER_STATS[conf][jid]['msg'] > 3:
			ORDER_STATS[conf][jid]['devoice']['time'] = time.time()
			ORDER_STATS[conf][jid]['devoice']['cnd'] = 1
			ORDER_STATS[conf][jid]['msg'] = 0
			handler_kick(conf, nick, u'слишком быстро отправляешь')
			return True
		return False

def order_check_len_flood(mlen, body, conf, jid, nick):
	if len(body) > mlen:
		ORDER_STATS[conf][jid]['devoice']['time'] = time.time()
		ORDER_STATS[conf][jid]['devoice']['cnd'] = 1
		handler_kick(conf, nick, u'флуд')
		return True
	return False

def order_check_obscene(body, conf, jid, nick):
	if order_check_obscene_words(body):
		ORDER_STATS[conf][jid]['devoice']['time'] = time.time()
		ORDER_STATS[conf][jid]['devoice']['cnd'] = 1
		handler_kick(conf, nick, u'нецензурно')
		return True
	return False

def order_check_caps(body, conf, jid, nick):
	for x in GROUPCHATS[conf]:
		if body.count(x):
			body = body.replace(x,'')
	col = 0
	for x in [x for x in body.replace(' ','')]:
		if x.isupper():
			col += 1
	if col >= len(body)/2 and col > 9:
		ORDER_STATS[conf][jid]['devoice']['time'] = time.time()
		ORDER_STATS[conf][jid]['devoice']['cnd'] = 1
		handler_kick(conf, nick, u'слишком много капса')
		return True
	return False

def order_check_like(body, conf, jid, nick):
	lcnt = 0
	lastmsg = ORDER_STATS[conf][jid]['msgtime']
	if lastmsg and ORDER_STATS[conf][jid]['msgbody']:
		if time.time() - lastmsg > 60:
			ORDER_STATS[conf][jid]['msgbody'] = body.split()
		else:
			for x in ORDER_STATS[conf][jid]['msgbody']:
				for y in body.split():
					if x == y:
						lcnt += 1
			if lcnt:
				lensrcmsgbody = len(body.split())
				lenoldmsgbody = len(ORDER_STATS[conf][jid]['msgbody'])
				avg = (lensrcmsgbody+lenoldmsgbody /2 )/ 2
				if lcnt > avg:
					ORDER_STATS[conf][jid]['msg'] += 1
					if ORDER_STATS[conf][jid]['msg'] >= 2:
						ORDER_STATS[conf][jid]['devoice']['time'] = time.time()
						ORDER_STATS[conf][jid]['devoice']['cnd'] = 1
						ORDER_STATS[conf][jid]['msg'] = 0
						handler_kick(conf, nick, u'мессаги слишком похожи')
						return True
			ORDER_STATS[conf][jid]['msgbody'] = body.split()
	else:
		ORDER_STATS[conf][jid]['msgbody'] = body.split()
	return False

def order_check_idle():
	for conf in ORDER:
		if ORDER[conf]['idle']['cond'] == 1:
			timee = ORDER[conf]['idle']['time']
			now = time.time()
			for nick in GROUPCHATS[conf]:
				if GROUPCHATS[conf][nick]['ishere']:
					if user_level(conf+'/'+nick, conf) <= 10:
						idle = now - GROUPCHATS[conf][nick]['idle']
						if idle > timee:
							handler_kick(conf, nick, u'молчание более '+timeElapsed(idle))
	try:
		threading.Timer(120, order_check_idle).start()
	except:
		LAST['null'] += 1

def handler_order_message(raw, type, source, body):
	if source[1] in GROUPCHATS and user_level(source[0], source[1]) <= 10:
		if source[2] != '':
			jid = handler_jid(source[0])
			if source[1] in ORDER_STATS and jid in ORDER_STATS[source[1]]:
				if ORDER[source[1]]['time'] == 1:
					if order_check_time_flood(source[1], jid, source[2]):
						return
				if ORDER[source[1]]['len'] == 1:
					if order_check_len_flood(900, body, source[1], jid, source[2]):
						return
				if ORDER[source[1]]['obscene'] == 1:
					if order_check_obscene(body, source[1], jid, source[2]):
						return
				if ORDER[source[1]]['caps'] == 1:
					if order_check_caps(body, source[1], jid, source[2]):
						return
				if ORDER[source[1]]['like'] == 1:
					if order_check_like(body, source[1], jid, source[2]):
						return
				ORDER_STATS[source[1]][jid]['msgtime'] = time.time()

def handler_order_join(conf, nick, afl, role):
	jid = handler_jid(conf+'/'+nick)
	if nick in GROUPCHATS[conf] and user_level(conf+'/'+nick, conf) <= 10:
		now = time.time()
		if conf not in ORDER_STATS:
			ORDER_STATS[conf] = {}
		if jid in ORDER_STATS[conf]:
			if ORDER_STATS[conf][jid]['devoice']['cnd'] == 1:
				if now-ORDER_STATS[conf][jid]['devoice']['time'] > 300:
					ORDER_STATS[conf][jid]['devoice']['cnd'] = 0
				else:
					handler_visitor(conf, nick, u'право голоса снято за предыдущие нарушения')
			if ORDER[conf]['kicks']['cond'] == 1:
				kcnt = ORDER[conf]['kicks']['cnt']
				if ORDER_STATS[conf][jid]['kicks'] > kcnt:
					handler_ban(conf, nick, u'слишком много киков')
					return
			if ORDER[conf]['fly']['cond'] == 1:
				lastprs = ORDER_STATS[conf][jid]['prstime']['fly']
				ORDER_STATS[conf][jid]['prstime']['fly'] = time.time()
				if now - lastprs <= 70:
					ORDER_STATS[conf][jid]['prs']['fly'] += 1
					if ORDER_STATS[conf][jid]['prs']['fly'] > 4:
						ORDER_STATS[conf][jid]['prs']['fly'] = 0
						fmode = ORDER[conf]['fly']['mode']
						ftime = ORDER[conf]['fly']['time']
						if fmode == 'ban':
							handler_ban(conf, nick, u'хватит летать')
							time.sleep(ftime)
							handler_unban(conf, jid)
						else:
							handler_kick(conf, nick, u'хватит летать')
							return
				else:
					ORDER_STATS[conf][jid]['prs']['fly'] = 0
			if ORDER[conf]['obscene'] == 1:
				if order_check_obscene(nick, conf, jid, nick):
					return
			if ORDER[conf]['len'] == 1:
				if order_check_len_flood(20, nick, conf, jid, nick):
					return
		elif nick in GROUPCHATS[conf]:
			ORDER_STATS[conf][jid] = {'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}
	elif conf in ORDER_STATS and jid in ORDER_STATS[conf]:
		del ORDER_STATS[conf][jid]

def handler_order_presence(Prs):
	ptype = Prs.getType()
	if ptype != 'unavailable' and ptype != 'error':
		conf = Prs.getFrom().getStripped()
		if conf not in ORDER_STATS:
			ORDER_STATS[conf] = {}
		nick = Prs.getFrom().getResource()
		stmsg = Prs.getStatus()
		jid = handler_jid(conf+'/'+nick)
		afl = Prs.getAffiliation()
		role = Prs.getRole()
		if jid in ORDER_STATS[conf] and afl in ['member','admin','owner']:
			del ORDER_STATS[conf][jid]
		elif jid not in ORDER_STATS[conf]:
			ORDER_STATS[conf][jid] = {'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}
		if jid in ORDER_STATS[conf]:
			if user_level(conf+'/'+nick, conf) <= 10:
				now = time.time()
				if now - GROUPCHATS[conf][nick]['joined'] > 1:
					if role == 'participant':
						ORDER_STATS[conf][jid]['devoice']['cnd'] = 0
					lastprs = ORDER_STATS[conf][jid]['prstime']['status']
					ORDER_STATS[conf][jid]['prstime']['status'] = now
					if ORDER[conf]['presence'] == 1:
						if now-lastprs > 300:
							ORDER_STATS[conf][jid]['prs']['status'] = 0
						else:
							ORDER_STATS[conf][jid]['prs']['status'] += 1
							if ORDER_STATS[conf][jid]['prs']['status'] > 5:
								ORDER_STATS[conf][jid]['prs']['status'] = 0
								handler_kick(conf, nick, u'презенс-флуд')
								return
					if ORDER[conf]['obscene']:
						if order_check_obscene(nick, conf, jid, nick):
							return
					if stmsg and ORDER[conf]['prsstlen']:
						if order_check_len_flood(200, nick, conf, jid, nick):
							return

def handler_order_leave(conf, nick, reason, code):
	jid = handler_jid(conf+'/'+nick)
	if user_level(conf+'/'+nick, conf) <= 10:
		if conf in ORDER_STATS and jid in ORDER_STATS[conf]:
			if ORDER[conf]['presence'] == 1:
				if reason == 'Replaced by new connection':
					return
				if code:
					if code == '307':
						ORDER_STATS[conf][jid]['kicks'] += 1
						return
					elif code == '301':
						del ORDER_STATS[conf][jid]
						return
					elif code == '407':
						return
			if ORDER[conf]['fly']['cond'] == 1:
				now = time.time()
				lastprs = ORDER_STATS[conf][jid]['prstime']['fly']
				ORDER_STATS[conf][jid]['prstime']['fly'] = time.time()
				if now-lastprs <= 70:
					ORDER_STATS[conf][jid]['prs']['fly'] += 1
				else:
					ORDER_STATS[conf][jid]['prs']['fly'] = 0

def handler_order_filt(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			if args[0] == 'time':
				if args[1] == '0':
					reply(type, source, u'временная фильтрация сообщений отключена')
					ORDER[source[1]]['time'] = 0
				elif args[1] == '1':
					reply(type, source, u'временная фильтрация сообщений включена')
					ORDER[source[1]]['time'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'presence':
				if args[1] == '0':
					reply(type, source, u'временная фильтрация презенсов отключена')
					ORDER[source[1]]['presence'] = 0
				elif args[1] == '1':
					reply(type, source, u'временная фильтрация презенсов включена')
					ORDER[source[1]]['presence'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'len':
				if args[1] == '0':
					reply(type, source, u'фильтрация длинных сообщений отключена')
					ORDER[source[1]]['len'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтрация длинных сообщений включена')
					ORDER[source[1]]['len'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'like':
				if args[1] == '0':
					reply(type, source, u'фильтрация подозрительно одинаковых сообщений отключена')
					ORDER[source[1]]['like'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтрация подозрительно одинаковых сообщений включена')
					ORDER[source[1]]['like'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'caps':
				if args[1] == '0':
					reply(type, source, u'фильтрация капса отключена')
					ORDER[source[1]]['caps'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтрация капса включена')
					ORDER[source[1]]['caps'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'prsstlen':
				if args[1] == '0':
					reply(type, source, u'фильтрация длинных статусных сообщений отключена')
					ORDER[source[1]]['prsstlen'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтрация длинных статусных сообщений включена')
					ORDER[source[1]]['prsstlen'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'obscene':
				if args[1] == '0':
					reply(type, source, u'фильтрация мата отключена')
					ORDER[source[1]]['obscene'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтрация мата включена')
					ORDER[source[1]]['obscene'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'fly':
				if args[1] == 'cnt':
					if check_number(args[2]):
						if int(args[2]) in xrange(0, 121):
							reply(type, source, u'разморозка установлена на '+args[2]+u' секунд')
							ORDER[source[1]]['fly']['time'] = int(args[2])
						else:
							reply(type, source, u'не более двух минут (120 секунд)')
					else:
						reply(type, source, u'синтакс инвалид')
				elif args[1] == 'mode':
					if args[2] in ['kick','ban']:
						if args[2] == 'ban':
							reply(type, source, u'за полёты будем банить')
							ORDER[source[1]]['fly']['mode'] = 'ban'
						else:
							reply(type, source, u'за полёты будем кикать')
							ORDER[source[1]]['fly']['mode'] = 'kick'
					else:
						reply(type, source, u'синтакс инвалид')
				elif args[1] == '0':
					reply(type, source, u'фильтр полётов отключен')
					ORDER[source[1]]['fly']['cond'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтр полётов включен')
					ORDER[source[1]]['fly']['cond'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'kicks':
				if args[1] == 'cnt':
					if check_number(args[2]):
						if int(args[2]) in xrange(2, 10):
							reply(type, source, u'автобан после '+args[2]+u' киков')
							ORDER[source[1]]['kicks']['cnt'] = int(args[2])
						else:
							reply(type, source, u'от 2 до 10 киков')
					else:
						reply(type, source, u'синтакс инвалид')
				elif args[1] == '0':
					reply(type, source, u'фильтр автобана после нескольких киков отключен')
					ORDER[source[1]]['kicks']['cond'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтр автобана после нескольких киков включен')
					ORDER[source[1]]['kicks']['cond'] = 1
				else:
					reply(type, source, u'синтакс инвалид')
			elif args[0] == 'idle':
				if args[1] == 'time':
					if check_number(args[2]):
						reply(type, source, u'кик за молчание после '+args[2]+u' секунд ('+timeElapsed(int(args[2]))+u')')
						ORDER[source[1]]['idle']['time'] = int(args[2])
					else:
						reply(type, source, u'синтакс инвалид')
				elif args[1] == '0':
					reply(type, source, u'фильтр кика за молчание отключен')
					ORDER[source[1]]['idle']['cond'] = 0
				elif args[1] == '1':
					reply(type, source, u'фильтр кика за молчание включен')
					ORDER[source[1]]['idle']['cond'] = 1
			else:
				reply(type, source, u'синтакс инвалид')
			write_file('dynamic/'+source[1]+'/order.txt', str(ORDER[source[1]]))
		else:
			reply(type, source, u'синтакс инвалид')
	else:
		repl, foff, fon = '', [], []
		time = ORDER[source[1]]['time']
		prs = ORDER[source[1]]['presence']
		flen = ORDER[source[1]]['len']
		like = ORDER[source[1]]['like']
		caps = ORDER[source[1]]['caps']
		prsstlen = ORDER[source[1]]['prsstlen']
		obscene = ORDER[source[1]]['obscene']
		fly = ORDER[source[1]]['fly']['cond']
		flytime = str(ORDER[source[1]]['fly']['time'])
		flymode = ORDER[source[1]]['fly']['mode']
		kicks = ORDER[source[1]]['kicks']['cond']
		kickscnt = str(ORDER[source[1]]['kicks']['cnt'])
		idle = ORDER[source[1]]['idle']['cond']
		idletime = ORDER[source[1]]['idle']['time']
		if time:
			fon.append(u'временная фильтрация сообщений')
		else:
			foff.append(u'временная фильтрация сообщений')
		if prs:
			fon.append(u'временная фильтрация презенсов')
		else:
			foff.append(u'временная фильтрация презенсов')
		if flen:
			fon.append(u'фильтрация длинных сообщений')
		else:
			foff.append(u'фильтрация длинных сообщений')
		if like:
			fon.append(u'фильтрация подозрительно одинаковых сообщений')
		else:
			foff.append(u'фильтрация подозрительно одинаковых сообщений')
		if caps:
			fon.append(u'фильтрация капса')
		else:
			foff.append(u'фильтрация капса')
		if prsstlen:
			fon.append(u'фильтрация длинных статусных сообщений')
		else:
			foff.append(u'фильтрация длинных статусных сообщений')
		if obscene:
			fon.append(u'фильтрация мата')
		else:
			foff.append(u'фильтрация мата')
		if fly:
			fon.append(u'фильтр полётов (режим '+flymode+u', таймер '+flytime+u' секунд)')
		else:
			foff.append(u'фильтр полётов')
		if kicks:
			fon.append(u'автобан после '+kickscnt+u' киков')
		else:
			foff.append(u'автобан после нескольких киков')
		if idle:
			fon.append(u'кик за молчание через '+str(idletime)+u' секунд ('+timeElapsed(idletime)+u')')
		else:
			foff.append(u'кик за молчание')
		fon = ', '.join(fon)
		if fon:
			repl += u'ВКЛЮЧЕНЫ\n'+fon+'\n\n'
		foff = ', '.join(foff)
		if foff:
			repl += u'ВЫКЛЮЧЕНЫ\n'+foff
		reply(type, source, repl.strip())

def order_init(conf):
	if check_file(conf, 'order.txt', str(ORDERS)):
		config = eval(read_file('dynamic/'+conf+'/order.txt'))
	else:
		config = ORDERS
		delivery(u'Внимание! Не удалось создать order.txt для "%s"!' % (conf))
	ORDER[conf] = config

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'бодигард', ['админ','все'], 20, 'Включает или отключает определённые фильтры для конференции.\ntime - временной фильтр\nlen - количественный фильтр\npresence - фильтр презенсов\nlike - фильтр одинаковых сообщений\ncaps - фильтр капса (ЗАГЛАВНЫХ букв)\nprsstlen - фильтр длинных статусных сообщений\nobscene - фильтр матов\nfly - фильтр полётов (частых входов/выходов в конмату), имеет два режима ban и kick, таймер от 0 до 120 секунд\nkicks - автобан после N киков, параметр cnt - количество киков от 1 до 10\nidle - кик за молчание в общем чате после N секунд, параметр time - кол-во секунд для срабатывания', 'бодигард [фильтр] [режим] [состояние]', ['бодигард smile 1', 'бодигард len 0','бодигард fly mode ban'])

register_stage1_init(order_init)
register_stage2_init(order_check_idle)
