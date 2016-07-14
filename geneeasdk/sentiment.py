# coding=utf-8

"""
Wrappers and CLI for sentiment analysis API
"""

import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://api.geneea.com/s2/sentiment'

class SentimentResponse(namedtuple('SentimentResponse', ['sentiment', 'label', 'language'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        return SentimentResponse(data['sentiment'], data['label'], data['language'])

    @staticmethod
    def fromJsonStr(strSentimentResponse):
        return SentimentResponse.fromDict(json.loads(strSentimentResponse))

def getSentiment(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=SentimentResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print(result.label, result.sentiment, sep='\t')

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateSentiment(inputsAndResults, trueVals):
    raise Exception('sentiment evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getSentiment,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateSentiment
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
