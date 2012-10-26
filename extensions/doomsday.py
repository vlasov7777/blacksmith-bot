# BS mark.1-55
# /* coding: utf-8 */

#  © WitcherGeralt

def command_apocalypse(mType, source, body):
		Time = time.gmtime()
		t1 = (356 - Time.tm_yday) 
		if not t1:
			answer = "We all gonna die today! | Сегодня мы все умрём!"
		elif t1 == 1:
			answer = "Tomorrow will be the doomsday! | Завтра конец света!"
		elif t1 < 0 or Time.tm_year > 2012:
			answer = "We must be already dead... | Мы должны были уже умереть..."
		else:
			answer = "There are %d days left to the Apocalypse." % (t1)
		reply(mType, source, answer)

command_handler(command_apocalypse, 10, "doomsday")
