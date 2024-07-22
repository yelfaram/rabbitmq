import pika
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange(s) exist(s) (in case this starts before)
channel.exchange_declare(exchange='alternate_exchange', exchange_type=ExchangeType.fanout)

channel.exchange_declare(
    exchange='main_exchange', 
    exchange_type=ExchangeType.direct,
    arguments={"alternate-exchange": "alternate_exchange"}
)

# create queue for main exchange and bind it
channel.queue_declare(queue='main_exchange_queue')

channel.queue_bind(queue='main_exchange_queue', exchange='main_exchange', routing_key='prod')

# consume messages with a callback
def callback(ch, method, properties, body):
    print(f"Main => Received new message: {body}")

channel.basic_consume(queue='main_exchange_queue', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()