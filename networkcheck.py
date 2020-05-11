#!/usr/bin/env python

from __future__ import print_function

import os
from subprocess import call, STDOUT

import config

def check_host(host):
    return call(['/bin/ping', '-c', '1', '-q', host],
                stdout=open(os.devnull, 'wb'),
                stderr=STDOUT) == 0

def check():
    down = False
    for (host, name) in config.HOSTS:
        down = down or not check_host(host)
        yield (host, name, not down)

if __name__ == '__main__':
    for (host, name, status) in check():
        print('{}: {}'.format(name, 'UP' if status else 'DOWN'))
