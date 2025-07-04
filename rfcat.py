#!/usr/bin/env python3

from __future__ import print_function

import sys
import logging
import msvcrt

import rlcompleter

try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        print("Optional: Install pyreadline3 for better tab completion")

from rflib import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)


intro = """'RfCat, the greatest thing since Frequency Hopping!'

Research Mode: enjoy the raw power of rflib

currently your environment has an object called "d" for dongle.  this is how 
you interact with the rfcat dongle:
    >>> d.ping()
    >>> d.setFreq(433000000)
    >>> d.setMdmModulation(MOD_ASK_OOK)
    >>> d.makePktFLEN(250)
    >>> d.RFxmit(b"HALLO")
    >>> d.RFrecv()
    >>> print(d.reprRadioConfig())

"""

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--research', default=False, action="store_true", help='Interactive Python and the "d" instance to talk to your dongle.  melikey longtime.')
    parser.add_argument('-i', '--index', default=0, type=int) 
    parser.add_argument('-s', '--specan', default=False, action="store_true", help='start spectrum analyzer')
    parser.add_argument('-f', '--centfreq', default=902e6, type=float) 
    parser.add_argument('-c', '--inc', default=250e3, type=float) 
    parser.add_argument('-n', '--specchans', default=104, type=int) 
    parser.add_argument('--bootloader', default=False, action="store_true", help='trigger the bootloader (use in order to flash the dongle)')
    parser.add_argument('--force', default=False, action="store_true", help='use this to make sure you want to set bootloader mode (you *must* flash after setting --bootloader)')
    parser.add_argument('-S', '--safemode', default=False, action="store_true", help='TROUBLESHOOTING ONLY, used with -r')

    ifo = parser.parse_args()

    if ifo.bootloader:
        if not ifo.force:
            print("Protecting you from yourself.  If you want to trigger Bootloader mode (you will then *have* to flash a new RfCat image on it) use the --force argument as well")
            exit(-1)

        print("Entering RfCat Bootloader mode, ready for new image...")
        RfCat(ifo.index, safemode=ifo.safemode).bootloader()
        exit(0)

    elif ifo.specan:
        RfCat(ifo.index).specan(ifo.centfreq,ifo.inc,ifo.specchans)

    elif ifo.research:
        interactive(ifo.index, DongleClass=RfCat, intro=intro, safemode=ifo.safemode)

    else:
         # do the full-rfcat thing
        d = RfCat(ifo.index, debug=False)
        print("RFCat (Windows-Compatible)")
        print("Type Python commands (e.g. d.ping()) or press Ctrl+C to exit.")

        try:
            while True:
                try:
                    line = input(">>> ")
                    exec(line)
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting RFCat.")
