import pika
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange(s) exist(s) (in case this starts before)
channel.exchange_declare(exchange='accept_reject_exchange', exchange_type=ExchangeType.fanout)

# create queue to consume messages from and bind to exchange
channel.queue_declare(queue='accept_reject_queue')

channel.queue_bind(queue='accept_reject_queue', exchange='accept_reject_exchange')

# consume messages off the dlx with a callback
def callback(ch, method, properties, body):
    # manually acknowledge the messages in batches (5 messages received then acknowledge all)
    if (method.delivery_tag % 5 == 0):
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)

    print(f"Consumer -> Received new message: {body}")

channel.basic_consume(queue='accept_reject_queue', on_message_callback=callback)

print("Started consuming")

channel.start_consuming()