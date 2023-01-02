from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Payment(BaseModel):
    payment_status: str
    price: Optional[int]


class food_items_list(BaseModel):
    Item_name: str
    Quantity: int
    size: str


class order_list(BaseModel):
    order_id: int
    customer_id: Optional[int]
    ordered_items: List[food_items_list]
    status: str
    order_time: Optional[datetime] = datetime.now()


class Orders(BaseModel):
    orders: List[order_list]
