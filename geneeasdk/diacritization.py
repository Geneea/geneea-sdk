# coding=utf-8

"""
Wrappers and CLI for diacritization API
"""

import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://beta-api.geneea.com/s2/diacritization'

class DiacResponse(namedtuple('DiacResponse', ['text', 'language'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        return DiacResponse(data['text'], data['language'])

    @staticmethod
    def fromJsonStr(strDiacResponse):
        return DiacResponse.fromDict(json.loads(strDiacResponse))

def getDiacText(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=DiacResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print(result.text, sep='\t')

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateDiac(inputsAndResults, trueVals):
    raise Exception('diacritization evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getDiacText,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateDiac
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
