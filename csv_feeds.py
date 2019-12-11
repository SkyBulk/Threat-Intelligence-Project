import csv
import pymongo

with open('test.csv', 'w', newline='') as feedsFile:
    feedsFileReader = csv.reader(feedsFile)
    feedsList = []
    for row in feedsFileReader:
        if len(row) != 0:
            feedsList = feedsList + [row]
            print feedsList
feedsFile.close()


