import db
from flask import app


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)


class OrderedItems(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.order_id'), primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(255), nullable=False)
    order = db.relationship("Orders", back_populates="ordered_items")


Orders.ordered_items = db.relationship(
    "OrderedItems", order_by=OrderedItems.order_id, back_populates="order")


with app.app_context():
    db.create_all()


def init_app(app):
    return 'DATABASE INITIALIZED'
