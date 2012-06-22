# BS mark.1 plugin
# /* coding: utf-8 */
# (c) simpleApps CodingTeam, 2011
# This program distributed under Apache 2.0 license.

def chkForDomain(domain, func):
	iterations = - 1
	host = domain
	for x in domain.split("."):
		if not x.isdigit():
			iterations += 1
	if domain.count(".") == iterations:
		host = func(domain)
	return host

def getHost(argv):
	if argv:
		if not chkUnicode(argv): 
			argv = IDNA(argv)
		from socket import gethostbyname
		dns = chkForDomain(argv.strip(), gethostbyname)
		del gethostbyname
		if argv.strip() == dns:
			from socket import gethostbyaddr
			hostname, aliaslist, ipaddrlist = gethostbyaddr(argv.strip())
			del gethostbyaddr
			if not aliaslist: aliaslist = str(None)
			dns = u"%s, %s, %s" % (hostname, aliaslist, " ".join(ipaddrlist))
	else:
		dns = u"что-что?"
	return dns

def command_dns(mType, source, argv):
	try:
		reply(mType, source, getHost(argv))
	except:
		reply(mType, source, returnExc())

def command_chkServer(mType, source, argv):
	answer = u"что?"	
	if argv:
		argv = argv.split()[:2]
		addr, port = str(), str()
		if len(argv) > 1:
			addr, port = argv
		elif argv[0].count(":"):
			addr, port = argv[0].split(":")
		else: 
			reply(mType, source, answer)
			return
		from socket import socket, AF_INET, SOCK_STREAM
		sock = socket(AF_INET, SOCK_STREAM)
		sock.settimeout(5)
		if port.isdigit():
			port = int(port)
		else:
			reply(mType, source, answer)
			return
		try:
			sock.connect((addr,port))
			answer = u"Порт %d на \"%s\" открыт." % (port, addr)
		except:
			print_exc()
			answer = u"Порт %d на \"%s\" закрыт. Не достучался за 5 секунд." % (port, addr) 
		sock.close()
		del socket, AF_INET, SOCK_STREAM
	reply(mType, source, answer)

command_handler(command_dns, 10, "dns")
command_handler(command_chkServer, 10, "dns")