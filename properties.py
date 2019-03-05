import configparser
import json

config = configparser.RawConfigParser()
# config.read('E:\MY-PROJECTS\pythonRest-ANPR - V2/static/config/config.properties')getProperties
config.read('static/config/config.properties')
# cfgfile = open('E:\MY-PROJECTS\pythonRest-ANPR - V2/static/config/config.properties','w')
# cfgfile = open('static/config/config.properties','w')

# Database configuration
DB_HOST = config.get('database', 'database_host')
DB_USERNAME = config.get('database', 'database_username')
DB_PASSWORD = config.get('database', 'database_password')
DB_NAME = config.get('database', 'database_name')
DB_TABLE = config.get('database', 'database_table')
# ANPR configuration
IMG_DIR = config.get('anpr', 'imagefilesDir')
PY_TESSERACT = config.get('anpr', 'pytesseract.pytesseract.tesseract_cmd')
PY_TESSERACT_DIR_CONF = config.get('anpr', 'tessdata_dir_config')
COST_PER_HOUR = config.get('anpr', 'costperhour')
# Queue Configuration
Q_CONNCETION = config.get('QUEUE_CONF', 'queueConnectionName')
Q_CONNCETION_URL = config.get('QUEUE_CONF', 'queueConnectUrl')
Q_NAME = config.get('QUEUE_CONF', 'queueName')
Q_DURABILIITY = config.get('QUEUE_CONF', 'queueDurable')

def getProperties():	
	data = {}
	data['DB_HOST'] = DB_HOST
	data['DB_USERNAME'] = DB_USERNAME
	data['DB_PASSWORD'] = DB_PASSWORD
	data['DB_NAME'] = DB_NAME
	data['DB_TABLE'] = DB_TABLE
	data['IMG_DIR'] = IMG_DIR
	data['PY_TESSERACT'] = PY_TESSERACT
	data['PY_TESSERACT_DIR_CONF'] = PY_TESSERACT_DIR_CONF
	data['COST_PER_HOUR'] = COST_PER_HOUR
	data['Q_CONNCETION'] = Q_CONNCETION
	data['Q_CONNCETION_URL'] = Q_CONNCETION_URL
	data['Q_NAME'] = Q_NAME
	data['Q_DURABILIITY'] = Q_DURABILIITY
	json_data = json.dumps(data)	
	return json_data

def updateProperties():
	try:
		# config.add_section('anpr')
		config.set('anpr','costperhour', 1000)
		config.write(cfgfile)
		cfgfile.close()
		print('Updating properties')
	except Exception as e:
		print(str(e))
# print(updateProperties())