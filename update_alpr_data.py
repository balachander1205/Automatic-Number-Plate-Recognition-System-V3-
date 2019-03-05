# import MySQLdb as my
import pymysql.cursors
import configparser
import json
from datetime import datetime
import time
from sql_connection_factory import get_sql_connection
# import simplejson as json

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

DB_TABLE = config.get('database', 'database_table')
COST_PER_HOUR = config.get('anpr', 'costperhour')
# definintion to update alpr sql table data
def update_data_to_sql_table(alpr_id, startdatetime, enddatetime):	
	try:		
		db = get_sql_connection()		
		startsatetime = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M")
		enddatetime = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M")
		print(startdatetime)
		print(enddatetime)
		diff = enddatetime - startsatetime

		days, seconds = diff.days, diff.seconds
		hours = days * 24 + seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60

		ALPR_ID = alpr_id
		ENDDATATIME = enddatetime				
		STARTDATETIME = startdatetime
		print(datetime.strftime(ENDDATATIME, "%Y-%m-%d %H:%M"))
		TOTAL_COST = int(hours) * int(COST_PER_HOUR)
		cursor = db.cursor()		
		UPDATE_QUERY = "UPDATE "+DB_TABLE+" SET ENDDATATIME = '"+str(ENDDATATIME)+"', PARKING_HOURS='"+str(hours)+"', TOTAL_COST='"+str(TOTAL_COST)+"' WHERE ALPR_ID = '"+ALPR_ID+"'"		
		update_row = cursor.execute(UPDATE_QUERY)
		db.commit()
		db.close()
	except Exception as e:
		print(str(e))
		