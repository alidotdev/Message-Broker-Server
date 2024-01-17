#!/usr/bin/env python
import pika


class Sender():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sender, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # You can initialize attributes here
        self.connection = pika.BlockingConnection(
                            pika.ConnectionParameters(
                                host='16.171.22.224',
                                port=5672,
                                credentials=pika.PlainCredentials('guest', 'guest')
                                ))
        self.channel = self.connection.channel()

        # Creating Queue
        max_priority = 2
        self.channel.queue_declare(queue='act_jobs', durable=True, arguments={"x-max-priority": max_priority})                         # Durable defines message queue will sustain even if the RabbitMQ server dies 


    def Publish(self, message, priority):
        print('I am in publish function')
        self.channel.basic_publish(
                            exchange='', 
                            routing_key='act_jobs', 
                            body=message,
                            properties=pika.BasicProperties(
                                delivery_mode = pika.DeliveryMode.Persistent,
                                priority=priority
                            ))
        print(" [x] Sent ", message)

    def Close_Connection(self):
        self.connection.close()

# Create instance
sender = Sender()

for x in range(10):                                                                     # Send messages in loop with diff preority
    sender.Publish('Hello World', x % 2 + 1)

sender.Close_Connection()