# example_consumer.py
import pika, os, time
from queueConnectionFactory import QueueConnectionFactory
import configparser
from savedata import save_data_to_sql_table
import json

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

QUEUE_NAME = config.get('QUEUE_CONF', 'queueName')

def process_msg_from_queue(msg):
	response = ''
	try:
		print("[ Processing ANPR request from Queue ]")
		print("[ Received Message from Queue ] %r " % msg)		
		
		# json_string = json.dumps(msg[1:-1])				
		# msg = json.dumps(json_string)
		# print(msg[1:-1])
		# ALPR_ID = msg['alpr_id']
		# ENDDATATIME = msg['enddatetime']
		# ALPR_IMG = msg['numberplate']
		# VEHICLE_IMG = msg['vehicle_img']
		# STARTDATETIME = msg['startdatetime']
		# QRCODE_IMG = msg['qrcode']
		# print(ALPR_ID)

		save_data_to_sql_table(msg)
		time.sleep(5) # delays for 5 seconds		
	except Exception as e:
		print(str(e))
	return response

queue_conn_fact = QueueConnectionFactory()
channel = queue_conn_fact.get_queue_channel()
# channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  process_msg_from_queue(body)

# set up subscription on the queue
channel.basic_consume(callback,
  queue='queue_anpr',
  no_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()