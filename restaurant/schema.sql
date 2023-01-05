-- Create a table to store orders
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  order_time TIMESTAMP NOT NULL
);

-- Create a table to store ordered items
CREATE TABLE ordered_items (
  order_id INTEGER NOT NULL,
  item_name VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  size VARCHAR(255) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
