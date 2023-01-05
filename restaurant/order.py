import sqlite3
from flask import (
    Blueprint, jsonify, request, abort
)
from models.orders_list import Payment, food_items_list, order_list, Orders
from flask_pydantic import validate

import json
import datetime

from restaurant.db import get_db

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


@bp.route('/')
def hello_restaurant():
    response = jsonify(
        'Welcome, To the Restaurant Application, YOU CAN ORDER NOW!')
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response


@bp.route('/orders', methods=['GET'])
def get_orders():
    """
    This function is used to display all the orders and their corresponding ordered items
    Returns: orders and ordered items as JSON
    """
    if request.method == 'GET':
        # Connect to the database
        conn = get_db()
        c = conn.cursor()

        # Execute a SELECT statement to get all orders and their corresponding ordered items
        c.execute("SELECT o.order_id, o.customer_id, o.status, o.order_time, i.Item_name, i.Quantity, i.size FROM orders o INNER JOIN ordered_items i ON o.order_id = i.order_id")
        rows = c.fetchall()

        # Convert the result to a list of dictionaries
        result = []
        for row in rows:
            result.append({
                "order_id": row[0],
                "customer_id": row[1],
                "status": row[2],
                "order_time": row[3],
                "Item_name": row[4],
                "Quantity": row[5],
                "size": row[6]
            })

        # Close the connection to the database
        conn.close()

        # Return the result as JSON
        return jsonify(result)


@bp.route('/orders/<int:number>', methods=['GET'])
def get_specific_order(number):
    """
    This function is used to display a specific order and its corresponding ordered items
    Parameters: order ID (number)
    Returns: order and ordered items as JSON
    """
    # Connect to the database
    conn = get_db()
    c = conn.cursor()

    # Execute a SELECT statement to get the specified order and its corresponding ordered items
    c.execute("SELECT o.order_id, o.customer_id, o.status, o.order_time, i.Item_name, i.Quantity, i.size FROM orders o INNER JOIN ordered_items i ON o.order_id = i.order_id WHERE o.order_id = ?", (number,))
    row = c.fetchone()

    # Convert the result to a dictionary
    result = {
        "order_id": row[0],
        "customer_id": row[1],
        "status": row[2],
        "order_time": row[3],
        "items": [
            {
                "Item_name": row[4],
                "Quantity": row[5],
                "size": row[6]
            }
        ]
    }

    # Close the connection to the database
    conn.close()

    # Return the result as JSON
    return jsonify(result)


@bp.route('/orders', methods=['POST'])
@validate()
def create_order():
    """
    This function is used to create a new order and its corresponding ordered items
    Returns: new order and ordered items as JSON
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return 'Content type not supported!', 400

    post_json_data = request.get_json()
    validated_data = order_list(**post_json_data)
    validated_json_data = validated_data.dict()

    if 'order_id' in post_json_data and type(validated_json_data['order_id']) == int:
        # Connect to the database
        conn = get_db()
        c = conn.cursor()

        # Insert the order into the orders table
        c.execute("INSERT INTO orders (order_id, customer_id, status, order_time) VALUES (?, ?, ?, ?)",
                  (validated_json_data['order_id'], validated_json_data['customer_id'], validated_json_data['status'], validated_json_data['order_time']))

        # Insert the ordered items into the ordered_items table
        for item in validated_json_data['ordered_items']:
            c.execute("INSERT INTO ordered_items (order_id, Item_name, Quantity, size) VALUES (?, ?, ?, ?)",
                      (validated_json_data['order_id'], item['Item_name'], item['Quantity'], item['size']))

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()

        return jsonify(validated_json_data, {"Message": "Order created Successfully"}), 201
    else:
        return jsonify({"Message": "Order Id not exists"}), 400


@bp.route('/orders/<int:order_id>', methods=['PUT'])
@validate()
def update_order(order_id):
    """
    This function is used to update an existing order and its corresponding ordered items
    Returns: updated order and ordered items as JSON
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Connect to the database
        conn = get_db()
        c = conn.cursor()

        # Get the data from the request body
        json_data = request.get_json()

        # Check if the order_id exists in the orders table
        c.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        if c.fetchone() is None:
            return jsonify({"Message": "Ordered Id not found Cannot place the request"})

        # Update the customer_id if it exists in the request body
        if "customer_id" in json_data:
            c.execute("UPDATE orders SET customer_id=? WHERE order_id=?",
                      (json_data['customer_id'], order_id))

        # Update the ordered items if they exist in the request body
        if "ordered_items" in json_data:
            ordered_items_list = json_data["ordered_items"]
            for each_order in ordered_items_list:
                c.execute("SELECT * FROM ordered_items WHERE order_id=? AND Item_name=?",
                          (order_id, each_order['Item_name']))
                ordered_item = c.fetchone()
                if ordered_item is not None:
                    if ('Quantity' in each_order.keys() and type(each_order['Quantity'])) == int:
                        c.execute("UPDATE ordered_items SET Quantity=? WHERE order_id=? AND Item_name=?", (
                            each_order['Quantity'], order_id, each_order['Item_name']))
                    else:
                        return jsonify({"Message": "Invalid type"})
                    if ('size' in each_order.keys() and type(each_order['size'])) == str:
                        c.execute("UPDATE ordered_items SET size=? WHERE order_id=? AND Item_name=?", (
                            each_order['size'], order_id, each_order['Item_name']))

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()

        return "Order data updated succesfully"
    else:
        return jsonify({"Message": "Content-type not supported"})


@bp.route('/orders/<int:order_id>/pay', methods=['POST'])
@validate()
def payment(order_id):
    """
    This function is used to update the payment status of an order
    Returns: message indicating the payment status was updated
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Connect to the database
        conn = get_db()
        c = conn.cursor()

        # Check if the order_id exists in the orders table
        c.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        if c.fetchone() is None:
            return "Order Id not found"

        # Update the status of the order
        c.execute("UPDATE orders SET status='paid' WHERE order_id=?", (order_id,))

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()

        return "Payment status updated"
    else:
        return "Content-type not supported"


@bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    This function is used to cancel an order
    Returns: the canceled order
    """
    # Connect to the database
    conn = get_db()
    c = conn.cursor()

    # Check if the order_id exists in the orders table
    c.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    row = c.fetchone()
    if row is None:
        return "Order Id not found"

    # Update the status of the order
    c.execute("UPDATE orders SET status='canceled' WHERE order_id=?", (order_id,))

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    # Return the canceled order
    return {
        "order_id": row[0],
        "customer_id": row[1],
        "status": "canceled",
        "order_time": row[3]
    }


@bp.route('/orders/<int:number>', methods=['DELETE'])
def delete_order(number):
    """
    Used to delete the order in the object
    :param number: respective order id to be deleted
    :return: Object should be deleted on success
    """
    # Connect to the database
    db = get_db()
    c = db.cursor()

    # Execute a DELETE statement to delete the order and its corresponding ordered items from the tables
    c.execute("DELETE FROM orders WHERE order_id = ?", (number,))
    c.execute("DELETE FROM ordered_items WHERE order_id = ?", (number,))
    db.commit()

    # Close the connection to the database
    db.close()

    return jsonify({"Message": "Order is deleted"})


if __name__ == "__main__":
    bp.run(debug=True)
