#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  infa_plugin.py

# Author: Mike Mintz [mikemintz@gmail.com]
# Modifications: Als [Als@exploit.in]

def handler_SG_infa(type, source, body):
	if not body:
		body = SERVER
	iq = xmpp.Iq(to = SERVER, typ = 'get')
	iq.setQueryNS(xmpp.NS_STATS)
	iq.setTo(SERVER)
	JCON.SendAndCallForResponse(iq, first_handler_SG, {'body': body, 'type': type, 'source': source})

def first_handler_SG(coze, stanza, body, type, source):
	sType = stanza.getType()
	if sType == 'error':
		reply(type, source, u'не судьба')
	elif sType == 'result':
		Qu = stanza.getQueryChildren()
		iq = xmpp.Iq(to = body, typ = 'get')
		iq.setQueryNS(xmpp.NS_STATS)
		iq.setQueryPayload(Qu)
		JCON.SendAndCallForResponse(iq, second_handler_SG, {'body': body,'type': type,'source': source})
	else:
		reply(type, source, u'не дождался')

def second_handler_SG(coze, stats, body, type, source):
	if stats.getType() == 'result':
		result = u'Инфа о '+body+':\n'
		Pay = stats.getQueryPayload()
		for stat in Pay:
			try:
				info = stat.getAttrs()['name']+': '+stat.getAttrs()['value']+' '+stat.getAttrs()['units']+'\n'
			except:
				info = ''
			result += info
		reply(type, source, result.strip())

command_handler(handler_SG_infa, 10, "infa")
