import pika
import uuid

# establish connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create temporary queue (reply queue) to consume messages from
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# consume messages from reply queue
def callback(ch, method, properties, body):
    print(f'Received a reply: {body}')

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

# Create and send messages to request queue (exchange will be default)
channel.queue_declare(queue='request_queue')

message = "Can I request a reply"
corr_id = str(uuid.uuid4())

print(f"Sending request: {corr_id}")

channel.basic_publish(
    exchange='', 
    routing_key='request_queue', 
    properties=pika.BasicProperties
        (
            reply_to=queue_name,
            correlation_id=corr_id,
        ),
    body=message
)

print(f"Starting Client...")

channel.start_consuming()