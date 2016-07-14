#geneea-sdk

Python SDK for Geneea APIs

### Example of usage

    from geneeasdk.util.datautil import Document
    from geneeasdk.sentiment import getSentiment
    
    doc = Document.make('1', title='I love Python', text='Yes, I do')
    list(getSentiment([doc], flags={}, url='https://api.geneea.com/s2/sentiment', key=<your_user_key>))

result: `[SentimentResponse(sentiment=1, label='positive', language='en')]`

Usage of other API methods is analogical. Methods like `getSentiment` accept any iterable of documents and therefore allow stream processing. Parallel processing is also possible by using `threadCount` argument (`-t` option in the CLIs).

### Example of CLI usage
Each module corresponding to an API function is also runnable and provides a CLI which accepts tab separated values.

`echo -e '1\tI love Python' | python3 geneeasdk/sentiment.py -u https://api.geneea.com/s2/sentiment -k <your_user_key>`

stdout: `positive    1`
