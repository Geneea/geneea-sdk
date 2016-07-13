# coding=utf-8

"""
Wrappers and CLI for entity recognition API
"""

import json
import sys

from geneeasdk import s2cli
from geneeasdk.util import restutil
from geneeasdk.util.restutil import S2ApiInput

from collections import namedtuple

DEFAULT_URL = 'https://beta-api.geneea.com/s2/entities'

EntityInstance = namedtuple('EntityInstance', ['text', 'textOffset', 'textSegment'])

class Entity(namedtuple('Entity', ['name', 'type', 'instances', 'links'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        instances = [EntityInstance(**i) for i in data['instances']]
        return Entity(data['name'], data['type'], instances, data['links'])

class EntitiesResponse(namedtuple('EntitiesResponse', ['entities', 'language'])):
    __slots__ = ()

    @staticmethod
    def fromDict(data):
        entities = [Entity.fromDict(e) for e in data['entities']]
        return EntitiesResponse(entities, data['language'])

    @staticmethod
    def fromJsonStr(strEntitiesResponse):
        return EntitiesResponse.fromDict(json.loads(strEntitiesResponse))

def getEntities(docs, flags, **kwargs):
    inputs = restutil.s2ApiInputStream(docs, flags)
    return restutil.remoteCalls(
            inputData=inputs,
            serialize=S2ApiInput.serialize,
            deserialize=EntitiesResponse.fromJsonStr,
            **kwargs
    )

def outputResults(callResults):
    for result in callResults:
        print(result, sep='\t')

def testResults(inputsAndResults):
    for apiInput, result in inputsAndResults:
        print(apiInput, result)

def evaluateEntities(inputsAndResults, trueVals):
    raise Exception('entities evaluation not implemented yet')

def main(cliargs):
    cli = s2cli.createS2Cli(
            defaultUrl=DEFAULT_URL,
            apiWrapFunc=getEntities,
            runFunc=outputResults,
            testFunc=testResults,
            evalFunc=evaluateEntities
    )
    return cli(cliargs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
