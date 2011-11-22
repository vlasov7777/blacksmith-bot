#===istalismanplugin===
# /* coding: utf-8 */
# BlackSmith Bot Plugin
# Other bots copability: True
# © simpleApps Unofficial.

def msgDelivery(client, msg):
	if msg.getType() == "chat":
		if msg.getTag("request"):
			reportMsg = xmpp.protocol.Message(msg.getFrom())
			reportMsg.setID(msg.getID())
			reportMsg.addChild("received", namespace = "urn:xmpp:receipts")
			client.send(reportMsg)

def registerMsgDelivery(nothing):
	JCON.RegisterHandler("message", msgDelivery)

register_stage1_init(registerMsgDelivery)
