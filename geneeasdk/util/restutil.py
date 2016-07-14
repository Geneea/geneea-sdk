# coding=utf-8

"""
Functions related to calling REST APIs
"""

import requests

import itertools
import json
import time

from collections import ChainMap, deque, namedtuple
from concurrent.futures import ThreadPoolExecutor
from operator import itemgetter
from itertools import islice

REQUEST_MAX_SIZE = 1024 * 1024
DEFAULT_BATCH_SIZE = 10

DEFAULT_CONNECT_TIMEOUT = 3.05
DEFAULT_READ_TIMEOUT = 600

class S2ApiInput(namedtuple('S2ApiInput', [
        'text',
        'title',
        'lead',
        'url',
        'extractor',
        'domain',
        'correction',
        'diacritization',
        'language',
        'returnTextInfo',
        'options'
    ])):
    """
    Representation of Geneea S2 API input
    """
    __slots__ = ()

    @staticmethod
    def fromDocAndFlags(document, flags):
        """
        @param document: input document
        @param flags: additional API parameters
        @return: S2ApiInput corresponding to given document and flags
        """
        docDict = {k: v for k, v in document._asdict().items() if v}
        data = ChainMap(docDict, flags)
        inputDict = {fldName : data.get(fldName, None) for fldName in S2ApiInput._fields}
        return S2ApiInput(**inputDict)

    def serialize(self) -> str:
        """
        @return: raw input to be sent to the API
        """
        return json.dumps(self._asdict())

def s2ApiInputStream(docs, flags):
    """
    Create an iterable of S2 API input objects for given documents and flags
    @param docs: document iterable
    @param flags: additional API parameters
    @return: iterable of S2ApiInput objects
    """
    return map(S2ApiInput.fromDocAndFlags, docs, itertools.repeat(flags))

def documentInput(document):
    """
    @param document: the input Document
    @return: document represented as a dictionary suitable as a REST API input
    """
    inputDict = {'id': document.uid}
    if document.text:
        inputDict['text'] = document.text
    if document.title:
        inputDict['title'] = document.title
    if document.lead:
        inputDict['lead'] = document.lead
    return inputDict

def errorMsg(error):
    """
    @param error: error object
    @return: error message for given error and input.
    """
    return "Error: {type}: {text}".format(type=type(error), text=error)

def remoteCall(url, inputData, key=None, serialize=json.dumps, deserialize=json.loads,
        connectTimeout=DEFAULT_CONNECT_TIMEOUT, readTimeout=DEFAULT_READ_TIMEOUT):
    """
    Call REST API on specified URL with specified parameters.
    @param url: URL to call
    @param inputData: input data object
    @param key: user API key
    @param serialize: function inputData -> str to be sent to server
    @param deserialize: function str -> output data object
    @param connectTimeout: connection timeout see: http://docs.python-requests.org/en/latest/user/advanced/#timeouts
    @param readTimeout: read timeout see: http://docs.python-requests.org/en/latest/user/advanced/#timeouts
    @return: deserialized API response or Exception in case of any error
    """
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    if key:
        headers['Authorization'] = 'user_key ' + key

    try:
        resp = requests.post(url, headers=headers, data=serialize(inputData), timeout=(connectTimeout, readTimeout))
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return deserialize(resp.text)
    except Exception as e:
        return e

def parallelMap(pool, fn, *iterables, timeout=None):
    """
    Lazy map given funcion on given data using a thread/process pool.
    @param pool: thread or process pool with submit() function
    @param fn: function to map
    @param iterables: iterables of individual arguments
    @param timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.

    NOTE: We override Executor.map because the original code was not memory efficient since
    it stored all Future objects in a list. This implementation is using a queue.
    """
    if timeout is not None:
        end_time = timeout + time.time()

    argStream = zip(*iterables)

    # Create a queue of size 2 * max_workers
    buffer = deque([pool.submit(fn, *args) for args in list(islice(argStream, 2 * pool._max_workers))])

    # Yield must be hidden in closure so that the futures are submitted
    # before the first iterator value is required.
    def result_iterator():
        try:
            # In a loop, pop a result from the queue and submit new data to be processed
            while buffer:
                future = buffer.popleft()
                if timeout is None:
                    yield future.result()
                else:
                    yield future.result(end_time - time.time())
                try:
                    args = next(argStream)
                    buffer.append(pool.submit(fn, *args))
                except StopIteration:
                    pass
        finally:
            for future in buffer:
                future.cancel()
    return result_iterator()

def remoteCalls(inputData, threadCount=1, returnInputs=False, failFast=True, **callArgs):
    """
    Call REST API in parallel with given data and arguments

    @param inputData: iterable of input data objects
    @param threadCount: number of worker threads used for parallel API calls
    @param returnInputs: if true, tuples (input, output) will be generated
    @param failFast: if true, raise an exception at any failure. If false and a remote call fails,
        return the exception as its return value.
    @param callArgs: arguments delegated to remoteCall()

    @return: generator of API call results or of tuples (input, output), depending
        on returnInput parameter
    """

    reqFunc = lambda d: (d, remoteCall(inputData=d, **callArgs))
    retValFunc = (lambda x: x) if returnInputs else itemgetter(1)

    with ThreadPoolExecutor(max_workers=threadCount) as executor:
        for (inputObj, result) in parallelMap(executor, reqFunc, inputData):
            if isinstance(result, Exception) and failFast:
                raise result
            yield retValFunc((inputObj, result))
