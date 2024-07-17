import pika

# first consumer listens to messages with severity of red

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare(exchange='direct_routing', exchange_type='direct')

# create temporary queue (will have name auto generated) and delete once consumer connection is closed --- like pub sub
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# bind queue to exchange with a binding key red
channel.queue_bind(exchange='direct_routing', routing_key='red', queue=queue_name)

# consume messages with a callback
def callback(ch, method, properties, body):
    print(f'First consumer => Received new message: {body}')

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()