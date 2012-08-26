# BS mark.1-55
# /* coding: utf-8 */
# BlackSmith Bot Plugin
# Other bots compability: True
# © simpleApps Unofficial.

def msgDelivery(client, msg):
	if msg.getType() == "chat":
		if msg.getTag("request"):
			reportMsg = xmpp.protocol.Message(msg.getFrom())
			reportMsg.setID(msg.getID())
			reportMsg.addChild("received", namespace = "urn:xmpp:receipts")
			client.send(reportMsg)

def registerMsgDelivery(nothing):
	jClient.RegisterHandler("message", msgDelivery)

handler_register("01si", registerMsgDelivery)
