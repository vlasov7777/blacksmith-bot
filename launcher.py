#! /usr/bin/python
# /* coding: utf-8 */
#  BlackSmith Bot launcher.

# (c) simpleApps CodingTeam, 2011.

import os, sys
from os import system
from time import sleep


interpreter = sys.executable
kernel = os.path.normpath(os.path.split(sys.argv[0])[0] + "/BlackSmith.py")
launch_target = u"%s %s" % (interpreter, kernel)

del os, sys
while True:
	try:
		system(launch_target)
		sleep(10)
	except KeyboardInterrupt:
		raise