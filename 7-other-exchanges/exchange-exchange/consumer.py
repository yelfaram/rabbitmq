import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare(exchange='second_exchange', exchange_type=ExchangeType.fanout)

# declare a queue from which we consume messages from
channel.queue_declare(queue='letterbox')

# bind queue to exchange
channel.queue_bind(exchange='second_exchange', queue='letterbox')

# consume the message by using a callback
def callback(ch, method, properties, body):
    print(f'Received new message: {body}')

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()