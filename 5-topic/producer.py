import pika, random, string

locations = ['asia', 'europe']
order_types = ['purchases', 'payments']
order_customers = ['user', 'business']

def generate_random_id():
    return ''.join(random.choice(string.hexdigits) for _ in range(4))

def generate_random_order():
    location = random.choice(locations)
    order_type = random.choice(order_types)
    customer = random.choice(order_customers)

    return f'{customer}.{location}.{order_type}'

# create connection + channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create exchange
channel.exchange_declare(exchange='topic_routing', exchange_type='topic')

# create message
uid = generate_random_id()
order = generate_random_order()
message = f'Message {uid} from {order}'

channel.basic_publish(exchange='topic_routing', routing_key=order, body=message)
print(f' [x] sent {uid} - {order}')

# close conncection after publishing
connection.close()