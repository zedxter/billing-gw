import os

username = ''
gw = ''
command = ''

os.popen("rsh %s@%s '%s'" % (username, gw, command))
