import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare(exchange='header_exchange', exchange_type=ExchangeType.headers)

# declare a queue from which we consume messages from
channel.queue_declare(queue='letterbox')

bind_args = {
    'x-match': 'all',
    'name': 'Brian',
    'age': 27
}

# bind queue to exchange
channel.queue_bind(exchange='header_exchange', queue='letterbox', arguments=bind_args)

# consume the message by using a callback
def callback(ch, method, properties, body):
    print(f'Received new message: {body}')

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()