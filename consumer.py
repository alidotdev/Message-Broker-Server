import pika
# from datetime import datetime


# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
# # Getting channel descriptor
# channel = connection.channel()
# # Declare new queue if it doesn't exist
# channel.queue_declare(queue='test_queue')

# # Start fetching from queue
# while True:
#         method_frame, header_frame, body = channel.basic_get(queue='test_queue', auto_ack=False)
#         if body:
#             print(body.decode("utf-8"))
#             channel.basic_ack(method_frame.delivery_tag)
#         else:
#             break

#!/usr/bin/env python

import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
x = 10
print(" [x] Requesting fib({0})".format(str(x)))
response = fibonacci_rpc.call(x)
print(f" [.] Got {response}")