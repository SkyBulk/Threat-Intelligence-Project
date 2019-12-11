import urllib 
import pygeoip
import subprocess, shlex
import json
import pymongo
import csv
import elasticsearch
import time
from datetime import date
import sys
import hashlib

url = "http://www.malwaredomainlist.com/hostslist/ip.txt"

#Elastic search connection
es = elasticsearch.Elasticsearch()

current_date = date.today()

#download function
def download_data(feed_url):
    #connection to web page
    response = urllib.urlopen(feed_url)
    data = response.read()
    data_str = str(data)
    lines = data_str.split("\\n")

    #save to a file
    destination = r'ip.txt'
    fx = open(destination, "w")
    for line in lines:
        fx.write(line + "\n")
    fx.close()

the_data = download_data(url)

gi = pygeoip.GeoIP('/home/mpumelelo/Documents/Project/geoip/GeoLiteCity.dat')
fhand = open('testing_ips.txt', "r")
json_data = []
for ip_addresses in fhand:
    ip_addresses = ip_addresses.rstrip()
  
    go = gi.record_by_addr(ip_addresses)
    try:
        longat = go['latitude'], go['longitude']
        ccode = go['country_code']
        ccountry = go['country_name']
    except:
        longat = ""
        ccode = ""
        ccountry = ""
       
    ip_parts = ip_addresses.split('.')
    query = ip_parts[-1] + '.' + ip_parts[-2] + '.' + ip_parts[-3] + '.' + ip_parts[-4] + '.origin.asn.cymru.com'
    cmd =  'dig +short '+ query + ' TXT'
    proc = subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
    out, err = proc.communicate()
    out_parts=out.split('\n')  
    print out_parts

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
        es.index(index='feeds', doc_type='theFeeds', id=23, body=json_data)
        f.write(dictionaryToJson)
        f.write("\n")
    f.close()

    
    #print ip_addresses, longat, ccode, ccountry
   