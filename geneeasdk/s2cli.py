# coding=utf-8

"""
Default CLI for Geneea S2 API
"""

import itertools
import sys
import time

from geneeasdk.util import cliutil, datautil

from argparse import ArgumentParser

def getS2Flags(args):
    """
    @param args: arguments returned from argument parser
    @return: API call flags extracted from args
    """
    options = dict(args.options) if args.options else {}
    return {'language': args.lang, 'options': options}

def getS2Argparser(defaultUrl):
    parser = ArgumentParser()
    parser = cliutil.addActionArg(parser, choices=['run', 'test', 'eval'], default='run')
    parser = cliutil.addDataConfigArg(parser)
    parser = cliutil.addIdColArg(parser, default=0)
    parser = cliutil.addTextColArg(parser, default=1)
    parser = cliutil.addEvalColArg(parser, default=2)
    parser = cliutil.addUrlArg(parser, default=defaultUrl)
    parser = cliutil.addUserKeyArg(parser)
    parser = cliutil.addLangArg(parser)
    parser = cliutil.addThreadCountArg(parser, default=1)
    parser = cliutil.addOptionsArg(parser)

    return parser

def createS2Cli(*, defaultUrl, apiWrapFunc, runFunc, testFunc, evalFunc):
    """
    Create a CLI - callable object (cmd arguments) -> return value
    which wraps an S2 API function and allows 3 actions:
      - run
      - test
      - evaluation
    @param defaultUrl: default url of the REST API function
    @param apiWrapFunc: function wrapping the API call itself. 
        (document iterable, flags, **kwargs) -> iterable of API call results
    @param runFunc: function implementing the 'run' action. It should accept an iterable of API call results
    @param testFunc: function implementing the 'test' action. 
        It should accept an iterable of tuples (API input, API call result)
    @param evalFunc: function implementing the 'eval' action. 
        It should accept an iterable of tuples (API input, API call result) and an iterable of expected 'true' values
    @return: callable object (cmd arguments) -> return value
    """
    parser = getS2Argparser(defaultUrl)

    def run(args):
        docs = datautil.docStream(sys.stdin, cliutil.columnConfig(args))
        flags = getS2Flags(args)

        results = apiWrapFunc(docs, flags, url=args.url, key=args.userKey, threadCount=args.threadCount)
        runFunc(results)
        return 0

    def test(args):
        docs = datautil.docStream(sys.stdin, cliutil.columnConfig(args))
        flags = getS2Flags(args)

        startTime = time.time()
        inputsAndResults = apiWrapFunc(docs, flags, url=args.url, key=args.userKey,
                threadCount=args.threadCount, returnInputs=True, failFast=False)
        testFunc(inputsAndResults)
        timeElapsed = time.time() - startTime
        print("Processing time: ", timeElapsed, "seconds")
        return 0

    def evaluate(args):
        docLines, evalLines = itertools.tee(sys.stdin, 2)
        columnConfig = cliutil.columnConfig(args)
        docs = datautil.docStream(docLines, columnConfig)
        flags = getS2Flags(args)

        trueVals = datautil.colStream(evalLines, columnConfig['eval'])

        results = apiWrapFunc(docs, flags, url=args.url, key=args.userKey,
                threadCount=args.threadCount, returnInputs=True)
        evalFunc(results, trueVals)
        return 0

    cli = cliutil.simpleCli(parser, {
        'run': run,
        'test': test,
        'eval': evaluate
    })
    return cli
