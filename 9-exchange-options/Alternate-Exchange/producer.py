import pika, random
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create alternate exchange (receives logs, tests)
channel.exchange_declare(exchange='alternate_exchange', exchange_type=ExchangeType.fanout)

# create main exchange with it being connected to alternate exchange (receives prod)
channel.exchange_declare(
    exchange='main_exchange', 
    exchange_type=ExchangeType.direct,
    arguments={"alternate-exchange": "alternate_exchange"}
)

# send a message
message = "Hello this is my first message!"
routing_key = random.choice(['prod', 'test', 'log'])

channel.basic_publish(exchange='main_exchange', routing_key=routing_key, body=message)

print(f' [x] sent message: {message} with key: {routing_key}')

connection.close()