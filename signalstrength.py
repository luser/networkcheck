#!/usr/bin/env python
from datetime import datetime
import csv
import os
from pysnmp.hlapi import *
import sys

def get_signal_strength():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('192.168.1.200', 161)),
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

def main(outfile):
    s = get_signal_strength()
    if s is not None:
        open_tsv(outfile).writerow([datetime.utcnow().isoformat(), s])

if __name__ == '__main__':
    main(sys.argv[1])
