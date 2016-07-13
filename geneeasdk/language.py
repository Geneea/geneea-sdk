# coding=utf-8

"""
Wrappers and CLI for language detection API
"""

import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://beta-api.geneea.com/s2/language'

class LanguageResponse(namedtuple('LanguageResponse', ['language'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        return LanguageResponse(data['language'])

    @staticmethod
    def fromJsonStr(strLangResponse):
        return LanguageResponse.fromDict(json.loads(strLangResponse))

def getLanguage(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=LanguageResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print(result.language, sep='\t')

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateLanguage(inputsAndResults, trueVals):
    raise Exception('language detection evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getLanguage,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateLanguage
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
