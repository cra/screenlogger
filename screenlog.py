#!/usr/bin/python
# coding: utf-8


"""
Thin timesink clone.

TODO
====
screenshot resize
store path to screenshot in db
analyze

"""


import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from actionlogger import ActionLogger


if __name__ == "__main__":
    ''' write test info in default db for ActionLogger '''

    parser = ArgumentParser(prog=sys.argv[0], formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dbname',
        action='store',
        default='logger.db',
        help="sqlite3 DB to use")
    parser.add_argument('--prefix',
        default='i_did_',
        help="Prefix for screenshots")
    args = parser.parse_args(sys.argv[1:])
    act_logger = ActionLogger(args.dbname, args.prefix)
    act_logger.proceed()


