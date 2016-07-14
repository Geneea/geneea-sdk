# coding=utf-8

"""
Wrappers and CLI for topic detection API
"""
import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://api.geneea.com/s2/topic'

TopicLabel = namedtuple('TopicLabel', ['label', 'confidence'])

class TopicResponse(namedtuple('TopicResponse', ['topic', 'confidence', 'language', 'labels'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        labels = [TopicLabel(**l) for l in data['labels']]
        return TopicResponse(data['topic'], data['confidence'], data['language'], labels)

    @staticmethod
    def fromJsonStr(strTopicResponse):
        return TopicResponse.fromDict(json.loads(strTopicResponse))

def getTopics(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=TopicResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print(result.topic)

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateTopic(inputsAndResults, trueVals):
    raise Exception('topic evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getTopics,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateTopic
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
