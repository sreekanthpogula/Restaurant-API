from flask import (
    Blueprint, jsonify, request
)
from flask import Flask, jsonify, abort
from models.orders_list import Payment, food_items_list, order_list, Orders
from flask_pydantic import validate

import json
import datetime

from restaurant.auth import login_required

bp = Blueprint('order', __name__)


@bp.errorhandler(400)
def bad_request(error):
    return "Bad Request Error -400", 400


@bp.errorhandler(404)
def not_found(error):
    return "File Not Found- 404", 404


@bp.errorhandler(405)
def method_not_allowed(error):
    return "Method Not Allowed 405", 405


@bp.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error 500", 500


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)


@bp.route("/")
def hello_restaurant():
    response = jsonify(
        'Welcome, To the Restaurant Appliaction, YOU CAN ORDER NOW!')
    response.status_code = 200
    return response


@bp.route('/orders', methods=['GET'])
def get_orders():
    """
    This function is used to display all the order
    returns:ordered items as json
    """
    try:
        if request.method == 'GET':
            with open('data.json', 'r') as f:
                fileData = json.load(f)
                return jsonify(fileData)
    except:
        abort(404)


@bp.route('/orders/<int:number>', methods=['GET'])
def get_specific_order(number):
    """
    used to display the specific ordered item in the json
    param number: ordered_id
    return: ordered_item as json
    """
    try:
        with open('data.json', 'r') as f:
            order_data = json.load(f)
            data = order_data["orders"]
            for order in data:
                if order["order_id"] == number:
                    return order
            else:
                return "Order not found with Id"
    except:
        abort(404)


@bp.route('/orders', methods=['POST'])
@validate()
def create_order():
    """
    This Function is used to create the new order and place the
    new json passed through the body
    :return: Succesfull response returns new placed json or
    Id exists or Content-type not exists
    """
    content_type = request.headers.get('Content-Type')
    try:
        if content_type == 'application/json':
            post_json_data = request.get_json()
            validated_data = order_list(**post_json_data)
            with open('data.json', 'r+') as file:
                orders_data = json.load(file)
                validated_json_data = validated_data.dict()
            if 'order_id' in post_json_data and type(validated_json_data['order_id']) == int:
                list_of_ids = [order["order_id"]
                               for order in orders_data["orders"]]

                for orderId in list_of_ids:
                    if post_json_data['order_id'] == orderId:
                        return jsonify({"Message": "Ordered Id Already exists"})
                else:
                    orders_data["orders"].append(validated_json_data)
                    with open('data.json', 'w') as json_file:
                        json.dump(orders_data, json_file,
                                  cls=DateTimeEncoder, indent=2)
                    return validated_json_data

        else:
            return 'Content type not supported!'
    except:
        return jsonify({"Message": "Invalid request body"})


@bp.route('/orders/<int:order_id>', methods=['PUT'])
@validate()
def update_order(order_id):
    """
    updates the json object according to the request
    :param order_id:
    :return: on success json object modified
    """
    content_type = request.headers.get('Content-Type')
    try:
        if content_type == 'application/json':
            json_data = request.get_json()

            with open('data.json') as fp:
                file_json_data = json.load(fp)
                list_json_data = file_json_data['orders']
            Each_object = [
                task for task in list_json_data if task["order_id"] == order_id]
            if len(Each_object) == 0:
                return jsonify({"Message": "Ordered Id not found Cannot place the request"})
            if not request.json:
                return jsonify({"Message": "Request body is invalid"})
            update_item = Each_object[0]

            if "customer_id" in json_data:
                update_item["customer_id"] = json_data['customer_id']

            if "ordered_items" in json_data:
                ordered_items_list = json_data["ordered_items"]
                updated_order_list = update_item["ordered_items"]
                for each_order in ordered_items_list:
                    print(each_order)
                    for each_ordered_item in updated_order_list:
                        if each_ordered_item['Item_name'] == each_order['Item_name']:
                            print(type(each_order["Quantity"]))
                            if ('Quantity' in each_order.keys() and type(each_order['Quantity'])) == int:
                                each_ordered_item['Quantity'] = each_order['Quantity']
                            else:
                                return jsonify({"Message: Invalid type"})
                            if ('size' in each_order.keys() and type(each_order['size'])) == str:
                                each_ordered_item['size'] = each_order['size']

            with open('data.json', 'w') as json_file:
                json.dump(file_json_data, json_file)
            return "Order data updated succesfully"
        else:
            return jsonify({"Message": "Content-type not supported"})
    except:
        return jsonify({"Message": "Invalid Request body"})


@bp.route('/orders/<int:order_id>/pay', methods=['POST'])
@validate()
def payment(order_id):
    """
    used to create the payment in the order
    :param order_id: order id to create the payment
    :return:On success returns message
    """
    print(order_id)
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            with open('data.json', 'r') as f:
                order_data = json.load(f)
                data = order_data["orders"]
                for order in data:
                    if order["order_id"] == order_id:
                        if 'Payment' in order:
                            return jsonify({"Message": "Payment status already updated"})
                        else:
                            order["Payment"] = json_data
                            with open('data.json', 'w') as json_file:
                                json.dump(order_data, json_file)
                            return order
                else:
                    return "Order Id not found"
    except:
        return "Invalid request body"


@bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    used to cancel the order that has been ordered
    :param order_id: order id used to cancel the respective order
    :return: respective order
    """
    with open('data.json', 'r') as f:
        order_data = json.load(f)
        data = order_data["orders"]
        for order in data:
            if order["order_id"] == order_id:
                if order["status"] == "Canceled":
                    return "Order already canceled"
                order["status"] = "Canceled"
    with open('data.json', 'w') as json_file:
        json.dump(order_data, json_file)
    return order


@bp.route('/orders/<int:number>', methods=['DELETE'])
def delete_order(number):
    """
    Used to delete the order in the object
    :param number: respective order id to be deleted
    :return: Object should be deleted on success
    """
    with open('data.json') as data_file:
        order_data = json.load(data_file)
        data = order_data["orders"]
        for order in data:
            if order["order_id"] == number:
                data.remove(order)
                with open('data.json', 'w') as modified_file:
                    json.dump(order_data, modified_file)
                return jsonify({"Message": "Order is deleted"})

        else:
            return jsonify({"Message": "Order is not found"})


if __name__ == "__main__":
    bp.run(debug=True)
