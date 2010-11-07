# $Id: __init__.py,v 0.1 2010/08/024 01:20:49 Witcher-team Exp $

# (c) WitcherGeralt [WitcherGeralt@rocketmail.com]
# for http://witcher-team.ucoz.ru/

from sys import version as SysVer

PyVer = (str(SysVer).split()[0])[:3]

del SysVer

if PyVer == '2.5':
	from hammer25 import *
elif PyVer == '2.6':
	from hammer26 import *
elif PyVer == '2.7':
	from hammer27 import *
else:
	print 'Error: Unsupported Python Version!'
