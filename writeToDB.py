import pymongo
import json

#mongoimport --db feeds_db --collection feeds --file feedsJson.json --jsonArray

conn = pymongo.MongoClient()
db = conn.feeds
record = db.feeds_collection
page = open("feedsJson.json",'r')
parsed = json.loads(page.read)

for i in parsed["Records"]:
    record.insert(i)

#submit feeds to elasticsearch 
    m = hashlib.md5()
    m.update(ip_addresses)
    es_dbid = m.hexdigest()
    es.index(
        index="threatIntelligence",
        doc_type = "test-type",
        id=es_dbid,
        body={
            "source" : ip_addresses,
            "sourch_info" : ip_addresses,
            "country" : ccountry,
            "country_code" : ccode,
            "geolocate" : longat,
            "ASN_name_number" : out_parts
           # "date" : current_date
        }
    )
     datas = "IP Address: " + str(ip_addresses) + " Geolocation: " + str(longat) + " Country Code: " + str(ccode) + " Country Name: " + str(ccountry) + " ASN: " + str(out_parts)
    the_data = str(datas).split("\\n")

    des = r'feeds.txt'
    f = open(des, "a")
    for line in the_data:
        f.write(line + "\n")
    f.close()

    #json
    with open('feedsJson.json', 'a') as f:
        json_data = {'IP Address': str(ip_addresses), 'Geolocation': str(longat), 'Country Code':  str(ccode), 'Country Name': str(ccountry), 'ASN': str(out_parts)}
        dictionaryToJson = json.dumps(json_data)
       # es.index(index='feeds', doc_type='theFeeds', id=23, body=json_data)
        f.write(dictionaryToJson)
        f.write("\n")
    f.close()

    #csv
    with open('test.csv', 'a') as fp:
        writer = csv.writer(fp, delimiter=',', lineterminator='\n')
        writer.writerow(datas)
    f.close()

    #with open('test.csv','w') as fp:
       # a = csv.writer(fp)
        #data = [data_to_write]
        #a.writerows(data)
        
    #print data_to_write
    #with open('feedsJson.json', 'w') as f:
        #feeds = {'IP Address ' : str(ip_addresses) ,  'Geolocation ' : str(longat) , 'Country Code ' : str(ccode) , 'Country Name ' : str(ccountry) , 'ASN ' : str(out_parts)}
        #dictionaryToJson = json.dumps(feeds)
        #f.write(dictionaryToJson)
        #print dictionaryToJson
    #f.close()