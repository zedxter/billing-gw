import re
import os
from ConfigParser import ConfigParser
from sshclient import *


class Connector(object):
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.optionxform=str
        self.cfg.read('config.ini')
        self.username = self.cfg.get('access', 'username')
#        self.password = self.cfg.get('access', 'password')
        self.gateways = [section for section in self.cfg.sections() if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', section)]

        self.block_commands = {
            'in': 'access-template %s %s %s %s 0.0.0.0 255.255.255.255',
            'out': 'access-template %s %s 0.0.0.0 255.255.255.255 %s %s',
        }
        self.unblock_commands = {
            'in': 'clear access-template %s %s %s %s any',
            'out': 'clear access-template %s %s any %s %s',
        }


    def proceed(self, gw, command):
        self.proceed_info(gw, command)
        factory = ClientCommandFactory(self.username, self.password, command)
        reactor.connectTCP(gw, 22, factory)
        reactor.run()
        print 'completed'

    def proceed_via_rsh(self, gw, command):
        os.popen("rsh -l %s %s '%s'" %(self.username, gw, command))
        print 'Server > %s:' % gw
        print 'Command: %s' % command
        print 'completed.'
        print

    def proceed_info(self, gw, command):
        print 'Connect to > %s, username: %s, password: %s' % (gw, self.username, self.password)
        print 'Doing: %s' % command

    def _do_command(self, ip_addr, netmask, action):
        back_netmask = '.'.join([str(255 - int(i)) for i in netmask.split('.')])
        for gw in self.gateways:
            for lists, _type in self.cfg.items(gw):

                _list, dynamic_list = [x.strip() for x in lists.split(',')]
                if _type in self.block_commands.keys() or _type in self.unblock_commands.keys():
                    if action == 'block':
                        command = self.block_commands.get(_type)
                        command = command % (_list, dynamic_list, ip_addr, back_netmask)
                    else:
                        command = self.unblock_commands.get(_type)
                        command = command % (_list, dynamic_list, ip_addr, back_netmask)
                else:
                    continue

                self.proceed_via_rsh(gw, command)

    def gw_block(self, ip_addr, netmask):
        self._do_command(ip_addr, netmask, action='block')

    def gw_unblock(self, ip_addr, netmask):
        self._do_command(ip_addr, netmask, action='unblock')