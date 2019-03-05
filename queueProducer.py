# Code to publish message in Queue
import pika, os, logging
from queueConnectionFactory import QueueConnectionFactory
import configparser

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

QUEUE_NAME = config.get('QUEUE_CONF', 'queueName')

class QueueProducer():
	def __int__(self, message):		
		self.message = message
	def send_message_to_queue(self,message):
		try:
			queue_conn_fact = QueueConnectionFactory()
			channel = queue_conn_fact.get_queue_channel()
			channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
			# print ("[x] Message sent to consumer is "+message)
			queue_conn_fact.close_queue_connection()			
		except Exception as e:
			print(str(e))

# obj = QueueProducer()
# obj.send_message_to_queue("Hello World from producer")