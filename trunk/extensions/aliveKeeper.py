# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  aliveKeeper.py

# (c) simpleApps CodingTeam.
# WARNING: THIS CODE IS NOT TESTED.

aliveKeeper = {"iters": 0}

def iQ_ask(victim, callbackFunc, qType):
	iQ = xmpp.Iq("get", to = victim)
	INFO["outiq"] += 1
	iQ.addChild("ping", {}, [], xmpp.NS_PING)
	jClient.SendAndCallForResponse(iQ, callbackFunc, {"qType": qType})

def aliveKeeper_ask(qType):
	if qType == "chat":
		for chat in GROUPCHATS.keys():
			iQ_ask(chat+"/"+handler_botnick(chat), aliveKeeper_answer, qType)
	elif qType == "roster":
		iQ_ask("%s@%s" % (USERNAME, SERVER), aliveKeeper_answer, qType)

def aliveKeeper_answer(coze, iQ, qType):
	if iQ:
		chat, error = iQ.getFrom().getStripped(), iQ.getErrorCode()
		if error and error != "405":
			try:
				ThrName = "rejoin-%s" % (conf.decode("utf-8"))
				if ThrName not in ThrNames():
					composeTimer(360, error_join_timer, ThrName, (chat,)).start()
			except:
				pass
			if qType == "chat":
				aliveKeeper_ask("roster")
			else:
				Print("\n#-# Warn: no answer from me. Lags?", color2)
				aliveKeeper["iters"] += 1
			if aliveKeeper["iters"] > 5:
				raise NoIqAnswer
		else:
			aliveKeeper["iters"] = 0
	else:
		aliveKeeper["iters"] += 1

def aliveKeeper_worker():
	while True:
		time.sleep(60)
		try:
			aliveKeeper_ask("chat")
		except KeyboardInterrupt:
			break
		except IOError, e:
			if e.message == "Disconnected!":
				sys_exit("Can't get an iQ answer.")
			else:
				lytic_crashlog(aliveKeeper_worker)
		except:
			lytic_crashlog(aliveKeeper_worker)

def aliveKeeper_init():
	composeThr(aliveKeeper_worker, aliveKeeper_worker.func_name).start()

handler_register("02si", aliveKeeper_init)
