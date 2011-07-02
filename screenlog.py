#!/usr/bin/python
# coding: utf-8

import sqlite3
import os
import sys
import shlex
import subprocess
from datetime import datetime as dt
from time import time
#from Xlib.protocol.request import GetInputFocus


def MakeName(frmt):
    return dt.strftime(dt.now(), frmt)


def ScreenShot(filename):
    cmd_line = "import -window root " + filename + ".png"
    subprocess.Popen(shlex.split(cmd_line))


def get_active_window():
    p1 = subprocess.Popen(["xdpyinfo"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "focus"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]

    window_id = output.split(',')[0].split()[-1]
    p3 = subprocess.Popen(["xprop", "-id", window_id], stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["grep", "WM_CLASS"],
            stdin=p3.stdout,
            stdout=subprocess.PIPE)
    p3.stdout.close()
    output = p4.communicate()[0]

    return output.split('=')[-1].rstrip()



if __name__ == "__main__":
    ScreenShot("/tmp/idid_" + MakeName('%Y-%m-%d_%H:%M:%S'))
    con = sqlite3.connect("logger.db")
    con.isolation_level = None
    cur = con.cursor()
    cur.execute("insert into programs values ('%s', '%s')" \
            % (get_active_window(), dt.now()))

