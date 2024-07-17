import pika, random
from pika.exchange_type import ExchangeType

headers_options = [{'name': 'Brian'}, {'name': 'Brian', 'age': 27}]
def generate_random_headers():
    return random.choice(headers_options)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare header exchange
channel.exchange_declare(exchange='header_exchange', exchange_type=ExchangeType.headers)

# send message
message = "This message will be sent with headers"
headers = generate_random_headers()
channel.basic_publish(
    exchange='header_exchange', 
    routing_key='letterbox', 
    body=message,
    properties=pika.BasicProperties(headers=headers)
)

print(f'sent message: {message} with headers {headers}')

# close connection after sending
connection.close()
