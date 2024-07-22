import pika
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create main exchange
channel.exchange_declare(exchange='main_exchange', exchange_type=ExchangeType.direct)

# send a message
message = 'This message will expire...'

channel.basic_publish(exchange='main_exchange', routing_key='test', body=message)

print(f' [x] sent message: {message}')

connection.close()