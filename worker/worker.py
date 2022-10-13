import pika
import time
import json
from pymongo import MongoClient

client = MongoClient("test_mongodb")  # connecting to mongodb service

db = client.pizza_house
collection = db.orders


# rabbitmq service takes one to couple of minutes after starting to accept messages,
# so we cannot send messages until the service is started and ready

print('Connecting to server, wait a few seconds...')

while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq"))
        break
    except:
        # continue to connect to rabbitmq service after every 5 seconds of failure
        time.sleep(5)
        continue


print('Connected to rabbitmq server!')


channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print('Waiting for messages.')


def callback(ch, method, properties, body):
    print(f"Received the message : {body}")
    cmd = body.decode()

    collection.insert_one(json.loads(body))  # consuming the message
    print("Done")

    # acknowledgement that message is consumed
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
# messages in task quesue are consumed one after another by calling the callback on every message
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
