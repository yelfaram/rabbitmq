import pika

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare(exchange='topic_routing', exchange_type='topic')

# create temporary queue and delete once connection is closed
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# bind queue to exchange with a binding key that receieves all messages from asia
channel.queue_bind(exchange='topic_routing', queue=queue_name, routing_key='*.asia.*')

# consume message with a callback
def callback(ch, method, properties, body):
    print(f'Analytics Europe consumer => Received new message: {body}')

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()