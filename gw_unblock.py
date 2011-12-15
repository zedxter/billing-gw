#!/usr/bin/env python
# coding: utf8

from connector import Connector
import sys

if __name__ == "__main__":
    ip_addr = sys.argv[3]
    netmask = sys.argv[4]
    connector = Connector()
    connector.gw_unblock(ip_addr, netmask)
