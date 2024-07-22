import pika
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange(s) exist(s) (in case this starts before)
channel.exchange_declare(exchange='main_exchange', exchange_type=ExchangeType.direct)

channel.exchange_declare(exchange='dead_letter_exchange', exchange_type=ExchangeType.fanout)

# create queue that will expire messages not consumed after 5 seconds and bind it to DLX (dead letter exchange)
# we won't be consuming messages here as we want them to expire
channel.queue_declare(
    queue='main_exchange_queue', 
    arguments={
        "x-dead-letter-exchange":"dead_letter_exchange",
        "x-message-ttl": 5000,
    }
)

channel.queue_bind(queue='main_exchange_queue', exchange='main_exchange', routing_key='test')

# create queue for the dead letter exchange to consume messages from and bind to dlx exchange
channel.queue_declare(queue='dlx_queue')

channel.queue_bind(queue='dlx_queue', exchange='dead_letter_exchange')

# consume messages off the dlx with a callback
def callback(ch, method, properties, body):
    print(f"DLX -> Received new message: {body}")

channel.basic_consume(queue='dlx_queue', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()

