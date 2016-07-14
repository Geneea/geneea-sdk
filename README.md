#geneea-sdk

Python SDK for Geneea APIs

### Example of usage

    from geneeasdk.util.datautil import Document
    from geneeasdk.sentiment import getSentiment
    
    doc = Document.make('1', title='I love Python', text='Yes, I do')
    list(getSentiment([doc], flags={}, url='https://api.geneea.com/s2/sentiment', key=<your_user_key>))

result: `[SentimentResponse(sentiment=1, label='positive', language='en')]`

### Example of CLI usage

`echo -e '1\tI love Python' | python3 geneeasdk/sentiment.py -u https://api.geneea.com/s2/sentiment -k <your_user_key>`

stdout: `positive    1`
