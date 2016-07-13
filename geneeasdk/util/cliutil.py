# coding=utf-8

"""
Functions related to building and using CLIs. Contains functions for adding commonly used arguments.
"""
import yaml

def simpleCli(argparser, actions):
    """
    Create a simple CLI: function args -> return value. The CLI will use given argument parser and run the action
    specified by action argument retrieved from the parser.
    @param argparser: argument parser with parse_args method
    @param actions: mapping action name to action function: args -> return value
    """
    def cli(cmdargs):
        args = argparser.parse_args(cmdargs)
        return actions[args.action](args)
    return cli

def addActionArg(parser, **kwargs):
    parser.add_argument('-a', '--action', dest='action', **kwargs)
    return parser

def addBatchSizeArg(parser, **kwargs):
    parser.add_argument('-b', '--batchSize', dest='batchSize', type=int, **kwargs)
    return parser

def addDataConfigArg(parser, **kwargs):
    parser.add_argument('-c', '--dataConfig', dest='dataConfig', **kwargs)
    return parser

def addIdColArg(parser, **kwargs):
    parser.add_argument('--idCol', dest='idCol', type=int, **kwargs)
    return parser

def addTextColArg(parser, **kwargs):
    parser.add_argument('--textCol', dest='textCol', type=int, **kwargs)
    return parser

def addEvalColArg(parser, **kwargs):
    parser.add_argument('--evalCol', dest='evalCol', type=int, **kwargs)
    return parser

def addUrlArg(parser, **kwargs):
    parser.add_argument('-u', '--url', dest='url', **kwargs)
    return parser

def addUserKeyArg(parser, **kwargs):
    parser.add_argument('-k', '--key', dest='userKey', **kwargs)
    return parser

def addLangArg(parser, **kwargs):
    parser.add_argument('-l', '--lang', dest='lang', **kwargs)
    return parser

def addOptionsArg(parser, **kwargs):
    parser.add_argument('-o', '--options', dest='options', nargs='+', type=lambda kv: kv.split('='), **kwargs)
    return parser

def addThreadCountArg(parser, **kwargs):
    parser.add_argument('-t', '--threads', dest='threadCount', type=int, **kwargs)
    return parser

def columnConfig(args):
    if args.dataConfig:
        with open(args.dataConfig, encoding='utf-8') as configFile:
            config = yaml.load(configFile)
    else:
        colNoArgNames = ('idCol', 'textCol', 'evalCol')
        # 'id' -> args.idCol,...
        config = {argName[:-3]: getattr(args, argName) for argName in colNoArgNames if hasattr(args, argName)}
    return config

