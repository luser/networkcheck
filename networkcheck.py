#!/usr/bin/env python

from __future__ import print_function

import os
from subprocess import call, STDOUT

def check_host(host):
    return call(['/bin/ping', '-c', '1', '-q', host],
                stdout=open(os.devnull, 'wb'),
                stderr=STDOUT) == 0

def hosts():
    return [
        ('192.168.1.2', '4955 Router'),
        ('192.168.1.200', '4955 WiFi'),
        ('192.168.1.203', '4975 WiFi 1'),
        ('192.168.1.202', '4975 WiFi 2'),
        ('192.168.1.201', '5061 WiFi'),
        ('192.168.1.1', '5061 Router'),
        ('8.8.8.8', 'Internet'),
    ]

def check():
    down = False
    for (host, name) in hosts():
        down = down or not check_host(host)
        yield (host, name, not down)

if __name__ == '__main__':
    for (host, name, status) in check():
        print('{}: {}'.format(name, 'UP' if status else 'DOWN'))
