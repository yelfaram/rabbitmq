import pika
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange(s) exits (in case it starts before)
channel.exchange_declare(exchange='alternate_exchange', exchange_type=ExchangeType.fanout)

# create queue for alternate exchange and bind it
channel.queue_declare(queue='alt_exchange_queue')

channel.queue_bind(queue='alt_exchange_queue', exchange='alternate_exchange')

# consume messages with a callback
def callback(ch, method, properties, body):
    print(f"Alt => Received new message: {body} ")

channel.basic_consume(queue='alt_exchange_queue', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()