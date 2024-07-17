import pika, random, string

def generate_random_id():
    return ''.join(random.choice(string.hexdigits) for _ in range(4))

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create exchange
channel.exchange_declare(exchange='pubsub', exchange_type='fanout')

# send message
uid = generate_random_id()
message = f"Sending message {uid}"
channel.basic_publish(exchange='pubsub', routing_key='', body=message)
print(f' [x] sent {uid}')

# close connection after sending
connection.close()