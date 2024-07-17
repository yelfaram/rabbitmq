import pika
import time
import random

# create connection
conneciton = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conneciton.channel()

# check if task queue exists
channel.queue_declare('task-queue')

# consume the message by using a callback
def callback(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'Received: {body}, will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")

# equal distribution of tasks
channel.basic_qos(prefetch_count=1)
# start consuming messages
channel.basic_consume(queue='task-queue', on_message_callback=callback)
print("Started consuming")
channel.start_consuming()
