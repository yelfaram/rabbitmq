import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Enables Publish Confirms
channel.confirm_delivery()

# Enables Transactions
channel.tx_select()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Creates a durable queue that survives restarts
channel.queue_declare("test", durable=True)

message = "I want to broadcast this message"

channel.basic_publish(
    exchange='pubsub',
	routing_key='1',
	# set properties including custom (headers), delivery_mode (message persistence), expiration and content type
	properties= pika.BasicProperties(
	    headers={'name': 'Brian'},
	    delivery_mode=1,
	    expiration=13434343,
	    content_type="application/json",
    ),
    body=message,
    # set the publish to be mandatory – i.e. receive a notification of failure
    mandatory=True
)

# Commit a transaction
channel.tx_commit()

# Rollback a transaction
channel.tx_rollback()

print(f"sent message: {message}")