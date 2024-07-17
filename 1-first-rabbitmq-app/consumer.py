import pika

# create a connection to locally running rabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check queue exists
channel.queue_declare(queue='letterbox')

# consume the message by using a callback
def on_message_received_callback(ch, method, properties, body):
    print(f'Received new message: {body}')


channel.basic_consume(
    queue='letterbox',
    auto_ack=True,
    on_message_callback=on_message_received_callback
)

print("Started consuming")

channel.start_consuming()