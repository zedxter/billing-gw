import os

username = ''
password = ''
gw = ''
command = ''

os.popen("rsh %s:%s@%s '%s'" % (username, password, gw, command))
