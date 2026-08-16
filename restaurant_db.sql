CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price DECIMAL NOT NULL
);

CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER UNIQUE NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'available'
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES tables(id),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR NOT NULL
);

CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL
);

INSERT INTO menu_items (name, price) VALUES 
('Pizza', 150000),
('Burger', 80000),
('Pasta', 120000),
('Salad', 60000);

INSERT INTO tables (table_number, status) VALUES 
(1, 'available'),
(2, 'available'),
(3, 'available'),
(4, 'available');