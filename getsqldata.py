# import MySQLdb as my
import pymysql.cursors
import configparser
import json
from sql_connection_factory import get_sql_connection

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

DB_TABLE = config.get('database', 'database_table')

def get_alpr_sql_table_data(date, from_date, to_date):
	dataset = ''
	row_count = 0
	total_cost = 0
	total_park_hours = 0
	SQL_QUERY = ""
	try:	
		if date not in "null":
			# print("DATE ::: "+str(date))
			SQL_QUERY = "SELECT `VEHICLE_IMG`,`ALPR_IMG`,`QRCODE_IMG`,`STARTDATETIME`,`ENDDATATIME`,`PARKING_HOURS`,`TOTAL_COST`,`ALPR_ID`,`VEHICLE_NUM` FROM "+DB_TABLE+" WHERE DATE(`STARTDATETIME`) LIKE '"+date+"'"
		elif from_date not in "null" and to_date not in "null":			
			SQL_QUERY = "SELECT `VEHICLE_IMG`,`ALPR_IMG`,`QRCODE_IMG`,`STARTDATETIME`,`ENDDATATIME`,`PARKING_HOURS`,`TOTAL_COST`,`ALPR_ID`,`VEHICLE_NUM` FROM "+DB_TABLE+" WHERE DATE(`STARTDATETIME`) >= '"+from_date+"' AND DATE(`STARTDATETIME`) <= '"+to_date+"'"
			# print(SQL_QUERY)
		db = get_sql_connection()		
		
		cursor = db.cursor()
		number_of_rows = cursor.execute(SQL_QUERY)
		rows = cursor.fetchall()
		rowset = []
		
		for row in rows:			
			data = {
				'VEHICLE_IMG': row[0],
				'ALPR_IMG': row[1],
				'QRCODE_IMG': row[2],
				'STARTDATETIME': row[3].strftime("%Y-%m-%d %H:%M"),
				'ENDDATATIME': row[4].strftime("%Y-%m-%d %H:%M"),
				'PARKING_HOURS': row[5],
				'ALPR_ID': row[7],
				'TOTAL_COST':row[6],
				'VEHICLE_NUM':row[8]
			}
			total_cost = int(total_cost)+int(row[6])
			total_park_hours = int(total_park_hours)+int(row[5])			
			row_count = int(row_count)+int(1)
			rowset.append(data)
		db.commit()
		db.close()
		dataset = json.dumps(rowset)
		print(row_count)		
	except Exception as e:
		print(str(e))
	return json.dumps({"tabledata":dataset, "rowcount":row_count, "totalcost":total_cost, "totalparkhours":total_park_hours})

# get_alpr_sql_table_data()