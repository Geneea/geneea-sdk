# coding=utf-8

"""
Wrappers and CLI for tagging API
"""
import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://api.geneea.com/s2/tags'

Tag = namedtuple('Tag', ['text', 'score'])

class TagsResponse(namedtuple('TagsResponse', ['tags', 'language'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        tags = [Tag(**l) for l in data['tags']]
        return TagsResponse(tags, data['language'])

    @staticmethod
    def fromJsonStr(strTopicResponse):
        return TagsResponse.fromDict(json.loads(strTopicResponse))

def getTags(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=TagsResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print('\t'.join('|'.join((t.text, '{:.2}'.format(t.score))) for t in result.tags))

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateTopic(inputsAndResults, trueVals):
    raise Exception('tagging evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getTags,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateTopic
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
