import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare two exchanges
channel.exchange_declare(exchange="first_exchange", exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange="second_exchange", exchange_type=ExchangeType.fanout)

# bind exchanges to one another
channel.exchange_bind(destination="second_exchange", source="first_exchange")

# send message to first exchange which will then route it to second exchange
message = "This message has gone through an exchange"
channel.basic_publish(exchange="first_exchange", routing_key='', body=message)

print(f'sent message: {message}')

# close connection after sending
connection.close()