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
import logging
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
    parser.add_argument('--logfile',
        action='store',
        default='screen.log',
        help="Log file name")
    args = parser.parse_args(sys.argv[1:])

    act_logger = ActionLogger(args.dbname, args.prefix)

    logging.basicConfig(filename=args.logfile,
        filemode='a',
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.DEBUG)

    act_logger.proceed()


