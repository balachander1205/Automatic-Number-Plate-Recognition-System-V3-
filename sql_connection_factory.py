# import MySQLdb as my
import pymysql.cursors
import configparser

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

DB_HOST = config.get('database', 'database_host')
DB_USERNAME = config.get('database', 'database_username')
DB_PASSWORD = config.get('database', 'database_password')
DB_NAME = config.get('database', 'database_name')
DB_TABLE = config.get('database', 'database_table')

def get_sql_connection():
	db_connection = ''
	try:
		db_connection = pymysql.connect(host=DB_HOST,
			user=DB_USERNAME,
			passwd="",
			db=DB_NAME
		)
	except Exception as e:
		print(str(e))
	return db_connection
