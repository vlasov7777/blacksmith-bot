# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  python_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  Gh0st [b0hdan[at]gmail.com]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_python_eval(mType, source, body):
	try:
		repl = unicode(eval(unicode(body)))
	except:
		exc = sys.exc_info()
		repl = '%s - %s' % (exc[0].__name__, exc[1])
	reply(mType, source, repl)

def handler_python_exec(mType, source, body):
	if '\n' in body and body[-1] != '\n':
		body += '\n'
	repl = 'Operation completed successfully!'
	try:
		exec(unicode(body), globals())
	except:
		exc = sys.exc_info()
		repl = '%s - %s' % (exc[0].__name__, exc[1])
	reply(mType, source, repl)

def handler_python_sh(type, source, body):
	if BOT_OS == 'posix':
		command = 'sh -c "%s" 2>&1' % (body.encode('utf-8'))
	else:
		command =  body.encode("cp1251")
	retval = read_pipe(command)
	if retval in ['', None]:
		retval = u'Cделано!'
	reply(type, source, retval)

def handler_python_calc(type, source, body):
	if body:
		if len(body) <= 24 and not body.count('**'):
			eQ = re.sub("([0123456789]|[\+\-\/\*\^\.])", "", body)
			if not eQ.strip():
				try:
					repl = str(eval(body))
				except:
					repl = u'Купи калькулятор и сам эту херь считай!'
			else:
				repl = u'Хрень ты какую-то пишешь! Отвали нафиг!'
		else:
			repl = u'Неее, я явно слишком туп для этого...'
	else:
		repl = u'Умножаем твой IQ на 10 и получаем 20 :lol:'
	reply(type, source, repl)

command_handler(handler_python_eval, 100, "python")
command_handler(handler_python_exec, 100, "python")
command_handler(handler_python_sh, 100, "python")
command_handler(handler_python_calc, 10, "python")
