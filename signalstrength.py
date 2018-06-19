#!/usr/bin/env python

from datetime import datetime
import csv
import json
import os
from pysnmp.hlapi import *
import sys
import web

def get_signal_strength(ip):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               # UBNT-AirMAX-MIB::ubntWlStatSignal
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.41112.1.4.5.1.5.1'))
           )
    )

    if errorIndication or errorStatus:
        return None
    else:
        return int(varBinds[0][1])


def open_tsv(path):
    write_header = not os.path.isfile(path)
    w = csv.writer(open(path, 'ab'), dialect='excel-tab')
    if write_header:
        w.writerow(['Time', 'Signal Strength'])
    return w


def main(outfile, ip):
    s = get_signal_strength(ip)
    if s is not None:
        open_tsv(outfile).writerow([datetime.utcnow().isoformat(), s])


class index:
    def GET(self):
        data = open(os.path.join(os.path.dirname(__file__), 'signalstrength.html'), 'rb').read()
        return data


class wifisignal:
    def GET(self, ip):
        s = get_signal_strength(ip)
        return json.dumps({'signal': s})


urls = (
    '/', index,
    '/wifisignal/(.+)', wifisignal,
)

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '192.168.1.200')
