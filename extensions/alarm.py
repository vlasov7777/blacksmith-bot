# BS mark.1
# /* coding: utf-8 */
# (c) simpleApps, 2011.
# Idea (c) WitcherGeralt, 2010 - 2011.

ALARM_FILE = 'dynamic/alarm.txt'
ALARM_LIST = {}

def alarmConfig(mType, source, text):
	if len(text) <= 256:
		jid = handler_jid(source[0])
		args = text.strip().split() or chr(32) * 2
		if args[0] == "+":
			data = text[(text.find(chr(32)) + 1):].strip()
			if not ALARM_LIST.get(jid):
				ALARM_LIST[jid] = list()
			if jid not in ADLIST and len(ALARM_LIST[jid]) > 5:
				reply(mType, source, u"Лимит напомниналок исчерпан!")
				return
			if text not in ALARM_LIST:
				ALARM_LIST[jid].append(data)
				answer = u"Добавил под номером %i." % len(ALARM_LIST[jid])
			else:
				answer = u"Такая напоминалка уже есть. Номер: %i." % ALARM_LIST[jid].index(data)
		elif args[0] == "-":
			if args[1].isdigit() and len(ALARM_LIST.get(jid, "")) > (int(args[1]) - 1) and int(args[1]) > 0:
				ALARM_LIST[jid].remove(ALARM_LIST[jid][int(args[1]) - 1])
				answer = u"Удалил запись под номером %s." % args[1]
			else:
				answer = u"Либо «%s» не число, либо нет записи с таким номером." % args[1]
		elif args[0] == u"очистить":
			if ALARM_LIST.get(jid):
				ALARM_LIST[jid] = list()
				answer = u"Очищено."
			else:
				answer = u"Пусто."
		else:
			answer = "\n"
			if ALARM_LIST.get(jid):
				for x, y in enumerate(ALARM_LIST[jid]):
					answer +=  u"%i. %s.\n" % (x + 1, y)
			else:
				answer = u"На тебя нет ничего."
		write_file(ALARM_FILE, str(ALARM_LIST))
		reply(mType, source, answer)

def alarmWork(chat, nick, afl, role):
	jid = handler_jid(chat+'/'+nick)
	answer = "\nНапоминаю: "
	if ALARM_LIST.get(jid):
		for x, y in enumerate(ALARM_LIST[jid]):
			answer +=  u"%i. %s.\n" % (x + 1, y)
		msg(chat + "/" + nick, answer)

def alarmInit():
	if initialize_file(ALARM_FILE):
		globals()["ALARM_LIST"] = eval(read_file(ALARM_FILE))
	else:
		Print('\n\nError: can`t create alarm.txt!', color2)

register_join_handler(alarmWork)
command_handler(alarmConfig, 10, "alarm")
register_stage0_init(alarmInit)
