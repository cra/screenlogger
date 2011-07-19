#!/usr/bin/python
# coding: utf-8

"""
Logger module

TODO
====
screenshot resize
store path to screenshot in db
pythonize (remove shell calls, use py-xlib)
move DB logic somewhere else (?)

sqlite3 db creation ejemplo
---------------------------
sqlite logger.db
create table programss(class text, name text, date text);

"""


import sqlite3
import os
import sys
import shlex
import subprocess
import logging
from datetime import datetime as dt
from time import time
from Xlib.display import Display


class ActionLogger(object):
    """
    Wrapper for screenshot and db dump
    """
    def __init__(self, dbname, prefix):
        self.dbname = dbname
        self.prefix = prefix

        display = Display()
        focused = display.get_input_focus().focus
        wm_class = focused.get_wm_class() or focused.query_tree().parent.get_wm_class()
        self.wm_name = focused.get_wm_name() or focused.query_tree().parent.get_wm_name()
        self.wm_info = ' '.join([s for s in wm_class])

        try:
            self.con = sqlite3.connect(dbname)
        except OSError:
            logging.exception("DB '%s' not found" % dbname)
            raise


    def proceed(self):
        ''' Perform the dirty stuff we are supposing to do. '''

        timestamp = dt.strftime(dt.now(), '%Y-%m-%d_%H:%M:%S')
        screenshot_filename = "%s%s" % (self.prefix, timestamp)
        self.grab_screenshot(screenshot_filename)

        logging.warning("Saved screenshot %s" % screenshot_filename)
        logging.info("Active window %s, title %s." % (self.wm_info, self.wm_name))

        try:
            with self.con as con:
                con.isolation_level = None
                con.execute("insert into programs values ('%s', '%s', '%s')" \
                    % (self.wm_info, self.wm_name, timestamp))
                logging.info("Database record stored.")
        except sqlite3.IntegrityError:
            logging.exception("sqlite3 found a same entry out there.")
            raise


    def grab_screenshot(self, filename):
        ''' Take the screenshot with the name supplied as parameter. '''

        cmd_line = "import -window root " + filename + ".png"
        if os.system(cmd_line):
            logging.exception("Failed to take a screenshot")
            raise Exception


