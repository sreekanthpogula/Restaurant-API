from flask import (
    Blueprint, jsonify, request, abort
)
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
    response.headers['Content-Type'] = 'application/json'
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
                    return jsonify(order)
    #                 return order
    #         else:
    #             return "Order not found with Id"
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
    if content_type != 'application/json':
        return 'Content type not supported!', 400

    post_json_data = request.get_json()
    validated_data = order_list(**post_json_data)
    validated_json_data = validated_data.dict()

    if 'order_id' in post_json_data and type(validated_json_data['order_id']) == int:
        with open('data.json', 'r+') as file:
            orders_data = json.load(file)

            list_of_ids = [order["order_id"]
                           for order in orders_data["orders"]]
            if post_json_data['order_id'] in list_of_ids:
                return jsonify({"Message": "Ordered Id Already exists"}), 400

            orders_data["orders"].append(validated_json_data)
            file.seek(0)
            json.dump(orders_data, file, cls=DateTimeEncoder, indent=2)
            file.truncate()

        return jsonify(validated_json_data), 201
    else:
        return jsonify({"Message": "Order Id not exists"}), 400


@bp.route('/orders/<int:order_id>', methods=['PUT'])
@validate()
def update_order(number):
    """
    This function is used to update the existing order
    :param number: order id
    :return: Succesfull response returns updated json or
    Id not exists or content type not exists or order not found
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return 'Content type not supported!', 400

    put_json_data = request.get_json()
    validated_data = order_list(**put_json_data)
    validated_json_data = validated_data.dict()

    if 'order_id' in put_json_data and type(validated_json_data['order_id']) == int:
        with open('data.json', 'r+') as file:
            orders_data = json.load(file)

            list_of_ids = [order["order_id"]
                           for order in orders_data["orders"]]
            if put_json_data['order_id'] not in list_of_ids:
                return jsonify({"Message": "Ordered Id not exists"}), 400

            for order in orders_data["orders"]:
                if order["order_id"] == number:
                    order.update(validated_json_data)
                    file.seek(0)
                    json.dump(orders_data, file, cls=DateTimeEncoder, indent=2)
                    file.truncate()
                    return jsonify(validated_json_data), 200

            return jsonify({"Message": "Order not found"}), 404
    else:
        return jsonify({"Message": "Order Id not exists"}), 400


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
