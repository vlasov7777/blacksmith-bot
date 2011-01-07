# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  trans_plugin.py

# (c) Gigabyte
# http://jabbrik.ru

LANGS = {'ky': u'Русский', u'en': u'английский', u'ja': u'японский', u'ru': u'русский', u'auto': u'Определить язык', u'sq': u'албанский', u'ar': u'арабский', u'af': u'африкаанс', u'be': u'белорусский', u'bg': u'болгарский', u'cy': u'валлийский', u'hu': u'венгерский', u'vi': u'вьетнамский', u'gl': u'галисийский', u'nl': u'голландский', u'el': u'греческий', u'da': u'датский', u'iw': u'иврит', u'yi': u'идиш', u'id': u'индонезийский', u'ga': u'ирландский', u'is': u'исландский', u'es': u'испанский', u'it': u'итальянский', u'ca': u'каталанский', u'zh-CN': u'китайский', u'ko': u'корейский', u'lv': u'латышский', u'lt': u'литовский', u'mk': u'македонский', u'ms': u'малайский', u'mt': u'мальтийский', u'de': u'немецкий', u'no': u'норвежский', u'fa': u'персидский', u'pl': u'польский', u'pt': u'португальский', u'ro': u'румынский', u'ru': u'русский', u'sr': u'сербский', u'sk': u'словацкий', u'sl': u'словенский', u'sw': u'суахили', u'tl': u'тагальский', u'th': u'тайский', u'tr': u'турецкий', u'uk': u'украинский', u'fi': u'финский', u'fr': u'французский', u'hi': u'хинди', u'hr': u'хорватский', u'cs': u'чешский', u'sv': u'шведский', u'et': u'эстонский'}
RULANG = {'ky': u'Русский', 'bg': u'Русский', 'ru': u'Русский', 'uk': u'Русский'}

def handler_google_trans(type, source, Params):
	if Params:
		body = Params.split(None, 2)
		if LANGS.has_key(body[0]) and LANGS.has_key(body[1]) and len(body) >= 3:
			(fl, tl, text) = body
			if fl == 'auto':
				if tl == 'auto':
					reply(type, source, u'Читай помощь по команде!')
					return
			else:
				answer = google_detect_lang(text)
				if not LANGS.has_key(answer):
					reply(type, source, answer)
					return
				else:
					fl = answer
			answer = google_translate(text, fl, tl)
			if answer != u'Аблом!':
				answer = replace_all(answer, {'<b>': u'«', '</b>': u'»', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&amp;': '&', '&middot;': ';'})
			reply(type, source, answer)
		else:
			reply(type, source, u'Читай помощь по команде!')
	else:
		reply(type, source, u'Непонимаю чего ты хочеш!')

def handler_google_trans_auto(type, source, text):
	if text:
		aw = google_detect_lang(text)
		if aw != u'Аблом!':
			if RULANG.has_key(aw):
				answer = google_translate(text, '', 'en')
			else:
				answer = google_translate(text, '', 'ru')
			if answer == '400: could not reliably detect source language':
				answer = u'Ошибка! Невозможно определить язык!'
			else:
				answer = replace_all(answer, {'<b>': u'«', '</b>': u'»', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&amp;': '&', '&middot;': ';'})
			if RULANG.has_key(aw):
				repl = u'Источник: %s\n%s' % (LANGS[aw], answer)
			else:
				repl = u'Источник: %s\n%s' % (aw, answer)
		else:
			repl = u'Аблом!'
		reply(type, source, repl)
	else:
		reply(type, source, u'а дальше?')

def google_translate(text, from_lang, to_lang):
	try:
		req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%s' % (urllib2.quote(text.encode('utf-8')), from_lang+'%7C', to_lang))
	except urllib2.HTTPError, Error:
		return unicode(Error)
	except:
		return u'Аблом!'
	answer = simplejson.load(req)
	if answer['responseStatus'] != 200:
		return '%s: %s' % (unicode(answer['responseStatus']), answer['responseDetails'])
	elif answer['responseData']:
		return answer['responseData']['translatedText']
	return u'неизвестная ошибка'

def google_detect_lang(text):
	try:
		req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q='+urllib2.quote(text.encode('utf-8')))
	except urllib2.HTTPError, Error:
		return unicode(Error)
	except:
		return u'Аблом!'
	answer = simplejson.load(req)
	if answer['responseStatus'] != 200:
		return '%s: %s' % (unicode(answer['responseStatus']), answer['responseDetails'])
	elif answer['responseData']:
		return answer['responseData']['language']
	return u'неизвестная ошибка'

register_command_handler(handler_google_trans, 'перевод', ['инфо','все'], 10, 'Переводчик с последней ревизии талисмана, респект als!\nПеревод с одного языка в другой. Используется Google Translate. Доступные для перевода языки:\n'+', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in LANGS.iteritems()])), 'перевод <исходный_язык> <нужный_язык> <фраза>', ['перевод en ru hello', 'перевод ru en привет'])
register_command_handler(handler_google_trans_auto, '!', ['инфо','все'], 10, 'Модификация переводчика,\nАвтор модификации: Gigabyte\nПеревод с одного языка в другой с автовыбором, традиционная моя модификация. Используется Google Translate. Доступные для перевода языки:\n'+', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in LANGS.iteritems()])), '! <фраза>', ['! hello', '! привет'])
