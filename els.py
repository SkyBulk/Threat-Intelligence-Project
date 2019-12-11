import json
import elasticsearch 

es = elasticsearch.Elasticsearch()
#data = {}
with open('feedsJson.json') as jf:
    for i in jf:
        data = json.loads(i)
        print data
        es.index(index='feeds', doc_type='feeds', body=data)
    #for lines in jf:
        #data = json.load(lines)
        #es.index(index='feeds', doc_type='feeds', id=23, body=data)


 
