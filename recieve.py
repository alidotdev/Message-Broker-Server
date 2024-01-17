# !/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                # host='localhost',
                host='16.171.22.224',
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()

    max_priority = 2
    channel.queue_declare(queue='act_jobs', durable=True, arguments={"x-max-priority": max_priority})  

    def callback(ch, method, properties, body):
        priority = properties.priority
        print(f" [x] Received message with priority {priority}: {body}")
        # print(f" [x] Received {body}")

    channel.basic_consume(queue='act_jobs', on_message_callback=callback, auto_ack=True)           # auto_ack is not overritning means all messages will be confirmed for processing by sending acknoledgment message

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)