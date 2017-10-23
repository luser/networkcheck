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
        ('192.168.1.2', 'Local Router'),
        ('192.168.1.200', 'Local WiFi'),
        ('192.168.1.201', 'Remote WiFi'),
        ('192.168.1.1', 'Remote Router'),
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
