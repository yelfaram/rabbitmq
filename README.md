# RabbitMQ Repository

## About

This repository contains examples and notes on RabbitMQ, a distributed message broker. RabbitMQ facilitates communication between applications through message exchanges, supporting asynchronous messaging and microservices architecture. It can be deployed on various cloud environments as well as on-premise.

## Description

RabbitMQ is a robust message broker that supports various messaging patterns, enabling scalable and reliable communication between services. This repository covers installation, core concepts, and common messaging patterns used with RabbitMQ.

## Table of Contents

- [About](#about)
- [Description](#description)
- [Installation](#installation)
  - [Windows and Docker Installation](#windows-and-docker-installation)
  - [Chocolatey Installation (Preferred)](#chocolatey-installation-preferred)
- [Core Concepts](#core-concepts)
  - [Message Broker](#message-broker)
  - [Producer](#producer)
  - [Consumer](#consumer)
  - [Exchanges](#exchanges)
  - [Queues](#queues)
  - [Bindings](#bindings)
  - [Connections and Channels](#connections-and-channels)
- [Common Messaging Patterns](#common-messaging-patterns)
  - [Competing Consumers](#competing-consumers)
  - [Publish/Subscribe](#publishsubscribe)
  - [Routing](#routing)
  - [Topics](#topics)
  - [Request/Reply](#requestreply)
- [Example Code](#example-code)
  - [Sending a Message (Python)](#sending-a-message-python)
  - [Receiving a Message (Python)](#receiving-a-message-python)
- [Notes](#notes)
- [References](#references)

## Installation

### Windows and Docker Installation

1. **Install Erlang** (≥ 26.0 && < 27.0)
   - [Erlang Download](https://erlang.org/download/otp_versions_tree.html)
2. **Install RabbitMQ**
   - [RabbitMQ Download](https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.13.3/rabbitmq-server-3.13.3.exe)

### Chocolatey Installation (Preferred)

```sh
choco install rabbitmq
```

## Core Concepts

### Message Broker
RabbitMQ acts as a post office that accepts and forwards messages between applications, allowing for loosely-coupled systems and seamless scalability.

### Producer
A producer is a program that sends messages to an exchange.

### Consumer
A consumer is a program that waits to receive messages from a queue.

### Exchanges
Producers send messages to exchanges, which then route the messages to queues. The main types of exchanges are:
- Direct: Routes messages based on routing keys.
- Fanout: Routes messages to all bound queues.
- Topic: Routes messages based on pattern matching.
- Headers: Routes messages based on header attributes.

### Queues
Queues store messages until they are consumed. Key properties include:
- Durability: Whether the queue survives broker restarts.
- Exclusive: Whether the queue is used by only one connection.
- Auto-delete: Whether the queue is deleted when the last consumer unsubscribes.

### Bindings
Bindings define the relationship between exchanges and queues.

### Connections and Channels
- Connection: A TCP connection between your application and the RabbitMQ broker.
- Channel: A virtual connection inside a connection, allowing multiple logical flows.

## Common Messaging Patterns

### Competing Consumers
Distributes tasks to multiple workers, with each task delivered to exactly one worker, enabling parallel processing and scalability.

### Publish/Subscribe
Delivers messages to multiple consumers. Each message is broadcasted to all queues bound to the exchange.

### Routing
Routes messages to queues based on routing keys. Useful for delivering messages selectively based on specific criteria.

### Topics
Routes messages based on patterns in routing keys, supporting wildcard matches for flexible routing.

### Request/Reply
Enables two-way communication between services, with a requestor sending a message and waiting for a reply from the replier.

## Example Code

### Sending a Message (Python)
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='letterbox')
message = "Hello world"

channel.basic_publish(exchange='', routing_key='letterbox', body=message)
```

### Receiving a Message (Python)
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='letterbox')

def callback(ch, method, properties, body):
    print(f"Received new message: {body}")

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=callback)
channel.start_consuming()
```

## Notes
If you're interested in learning more or want more detailed explanations, please refer to [this Google Doc](https://docs.google.com/document/d/1nyqWjwtteHgaWfPvPUkoTdk0CyLFYVVjTEfRCv_BpLM/edit?usp=sharing).

## References

- [RabbitMQ YouTube Playlist](https://www.youtube.com/playlist?list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO)
- [RabbitMQ Official Documentation](https://www.rabbitmq.com/docs)

---

*Notes compiled with thanks to the above references.*
