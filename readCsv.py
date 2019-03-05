import csv
import json


def readCsvFileAsJson():
	try:
		cameras = []
		with open('static/config/cameras.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				content = ['<style type="text/css">p{color:black}</style><p>' \
				+row['camera_name']+' Location('+row['latitude']+','+row['longitude']+')</p><img width="100%" src=\'/anprfromcam?camera=' \
				+row['camera']+'\' /><input class="btn btn-primary" type="button" value="Click to View" onclick="openCamera( \
				\'\/anprfromcam?camera='+row['camera']+'\',\'Location (lat:'+row['latitude']+','+row['longitude']+')\',\''+row['camera_name']+'\')">', \
				row['latitude'], row['longitude'], row['s_no']]
				# item = {}
				# item['camera_name'] = row['camera_name']
				# item['camera'] = row['camera']
				# item['latitude'] = row['latitude']
				# item['longitude'] = row['longitude']

				cameras.append(content)
		return json.dumps(cameras)
	except Exception as e:
		print("{ Xception in readCsvFileAsJson } ", str(e))

# print(readCsvFileAsJson())