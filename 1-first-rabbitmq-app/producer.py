import pika

# create a connection to locally running rabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue to send message to
channel.queue_declare(queue='letterbox')

# we will be using default exchange to send message to which will handle sending message to queue
message = "Hello world"
channel.basic_publish(exchange='', routing_key='letterbox', body=message)
print(f'sent message: {message}')

# close connection after sending
connection.close()