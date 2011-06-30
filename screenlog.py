#!/usr/bin/python
# coding: utf-8

import sqlite3
import os
import sys
from datetime import datetime as dt
from time import time

def MakeName(frmt):
    return dt.strftime(dt.now(), frmt)

def ScreenShot(filename):
    os.system("import -window root " + filename + ".png")

if __name__ == "__main__":
    ScreenShot("/tmp/idid_" + MakeName('%Y-%m-%d_%H:%M:%S'))
    con = sqlite3.connect("logger.db")
    con.isolation_level = None
    cur = con.cursor()
    cur.execute("insert into programs values ('%s', '%s')" % ('proganame', dt.now()))

