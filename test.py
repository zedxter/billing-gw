from sshclient import *

username = ''
password = ''
gw = ''
command = ''

factory = ClientCommandFactory(username, password, command)
reactor.connectTCP(gw, 22, factory)
reactor.run()
