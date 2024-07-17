import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare('hashing_exchange', "x-consistent-hash")

# declare queue and bind to exchange with a routing key (binding weight) of 1
# 1/4 of messages will be received by second consumer
channel.queue_declare('letterbox_one')

channel.queue_bind(queue='letterbox_one', exchange='hashing_exchange', routing_key='1')

# consume the message by using a callback
def callback(ch, method, properties, body):
    print(f'First consumer -> Received new message: {body}')

channel.basic_consume(queue='letterbox_one', auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()
