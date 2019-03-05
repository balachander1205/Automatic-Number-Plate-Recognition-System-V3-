import pika, os, logging
import configparser

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

QUEUE_CONNECTION_NAME = config.get('QUEUE_CONF', 'queueConnectionName')
QUEUE_CONNECT_URL = config.get('QUEUE_CONF', 'queueConnectUrl')
QUEUE_NAME = config.get('QUEUE_CONF', 'queueName')
QUEUE_DURABLE = config.get('QUEUE_CONF', 'queueDurable')
			
#connection = ""
class QueueConnectionFactory(object):
	"""docstring for ClassName"""
	def __init__(self):
		super(QueueConnectionFactory, self).__init__()		

	def get_queue_channel(self):
		channel=0
		try:
			logging.basicConfig()
			# Parse CLODUAMQP_URL (fallback to localhost)			

			url = os.environ.get(QUEUE_CONNECTION_NAME, QUEUE_CONNECT_URL)
			params = pika.URLParameters(url)
			params.socket_timeout = 5

			self.connection = pika.BlockingConnection(params) # Connect to CloudAMQP
			channel = self.connection.channel() # start a channel
			channel.queue_declare(queue=QUEUE_NAME, durable=QUEUE_DURABLE) # Declare a queue
		except Exception as e:
			print(str(e))
		return channel

	def close_queue_connection(self):
		try:
			self.connection.close()
		except Exception as e:
			print(str(e))
		