import pika, random, string

# will produce messages with a severity ['red', 'yellow', 'green']
# first consumer listens to messages with severity of red
# second cosnumer listens to messages with severity of yellow and green

severities = ['red', 'yellow', 'green']

def generate_random_id():
    return ''.join(random.choice(string.hexdigits) for _ in range(4))

def generate_random_severity():
    return random.choice(severities)

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create exchange
channel.exchange_declare(exchange='direct_routing', exchange_type='direct')

# create message with random severity
severity = generate_random_severity()
uid = generate_random_id()
message = f"Message {uid} with a severity of {severity}"

# send message to exchange with a particular routing key -- severity
channel.basic_publish(exchange='direct_routing', routing_key=severity, body=message)
print(f' [x] sent {uid} - {severity}')

# close connection after sending
connection.close()
