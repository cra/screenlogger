#!/usr/bin/python
# coding: utf-8


"""
Thin timesink clone.

TODO
====
screenshot resize
store path to screenshot in db
analyze
pythonize (remove shell calls, use py-xlib)

sqlite3 db creation:
sqlite logger.db
create table progs(text, when INTEGER);

"""


import sqlite3
import os
import sys
import shlex
import subprocess
from datetime import datetime as dt
from time import time


class ActionLogger(object):
    """
    Wrapper for screenshot and db dump
    """
    def __init__(self, dbname="logger.db", prefix="/tmp/idid_"):
        self.dbname = dbname
        self.prefix = prefix
        try:
            self.con = sqlite3.connect(dbname)
        except OSError:
            print >>sys.stderr, "WTF?! '%s' DB not found" % dbname


    def proceed(self):
        ''' Actually perform the dirty stuff we are supposing to do. '''

        timestamp = dt.strftime(dt.now(), '%Y-%m-%d_%H:%M:%S')
        screenshot_filename = "%s%s" % (self.prefix, timestamp)
        self.grab_screenshot(screenshot_filename)
        self.get_active_window()

        try:
            with self.con as con:
                con.isolation_level = None
                con.execute("insert into programs values ('%s', '%s')" \
                    % (self.window_class, timestamp))
        except sqlite3.IntegrityError:
            print >>sys.stderr, "Running way too fast?"

        print "Took a screenshot:\n%s\nActive window %s (WM_CLASS='%s')." % (
            screenshot_filename,
            self.window_id,
            self.window_class,
        )


    def grab_screenshot(self, filename):
        ''' Take the screenshot with the name supplied as parameter. '''

        cmd_line = "import -window root " + filename + ".png"
        if os.system(cmd_line):
            print >>sys.stderr, "Failed to take a screenshot"
            raise Exception


    def get_active_window(self):
        ''' Parse X tools output for WM_CLASS '''

        xdpyinfo = subprocess.Popen(["xdpyinfo"], stdout=subprocess.PIPE)
        grep_focus = subprocess.Popen(["grep", "focus"], stdin=xdpyinfo.stdout, stdout=subprocess.PIPE)
        xdpyinfo.stdout.close()
        output = grep_focus.communicate()[0]

        self.window_id = output.split(',')[0].split()[-1]

        xprop = subprocess.Popen(["xprop", "-id", self.window_id], stdout=subprocess.PIPE)
        grep_for_class = subprocess.Popen(["grep", "WM_CLASS"],
            stdin=xprop.stdout,
            stdout=subprocess.PIPE)
        xprop.stdout.close()
        output = grep_for_class.communicate()[0]

        self.window_class = output.split('=')[-1].rstrip()

        return self.window_class


if __name__ == "__main__":
    ''' write test info in default db for ActionLogger '''

    act_logger = ActionLogger()
    act_logger.proceed()


