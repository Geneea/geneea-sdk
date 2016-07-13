# coding=utf-8

"""
Functions for dealing with the vertical format
"""

import re

from collections import namedtuple

from geneeasdk.util.datautil import Document

TabularDocument = namedtuple('TabularDocument', ['docId', 'sentences'])
"""
A document with an ID and iterable of sentences. A sentence is an iterable of words. A word is an iterable of fields.
Number and meaning of the fields is not fixed by this class.
"""

def tabularDocStream(lines, docIdRegex):
    """
    Read documents from a vertical format. Returned documents have tabular structure corresponding to the input data.
    @param lines: iterable of lines in vertical format
    @param docIdRegex: regex capturing the document ID format
    @return: generator of TabularDocument instances
    """
    if isinstance(docIdRegex, str):
        docIdRegex = re.compile(docIdRegex)

    docId = None
    sentences = []
    rowBuf = []

    for line in lines:
        line = line.rstrip('\r\n')
        docMatch = docIdRegex.fullmatch(line)
        if docMatch:
            if docId:
                if rowBuf:
                    sentences.append(tuple(rowBuf))
                    rowBuf = []
                yield TabularDocument(docId, tuple(sentences))
                sentences = []
            docId = docMatch.group()
        elif not line:
            if rowBuf:
                sentences.append(tuple(rowBuf))
                rowBuf = []
        else:
            fields = line.split('\t')
            rowBuf.append(tuple(fields))

    if rowBuf:
        sentences.append(tuple(rowBuf))
    if docId:
        yield TabularDocument(docId, tuple(sentences))

def _sentText(tabularSentence, fieldNo=0):
    return ' '.join(row[fieldNo] for row in tabularSentence)

def docStream(lines, docIdRegex, fieldNo=0):
    """
    Read documents usable as API inputs from a vertical format. Plain text of the document is created
    by joining tokens by a single space.
    @param lines: iterable of lines in vertical format
    @param docIdRegex: regex capturing the document ID format
    @return: generator of Document instances
    """
    for tabularDoc in tabularDocStream(lines, docIdRegex):
        text = ' '.join(_sentText(sent, fieldNo=fieldNo) for sent in tabularDoc.sentences)
        yield Document(tabularDoc.docId, text, '', '', None, None, {})

def sentenceDocStream(lines, docIdRegex, fieldNo=0):
    """
    Read sentences from a vertical format and for each return a document usable as API input.
    Plain text of sentences is created by joining tokens by a single space. Document ID for these
    single-sentence documents is generated as {original doc ID}-{zero-based sentence ID}.
    @param lines: iterable of lines in vertical format
    @param docIdRegex: regex capturing the document ID format
    @return: generator of Document instances, one document for each sentence.
    """
    for tabularDoc in tabularDocStream(lines, docIdRegex):
        for i, sent in enumerate(tabularDoc.sentences):
            text = _sentText(sent, fieldNo=fieldNo)
            docId = '{}-{}'.format(tabularDoc.docId, i)
            yield Document(docId, text, '', '', None, None, {})

def sentenceTextStream(lines, docIdRegex, fieldNo=0):
    """
    Read sentences from a vertical format and for each return its plain text.
    Plain text of sentences is created by joining tokens by a single space.
    @param lines: iterable of lines in vertical format
    @param docIdRegex: regex capturing the document ID format
    @return: generator plain text sentences.
    """
    for tabularDoc in tabularDocStream(lines, docIdRegex):
        for sent in tabularDoc.sentences:
            yield _sentText(sent, fieldNo=fieldNo)
