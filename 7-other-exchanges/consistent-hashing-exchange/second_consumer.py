import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare('hashing_exchange', "x-consistent-hash")

# declare queue and bind to exchange with a routing key (binding weight) of 4
# 3/4 of messages will be received by second consumer
channel.queue_declare('letterbox_two')

channel.queue_bind(queue='letterbox_two', exchange='hashing_exchange', routing_key='4')

# consume the message by using a callback
def callback(ch, method, properties, body):
    print(f'Second consumer -> Received new message: {body}')

channel.basic_consume(queue='letterbox_two', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()
