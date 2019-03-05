# import MySQLdb as my
import pymysql.cursors
import configparser
import json
from sql_connection_factory import get_sql_connection
# import simplejson as json

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

DB_TABLE = config.get('database', 'database_table')


def save_data_to_sql_table(data):
	try:
		db = get_sql_connection()		
		json_data_str = data
						
		datastore = json.loads(json_data_str)
		
		ALPR_ID = datastore['alpr_id']
		ENDDATATIME = datastore['enddatetime']
		ALPR_IMG = datastore['numberplate']
		VEHICLE_IMG = datastore['vehicle_img']
		STARTDATETIME = datastore['startdatetime']
		QRCODE_IMG = datastore['qrcode']
		VEHICLE_NUM = datastore['vehicle_number']

		cursor = db.cursor()	
		sql = "INSERT INTO "+DB_TABLE+"(`ID`,`VEHICLE_IMG`,`ALPR_IMG`,`QRCODE_IMG`,`STARTDATETIME`,`ENDDATATIME`,`PARKING_HOURS`,`TOTAL_COST`,`ALPR_ID`,`VEHICLE_NUM`,`EXTRA_COL2`,`EXTRA_COL3`)VALUES(NULL,\""+VEHICLE_IMG+"\",\""+ALPR_IMG+"\",\""+QRCODE_IMG+"\",\""+STARTDATETIME+"\",\""+ENDDATATIME+"\",\""+str(0)+"\",\""+str(0)+"\",\""+ALPR_ID+"\",\""+VEHICLE_NUM+"\",NULL,NULL)"		
		# number_of_rows = cursor.execute(SQL_QUERY, data)
		number_of_rows = cursor.execute(sql)
		db.commit()
		db.close()
	except Exception as e:
		print(str(e))
	