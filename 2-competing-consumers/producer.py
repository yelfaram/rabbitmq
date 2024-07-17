import pika
import random
import string
import time

# create connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create queue
channel.queue_declare('task-queue')

# create message id
def generate_message_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

# default exchange to send message to which will handle sending message to queue
while True:
    message_id = generate_message_id()
    message = f"Sending messageId: {message_id}"

    channel.basic_publish(exchange='', routing_key='task-queue', body=message)
    print(f'sent message: {message}')

    # send messages every 1-3 seconds
    time.sleep(random.randint(1, 3))

