import re
from ConfigParser import ConfigParser
from sshclient import *


class Connector(object):
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read('config.ini')
        self.username = self.cfg.get('access', 'username')
        self.password = self.cfg.get('access', 'password')
        self.gateways = [section for section in self.cfg.sections() if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', section)]

        self.block_commands = {
            'in': 'access-template %s abonent_blocked %s %s any',
            'out': 'access-template %s abonent_blocked any %s %s',
        }

    def proceed(self, gw, command):
        factory = ClientCommandFactory(self.username, self.password, command)
        reactor.connectTCP(gw, 22, factory)
        reactor.run()

    def proceed_test(self, gw, command):
        print 'Connect to > %s, username: %s, password: %s' % (gw, self.username, self.password)
        print 'Doing: %s' % command

    def _do_command(self, ip_addr, netmask, action):
        for gw in self.gateways:
            for _list, _type in self.cfg.items(gw):
                command = self.block_commands.get(_type)
                if command:
                    if action == 'block':
                        command = command % (_list, ip_addr, netmask)
                    else:
                        command = 'clear ' + command % (_list, ip_addr, netmask)
                else:
                    continue

                self.proceed(gw, command)

    def gw_block(self, ip_addr, netmask):
        self._do_command(ip_addr, netmask, action='block')

    def gw_unblock(self, ip_addr, netmask):
        self._do_command(ip_addr, netmask, action='unblock')