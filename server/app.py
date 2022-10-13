from flask import Flask, request
from pymongo import MongoClient, errors
from bson.json_util import dumps
import pika                                        #importing the required modules
import uuid
from model.data_model import Order

app = Flask(__name__)
try:
    client = MongoClient("test_mongodb")            #connecting to mongodb service
except errors.ConnectionFailure:
    print("Not able to connect to server")

db = client.pizza_house                             #creating the database and the collection
collection = db.orders


@app.route("/welcome", methods=["GET"])
def welcome():                                      #welcome route
    return "Welcome to Pizza House", 200


#The commented out code is the order route before using the message queue

@app.route("/order", methods=["POST"])
# def save_order():
#     order_object = Order(uuid.uuid4().hex, request.json)                             
#     collection.insert_one({"_id": order_object._id, "data": order_object.data})
#     return dumps({"Order ID": order_object._id}), 201
def save_order():
    order_object = Order(uuid.uuid4().hex, request.json)        # create object from class Order and 
                                                                # uuid generates a unique id for each order
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq"))                      #connecting to rabbitmq service
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)            #creating a message queue
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',                                       #sending/publish the message to queue
        body=dumps({"_id": order_object._id, "data": order_object.data}),
        properties=pika.BasicProperties(
            delivery_mode=2,                                            # make message persistent
        ))
    connection.close()
    return dumps({"Order ID": order_object._id}), 201               #returning the order id


@app.route("/getorders", methods=["GET"])
def get_allorders():                                          #getorders route without trailing forward slash
    allorders = collection.find({})
    return dumps(allorders), 200                              #returning json array of objects


@app.route("/getorders/<order_id>", methods=["GET"])
def get_specificOdrer(order_id):
    filteredOrder = collection.find({"_id": order_id})
    if (len(list(filteredOrder.clone())) == 0):             #counting the documents and if 0 returns 404
        return "Not Found", 404

    return dumps(filteredOrder), 200


if __name__ == '__main__':
    app.debug = True
    app.run()
