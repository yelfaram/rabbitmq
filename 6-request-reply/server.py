import pika
import uuid

# establish connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# consume messages from request queue and send reply to reply queue
channel.queue_declare(queue='request_queue')

def callback(ch, method, properties, body):
    print(f'Received a request: {body} with corr_id {properties.correlation_id}')

    # send reply back (default exchange) to reply queue
    message = f"This is a reply for {properties.correlation_id}"
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=message)

channel.basic_consume(queue='request_queue', auto_ack=True, on_message_callback=callback)

print(f"Starting Server...")

channel.start_consuming()