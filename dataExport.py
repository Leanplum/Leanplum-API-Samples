#Gets data export
#(c) Leanplum 2015

import urllib2
import re
import json
import time

startDate = raw_input('Enter the startDate you want data for: ')
appId = raw_input('Enter your appId: ')
clientKey = raw_input('Enter your clientKey: ')

# Optional Entries - make sure to uncomment out urlTwo
# endDate = raw_input('Enter the endDate you want data for: ')
# s3ObjectPrefix = raw_inpute('Enter the s3ObjectPrefix: ')

#NOTE: If using for one app, it may be beneficial to store the appId and clientKey
#appId = 'enter your appId as a string here'
#clientKey = 'enter your clientKey as a string here'

#Making the URL that will return the jobId
urlOne = "http://www.leanplum.com/api?appId=" + appId + "&clientKey=" + clientKey + "&apiVersion=1.0.6&action=exportData&startDate=" + startDate
#urlAlt = "http://www.leanplum.com/api?appId=" + appId + "&clientKey=" + clientKey + "&apiVersion=1.0.6&action=exportData&startDate=" + startDate + "&endDate=" + endDate + "&s3ObjectPrefix=" + s3ObjectPrefix + "&s3BucketName=" + s3BucketName +"&s3AccessKey=" + s3AccessKey + "&s3AccessId=" + s3AccessId + "&compressData=" + compressData 

print urlOne
#Getting the jobId
# MAKE SURE TO REPLACE urlOne with urlAlt IF YOU ARE USING THE OTHER ENTRIES 
response = urllib2.urlopen(urlOne)
html = response.read()
fullHTML = json.loads(html)
jobId = fullHTML['response'][0]['jobId']

#Making the URL that will return the link for the data export
urlTwo = "http://www.leanplum.com/api?appId=" + appId + "&clientKey=" + clientKey + "&apiVersion=1.0.6&action=getExportResults&jobId=" + jobId
print urlTwo

loading = True
while(loading):
 	responseTwo = urllib2.urlopen(urlTwo)
 	htmlTwo = responseTwo.read()
 	fullTwo = json.loads(htmlTwo)
 	state = fullTwo['response'][0]['state']
	if (state == 'FINISHED'):
		loading = False
	else:
		print "Running, please wait for job to finish"
		time.sleep(10)


#getting the URLs for data export
fullText = json.loads(htmlTwo)
numURLs = len(fullText['response'][0]['files'])

#saving to json
for x in range(0, numURLs):
	print "Saving file %d of %d" % (x+1, numURLs)
	dataExportUrl = fullText['response'][0]['files'][x]
	responseDataExport = urllib2.urlopen(dataExportUrl)
	dataExport = responseDataExport.read()
	with open(date + 'dataExport' + str(x), 'w') as fid:
		fid.write(dataExport)