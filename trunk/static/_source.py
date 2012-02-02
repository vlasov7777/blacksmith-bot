# -*- coding: utf-8 -*-

# BlackSmith general configuration file

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Сервер на котором зарегистрирована учётка бота | Connect server
SERVER = 'jabber.ru'

# Порт для соединения | Connecting port
PORT = 5222

# Хост сервера (часто совпадает с SERVER) | Jabber server's connecting host
HOST = 'xmpp.ru'

# Шифрование трафика (True - включить, False - выключить) | Use TLS (set True to enable, False for disable)
SECURE = False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Аккаунт бота (жид до @) | User's account
USERNAME = 'BlackSmith[nts]'

# Пароль от жида | Password to Jabber ID
PASSWORD = '******'

# Ресурс бота | Bot's resource
RESOURCE = u"simpleApps" # Можно писать unicode

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Стандартный ник бота | Default bot's nick
DEFAULT_NICK = u"BlackSmith".strip() # Можно писать unicode | You can write unicode symbols here

# Лимит сообщений отсылаемых в конференцию (подробновси в хелпе команды "далее*") | Groupchat message size limit
CHAT_MSG_LIMIT = 1024

# Лимит сообщений, отсылаемых в приват/ростер (сообщения больше лимита отсылаются по частям) | Private/Roster message size limit
PRIV_MSG_LIMIT = 2024

# Максимальный размер принимаемых сообщений (сообщения больше лимита урезаются до размера лимита) | Incoming message size limit
INC_MSG_LIMIT = 8960

# Работа без прав модератора (True - включить, False - выключить) | Working without rights of moder (True - to enable, False - to disable)
MSERVE = False

# Владелец бота (жид, на который бот будет отсылать извещения о важных событиях) | Jabber account of bot's owner
BOSS = 'admin[at]tld'.lower()

# Лимит на использование оперативной памяти (размер в килобайтах, 0 - без лимита) | Memory usage limit (set 0 for disable)
MEMORY_LIMIT = 49152

# Пароль администратора (нужен для команды "логин"; укажите "/random(количество символов)" для автогенерации) | Bot's password (for login cmd; set "/random(symbols count)" for auto generation)
BOSS_PASS = '/random(10)'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
