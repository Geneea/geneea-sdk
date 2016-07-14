# coding=utf-8

"""
Data representation and processing
"""

import itertools
import time

from collections import namedtuple
from collections.abc import Iterable
from operator import itemgetter

class Document(namedtuple('Document', ['uid', 'text', 'title', 'lead', 'language', 'domain', 'metadata'])):
    """
    A textual document, typically used as analysis input
    """
    __slots__ = ()

    @staticmethod
    def make(uid, text, *, title='', lead='', language=None, domain=None, metadata=None):
        """
        Create a new Document instance. This is a more user friendly method than the default constructor,
        since it has default values for most of parameters.

        @param uid: unique document ID
        @param text: text (body) of the document
        @param title: title of the document
        @param lead: lead (abstract) of the document
        @param language: document's language
        @param domain: document's domain
        @param metadata: additional metadata (dict)
        """
        metadata = {} if metadata is None else metadata
        return Document(uid, text, title, lead, language, domain, metadata)

def timeStr(seconds=None) -> str:
    """
    @return: string representing the current date and time in the format YYYY-MM-DD.HH-mm-SS,
    e.g., 2015-03-30.09-35-06
    """
    return time.strftime("%Y-%m-%d.%H-%M-%S", time.gmtime(seconds))

def tsvRowStream(lineIterable):
    """
    @param lineIterable: iterable of strings which are valid TSV lines
    @return: generator of TSV rows. A row is represented as a list of strings.
    """
    for line in lineIterable:
        yield line.rstrip('\r\n').split('\t')

def getCols(row, index, sep=' ') -> str:
    """
    Return columns concatenated by given separator.
    @param row: a list of strings
    @param index: index or list of indices
    @return: column(s) from the specified index(es) concatenated by given separator
    """
    if isinstance(index, Iterable):
        return sep.join(row[i] for i in index)
    else:
        return row[index]

def rowToDocument(row, config) -> Document:
    """
    @param row: input row, list of strings
    @param config: input data configuration (dict)
    @return: Document for given row
    """
    uid = getCols(row, config['id'])
    text = getCols(row, config['text']) if 'text' in config else None
    title = getCols(row, config['title']) if 'title' in config else None
    lead = getCols(row, config['lead']) if 'lead' in config else None
    language = getCols(row, config['language']) if 'language' in config else None
    domain = getCols(row, config['domain']) if 'domain' in config else None
    metadataConf = config.get('metadata', {})

    metadata = {field: getCols(row, index) for field, index in metadataConf.items()}

    if not (text or title or lead):
        raise LookupError("either one of 'text', 'title' and 'lead' has to be present. row={r}, config={c}".format(r=row, c=config))
    return Document(uid, text, title, lead, language, domain, metadata)

def docStream(lines, config):
    """
    Create a stream of Documents from TSV line iterable
    @param lines: input line iterable, lines should contain TSV
    @param config: input data column configuration
    @return: generator of Document objects
    """
    return map(rowToDocument, tsvRowStream(lines), itertools.repeat(config))

def colStream(lines, colNo):
    """
    Create a stream of values of given column from TSV line iterable
    @param lines: input line iterable, lines should contain TSV
    @param colNo: column number
    @return: generator of string values of given column
    """
    return map(itemgetter(colNo), tsvRowStream(lines))

def tsvLine(rowIterable) -> str:
    """
    @param rowIterable: iterable of any elements representing a table row
    @return: string with tab separated elements converted to strings by str()
    """
    return '\t'.join(map(str, rowIterable))
