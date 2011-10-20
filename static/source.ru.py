# -*- coding: utf-8 -*-

# BlackSmith general configuration file

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Сервер на котором зарегистрирована учётка бота
SERVER = 'jabber.ru'

# Порт соединения
PORT = 5222

# Хост сервера (жид после @)
HOST = 'xmpp.ru'

# Кодирование трафика (True - включить, False - выключить)
SECURE = False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Аккаунт бота (жид до @)
USERNAME = 'BlackSmith[nts]'

# Пароль от жида
PASSWORD = '******'

# Ресурс бота (просьба не менять)
RESOURCE = u'BlackSmith by WitcherGeralt'# Можно писать Русскими буквами

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Стандартный ник бота
DEFAULT_NICK = u'BlackSmith[бот]'.strip()# Можно писать Русскими буквами

# Лимит сообщений отсылаемых в конференцию (подробновси в хелпе команды "ещё*")
CHAT_MSG_LIMIT = 1024

# Лимит сообщений отсылаемых в приват/ростер (сообщения больше лимита отсылаются по частям)
PRIV_MSG_LIMIT = 2024

# Лимит размера принимаемых сообщений (сообщения больше лимита урезаются до размера лимита)
INC_MSG_LIMIT = 8960

# Работа без прав модератора (True - включить, False - выключить)
MSERVE = False

# Владелец бота (жид на который бот будет отсылать извещения о важных событиях)
BOSS = 'admin[at]tld'.lower()

# Лимит на использование оперативной памяти (размер в килобайтах, 0 - без лимита)
MEMORY_LIMIT = 49152

# Пароль администратора (нужен для команды "логин")
BOSS_PASS = '[%s]'# % PASS_GENERATOR('', 14)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
