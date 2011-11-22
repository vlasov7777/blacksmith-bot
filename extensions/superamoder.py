# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  superamoder_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_superadmin_amoder(conf, nick, afl, role):
	if not role == 'moderator':
		jid = handler_jid(conf+'/'+nick)
		if jid in ADLIST:
			handler_moder(conf, nick, u'BOSS Лютика всегда модер!')
			msg(conf, u'/me включил модера для %s, так как он его BOSS' % (nick))

register_join_handler(handler_superadmin_amoder)
