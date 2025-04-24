-- Customer master
CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    city            TEXT,
    signup_date     TEXT            -- ISO-8601 yyyy-mm-dd
);

INSERT INTO customers VALUES
 (1,'John','Doe','john.doe@example.com','Prague','2024-11-15'),
 (2,'Vasilii','Tokarev','vasilii.tokarev@example.cz','Prague','2024-12-02'),
 (3,'Ivan','Ivanov','ivan.ivanov@example.cz','Prague','2025-01-08'),
 (4,'Janinne','Doe','janinne.ddoe@example.cz','Prague','2025-02-20'),
 (5,'Name','Surname','name.surname@example.cz','Prague','2025-03-05');

-- Product catalog
CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY,
    name            TEXT,
    category        TEXT,
    unit_price      REAL,
    currency        TEXT
);

INSERT INTO products VALUES
 (101,'USB-C Hub','Accessories', 32.90,'EUR'),
 (102,'Wireless Mouse','Peripherals',18.50,'EUR'),
 (103,'27\" 4K Monitor','Displays',299.00,'EUR'),
 (104,'Laptop Stand','Accessories',24.25,'EUR');

-- Order header
CREATE TABLE orders (
    order_id        INTEGER PRIMARY KEY,
    customer_id     INTEGER REFERENCES customers(customer_id),
    order_date      TEXT,
    status          TEXT,          -- SHIPPED | PROCESSING | CANCELLED
    total_amount    REAL,
    currency        TEXT
);

INSERT INTO orders VALUES
 (5001,1,'2025-03-10','SHIPPED',   417.40,'EUR'),
 (5002,3,'2025-03-21','PROCESSING',18.50 ,'EUR'),
 (5003,2,'2025-04-01','SHIPPED',   356.15,'EUR'),
 (5004,5,'2025-04-05','CANCELLED',  0.00 ,'EUR'),
 (5005,4,'2025-04-22','PROCESSING',57.15 ,'EUR');

-- Order line items
CREATE TABLE order_items (
    order_id        INTEGER,
    product_id      INTEGER,
    quantity        REAL,
    unit_price      REAL,
    line_total      REAL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY(order_id)  REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

INSERT INTO order_items VALUES
 (5001,101,2,32.90, 65.80),
 (5001,102,1,18.50, 18.50),
 (5001,103,1,299.00,299.00),
 (5002,102,1,18.50, 18.50),
 (5003,103,1,299.00,299.00),
 (5003,104,2,24.25, 48.50),
 (5005,101,1,32.90, 32.90),
 (5005,104,1,24.25, 24.25);

-- Simple stock snapshot
CREATE TABLE inventory (
    product_id          INTEGER PRIMARY KEY,
    warehouse           TEXT,
    quantity_available  INTEGER,
    last_updated        TEXT
);

INSERT INTO inventory VALUES
 (101,'WH1',120,'2025-04-24'),
 (102,'WH1',200,'2025-04-24'),
 (103,'WH1', 50,'2025-04-24'),
 (104,'WH1', 75,'2025-04-24');