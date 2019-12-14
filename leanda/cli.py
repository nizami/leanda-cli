#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
"""
It is assumed that this script will handle loosely coupled subcommands.
So processing of these subcommands is isolated in separate subclasses
based on superclass responsible for creating an cli-interface

"""

import argparse
from leanda.parser_helper import HandlerBase
from leanda.commands.login import Login, Logout, WhoAmI
from leanda.commands.upload import Upload
from leanda.commands.browse import PWD, LS, CD, RM
from leanda.commands.livesync import LiveSync
from leanda.commands.convert import Convert
from leanda.commands.predict import Predict
from leanda.commands.train import Train
from leanda.commands.list_items import ListItems
from leanda.commands.models import ListModels
from leanda.commands.recordsets import ListRecordsets
from leanda.commands.predict import Predict
from leanda.commands.download import Download
from leanda.commands.categories import Categories
from clint.textui import colored
from leanda.config import DEBUG


def is_subparser(klass):
    return type(klass) == type(object) \
           and issubclass(klass, HandlerBase) \
           and klass is not HandlerBase


def init_subparsers(parser):
    """
    Initialize subclasses - subparsers

    :param parser: main cli parser 
    """
    # handlers = [klass for klass in globals().values() if is_subparser(klass)]
    handlers = [Login, Logout, WhoAmI,
                PWD, LS, CD, RM,
                Download, Upload, LiveSync,
                Train, ListItems, Predict,
                ListModels, ListRecordsets, Categories
                # Convert, 
                ]

    subparsers = parser.add_subparsers()
    for klass in handlers:
        klass.subparser(subparsers)


def init_parser():
    """
    Init main cli parser

    :return parser: main cli parser
    """
    description = '''
           Leanda Command Line Interface (CLI) is intended for installation
           on users computers and will serve as another "client"
           for Leanda platform.'''
    epilog = 'ArqiSoft.com, Gaithersburg, MD 20878, USA'

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    return parser

def main():
    parser = init_parser()
    init_subparsers(parser)
    args = parser.parse_args()

    if 'factory' not in args:
        rgs = parser.parse_args(['-h'])

    if not DEBUG:
        try:
            args.factory(args)
        except AttributeError:
            print(colored.red(parser.format_usage()))
        except AssertionError as e:
            print(colored.red(e))
        except Exception as e:
            print(colored.red(e))
    else:
        args.factory(args)


if __name__ == '__main__':
    main()
