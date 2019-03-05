# import MySQLdb as my
import pymysql.cursors
import configparser
import json
from sql_connection_factory import get_sql_connection

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

DB_TABLE = config.get('database', 'database_veh_hotlist')

def get_vehicle_hotlist_data():
	SQL_QUERY = ""
	try:
		SQL_QUERY = "SELECT `VEHICLE_NUM` FROM "+DB_TABLE	
		db = get_sql_connection()		
		
		cursor = db.cursor()
		number_of_rows = cursor.execute(SQL_QUERY)
		rows = cursor.fetchall()
		rowset = []		
		for row in rows:						
			rowset.append(row[0])
		db.commit()
		db.close()
		print(rowset)		
	except Exception as e:
		print(str(e))
	return rowset

# get_vehicle_hotlist_data()