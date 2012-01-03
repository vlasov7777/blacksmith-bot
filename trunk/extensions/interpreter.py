# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  Interpreter Plugin
#  Idea (c) Unknown Author
#  Code (c) simpleApps, 2011

def pyEval(mType, source, code):
	try: result = unicode(eval(code))
	except Exception: result = returnExc()
	reply(mType, source, result)

def pyExec(mType, source, code):
	result = u"Done."
	try: exec(unicode(code + "\n"), globals())
	except Exception: result = returnExc()
	reply(mType, source, result)

## PyShell is a name of one our project...
def pyShell(mType, source, cmd):
	if os.name == "posix":
		cmd = "sh -c \"%s\" 2>&1" % (cmd.encode("utf"))
	elif os.name == "nt":
		cmd = cmd.encode("cp1251")
	shell = os.popen(cmd)
	result = shell.read(); shell.close()
	if os.name == "nt": result = result.decode("cp866")
	if not result: result = "Done."
	reply(mType, source, result)

def pyCalc(mType, source, expression):
	if expression and len(expression) <= 24 and not expression.count("**"):
		reg = re.sub("([0-9]|[\+\-\(\/\*\)\%\^\.])", "", expression)
		if reg:
			result = "Недопустимо."
		else:
			try:
				result = eval(expression)
			except ZeroDivisionError:
				result = unichr(8734)
			except Exception:
				result = "An exception found."
	else:
		result = `None`
	reply(mType, source, str(result))

command_handler(pyEval, 100, "interpreter")
command_handler(pyExec, 100, "interpreter")
command_handler(pyShell, 100, "interpreter")
command_handler(pyCalc, 10, "interpreter")