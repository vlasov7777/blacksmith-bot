# -*- coding: utf-8 -*-

# BlackSmith general configuration file

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Jabber server to connect
SERVER = 'jabber.ru'

# Connecting Port
PORT = 5222

# Jabber server`s connecting Host
HOST = 'xmpp.ru'

# Using TLS (True - to enable, False - to disable)
SECURE = False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# User`s account
USERNAME = 'BlackSmith[nts]'

# Jabber ID`s Password
PASSWORD = '******'

# Resourse (please don`t touch it)
RESOURCE = u'BlackSmith by WitcherGeralt'# You may write ru symbols here

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Default chatroom nick
DEFAULT_NICK = u'BlackSmith[bot]'.strip()# You may write ru symbols here

# Groupchat message size limit
CHAT_MSG_LIMIT = 1024

# Private/Roster message size limit
PRIV_MSG_LIMIT = 2024

# Incoming message size limit
INC_MSG_LIMIT = 8960

# Working without rights of moder (True - to enable, False - to disable)
MSERVE = False

# Jabber account of bot`s owner
BOSS = 'admin[at]tld'.lower()

# Memory usage limit (size in kilobytes, 0 - not limited)
MEMORY_LIMIT = 49152

# Admin password, used as a key to command "login"
BOSS_PASS = '[%s]'# % PASS_GENERATOR('', 14)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
