import pika

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check if exchange exists
channel.exchange_declare(exchange='pubsub', exchange_type='fanout')

# create temporary queue (will have name auto generated) that deletes when consumer connection is closed
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# bind queue to exchange
channel.queue_bind(exchange='pubsub', queue=queue_name)

# consume the message by using a callback
def callback(ch, method, properties, body):
    print(f"Second Consumer => Received new message: {body}")

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

print("Started consuming")

channel.start_consuming()
