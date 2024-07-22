import pika, random, string, time
from pika.exchange_type import ExchangeType

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create message id
def generate_message_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

# create exchange for accept/reject messages
channel.exchange_declare(exchange='z', exchange_type=ExchangeType.fanout)

while True:
    message_id = generate_message_id()
    message = f"Sending messageId: {message_id}"

    channel.basic_publish(exchange='accept_reject_exchange', routing_key='test', body=message)
    print(f' [x] sent message: {message}')

    input('Press any key to continue...')