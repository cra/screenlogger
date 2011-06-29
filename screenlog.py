#!/usr/bin/python
# coding: utf-8

import os
import sys
from datetime import datetime as dt

def MakeName(frmt):
    return dt.strftime(dt.now(), frmt)

def ScreenShot(filename):
    os.system("import -window root " + filename + ".png")

if __name__ == "__main__":
    ScreenShot("/tmp/idid_" + MakeName('%Y-%m-%d_%H:%M:%S'))
