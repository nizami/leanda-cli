# _*_ encoding: utf-8 _*_

import argparse
import getpass
import sys
import os
import yaml
import json


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            try:
                values = getpass.getpass()
            except KeyboardInterrupt:
                print('Password input interrupted.')
                sys.exit(1)
        setattr(namespace, self.dest, values)


class HandlerBase(object):
    info = {}

    def __init__(self, params):
        params = vars(params)
        self.__dict__.update(params)
        self.__call__()

    def __call__(self):
        # pprint.pprint(self.__dict__, width=1)
        pass

    @classmethod
    def eval_params(cls, params):
        token = '+'
        if isinstance(params, list) and params:
            for idx, item in enumerate(params):
                if isinstance(params, dict) or isinstance(params, list):
                    params[idx] = cls.eval_params(item)
                    continue
        if isinstance(params, dict) and params:
            for key, val in params.items():
                if isinstance(val, str) and val.startswith(token):
                    params[key] = eval(val.strip(token))
                    continue
                if isinstance(params, dict) or isinstance(params, list):
                    params[key] = cls.eval_params(val)
                    continue
        return params

    @classmethod
    def subparser(cls, subparsers):
        # '''
        # - Init subparser for class parameters
        # - Init input parameters from class.info variable
        # - Set subclass as handler for current parser
        # '''
        args = yaml.load(cls.info)
        args = cls.eval_params(args)
        options = args.get('params') and args.pop('params') or []
        # print(options)
        subparser = subparsers.add_parser(**args)
        for option in options:
            names = option.pop('names')
            subparser.add_argument(*names, **option)
        subparser.set_defaults(factory=cls)

    @staticmethod
    def get_meta(filepath):
        if not os.path.isfile(filepath):
            raise IOError('Model meta file %s not found' % filepath)
        try:
            with open(filepath) as fh:
                model_meta = json.load(fh)
        except Exception:
            try:
                with open(filepath) as fh:
                    model_meta = yaml.load(fh)
            except Exception:
                message = 'Unsupported format meta file %s' % filepath
                raise RuntimeError(message)
        return model_meta
