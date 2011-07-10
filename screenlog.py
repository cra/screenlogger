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


from actionlogger import ActionLogger


if __name__ == "__main__":
    ''' write test info in default db for ActionLogger '''

    act_logger = ActionLogger()
    act_logger.proceed()


