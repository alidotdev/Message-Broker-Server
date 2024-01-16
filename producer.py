import pika
# from datetime import datetime

# def main():
#     # Creating connection for RabbitMQ
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    
#     # Getting channel descriptor
#     channel = connection.channel()
#     # Declare new queue if it doesn't exist
#     channel.queue_declare(queue='test_queue')
#     # Create new message with timestamp
#     data = "Hi, consumer! [{}]".format(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'))
#     # Publish message in queue
#     channel.basic_publish(exchange='',
#                           routing_key='test_queue',
#                           body=data)
#     # Close connection
#     connection.close()


# if __name__ == '__main__':
#     main()

#!/usr/bin/env python


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(f" [.] fib({n})")
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()