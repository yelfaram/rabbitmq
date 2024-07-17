import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare exchange to send messages to
channel.exchange_declare('hashing_exchange', "x-consistent-hash")

# send message
routing_key = "Hfddfsfs asadeq"
message = "Hello World"

channel.basic_publish(exchange='hashing_exchange', routing_key=routing_key, body=message)

print(f'sent message: {message}')

# close connection after sending
connection.close()