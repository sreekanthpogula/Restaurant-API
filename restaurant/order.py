from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
import json
from werkzeug.exceptions import abort

from restaurant.auth import login_required
from restaurant.db import get_db

bp = Blueprint('blog', __name__)

# d = [{'Item': 'Rice', 'Price': 150}, {'Item': 'Dal', 'Price': 125}, {'Item': 'Chicken', 'Price': 200}, {
#     'Item': 'Mutton', 'Price': 450}, {'Item': 'Fish', 'Price': 300}, {'Item': 'IceCream', 'Price': 199}, {'Item': 'manchurian', 'Price': 75}, {'Item': 'noodles', 'Price': 90}, {'Item': 'ChickenNoodles', 'Price': 175}, {
#     'Item': 'EggNoodles', 'Price': 100}, {'Item': 'FishFry', 'Price': 300}, {'Item': 'Thumbsup', 'Price': 90}]

with open('data.json') as f:
    d = json.load(f)
orders = []


# @bp.route('/')
# @login_required
# def hello():
#     db = get_db()
#     orders = db.execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' ORDER BY created DESC'
#     ).fetchall()
#     return render_template('order/index.html', orders=orders)


@bp.route("/")
@login_required
def hello_restaurant():
    response = jsonify(
        'Welcome, To the Restaurant Appliaction, YOU CAN ORDER NOW!')
    response.status_code = 200
    return response


@bp.route('/order/showmenu')
@login_required
def show_menu():
    response = jsonify({'Menu': d})
    response.status_code = 200
    return response


@bp.route('/order/createorder/<int:id>', methods=['GET', 'POST'])
@login_required
def create_order(id):
    response = {}
    if id < len(d) and d[id] not in orders:
        d = d[id]
        d['Quantity'] = 1
        orders.append(d)
        response = jsonify({'Status': 'Added', 'Item': d})
        response.status_code = 200
    elif id >= len(d):
        response = jsonify({'Status': 'Not in menu'})
        response.status_code = 404
    elif d[id] in orders:
        for i in orders:
            if i['Item'] == d[id]['Item']:
                i['Quantity'] += 1
        response = jsonify(
            {'Status': 'Updated quantity', 'Item': d[id]})
        response.status_code = 200
    return response
# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')


@bp.route('/order/showorder', methods=['GET'])
@login_required
def show_orders():
    response = ' '
    if len(orders) == 0:
        response = jsonify({'Your orders': 'Haven\'t ordered anything yet'})
        response.status_code = 404
    else:
        response = jsonify({'Your orders': orders})
        response.status_code = 200
    return response

# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


@bp.route('/order/showprice', methods=['GET'])
def show_price():
    response = {}
    if len(orders) == 0:
        response = jsonify({'Orders': 'Haven\'t ordered yet', 'Price': 0})
        response.status_code = 404
    else:
        p = 0
        for i in orders:
            p = p + i['Price']*i['Quantity']
        response = jsonify({'Orders': orders, 'TotalPrice': p})
        response.status_code = 200
    return response


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)

@bp.route('/order/deleteorder/<int:delid>', methods=['GET', 'POST'])
def delete_order(delid):
    response = {}
    if (delid < len(orders) and delid >= 0):
        for i in range(len(orders)):
            if i == delid:
                orders[i]['Quantity'] -= 1

        for i in orders:
            if i['Quantity'] == 0:
                orders.remove(i)
        response = jsonify({'Status': 'Successfully Deleted'})
        response.status_code = 200
    else:
        response = jsonify({'Status': 'Item Wasn\'t in the menu'})
        response.status_code = 404
    return response
# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))


@bp.route('/order/editmenu', methods=['GET', 'PUT'])
def edit_menu():
    item = {'Item': 'New Item', 'Price': 15}
    f = False
    for i in d:
        if i == item:
            f = True
    if not f:
        d.append(item)
        response = jsonify(
            {'Status': 'New Item Added Successfully', 'Item': item})
        response.status_code = 201
    else:
        response = jsonify({'Status': 'Already There', 'Item': item})
        response.status_code = 400
    return response


@bp.route('/order/cancel', methods=['DELETE'])
def delete_from_menu():
    item = d[2]
    for i in d:
        if i == item:
            d.remove(i)
            response = jsonify({'Status': 'Cancelled', 'Item': item})
            response.status_code = 200
            return response

    response = jsonify({'Status': 'Not in Menu', 'Item': item})
    response.status_code = 404
