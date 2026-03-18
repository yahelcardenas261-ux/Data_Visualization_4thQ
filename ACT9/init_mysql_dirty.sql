CREATE DATABASE IF NOT EXISTS sales_data_raw;
USE sales_data_raw;

DROP TABLE IF EXISTS customer_orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    age INT,
    country VARCHAR(50),
    registration_date VARCHAR(50),
    account_balance DECIMAL(10,2)
);

INSERT INTO customers VALUES
(1, 'John Smith', 'john.smith@email.com', '+1-555-0101', 34, 'USA', '2024-01-15', 1250.50),
(2, 'john smith', 'john.smith@email.com', '555-0101', 34, 'usa', '15/01/2024', 1250.50),
(3, 'María García', NULL, '+52-555-0102', 28, 'Mexico', '2024-02-20', -50.00),
(4, 'Li Wei', 'li.wei@email.com', NULL, 999, 'China', '2024-03-10', 3500.00),
(5, 'Anna Müller', 'anna.muller@email.com', '+49-555-0103', 45, 'Germany', '2024-04-05', 2100.75),
(6, 'Anna Mueller', 'anna.mueller@email.com', '+49-555-0103', 45, 'germany', '05/04/2024', 2100.75),
(7, 'Raj Patel', 'raj.patel@', '555-0104', NULL, 'India', NULL, 890.25),
(8, 'Sophie Martin', 'sophie.martin@email.com', '+33-555-0105', 31, 'France', '2024-06-15', NULL),
(9, 'Mohamed Ali', 'mohamed.ali@email.com', '+20-555-0106', -5, 'Egypt', '2024-07-20', 1500.00),
(10, NULL, 'unknown@email.com', NULL, 25, 'UK', '2024-08-01', 750.00);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT,
    supplier VARCHAR(100),
    last_updated VARCHAR(50)
);

INSERT INTO products VALUES
(101, 'Laptop Pro 15"', 'Electronics', 1299.99, 45, 'TechCorp Inc.', '2024-01-10'),
(102, 'laptop pro 15"', 'electronics', 1299.99, 45, 'TechCorp Inc', '10/01/2024'),
(103, 'Wireless Mouse', 'Accessories', 29.99, -5, 'GadgetCo', NULL),
(104, 'USB-C Cable', NULL, 0.00, 200, 'CableTech', '2024-02-15'),
(105, 'Gaming Keyboard', 'Accessories', 149.99, 30, NULL, '2024-03-20'),
(106, 'Monitor 27"', 'Electronics', 99999.99, 15, 'DisplayPro', '2024-04-10'),
(107, 'HDMI Cable', 'Accessories', 19.99, NULL, 'CableTech', '15/04/2024'),
(108, 'Webcam HD', 'Electronics', 89.99, 0, '', '2024-05-01'),
(109, 'Desk Lamp', 'Office', -10.50, 60, 'LightCo', NULL),
(110, NULL, 'Electronics', 599.99, 25, 'UnknownSupplier', '2024-06-15');

CREATE TABLE customer_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date VARCHAR(50),
    status VARCHAR(30),
    total_amount DECIMAL(10,2)
);

INSERT INTO customer_orders VALUES
(1001, 1, 101, 2, '2024-05-10', 'Completed', 2599.98),
(1002, 1, 101, 2, '2024-05-10', 'completed', 2599.98),
(1003, 3, 103, 5, NULL, 'Pending', 149.95),
(1004, 999, 104, 1, '2024-06-15', 'Completed', 0.00),
(1005, 5, 105, -3, '15/07/2024', 'SHIPPED', 449.97),
(1006, 7, 106, 1, '2024-08-01', NULL, 99999.99),
(1007, NULL, 107, 2, '2024-08-15', 'Cancelled', 39.98),
(1008, 8, 999, 1, '2024-09-01', 'Completed', 89.99),
(1009, 9, 108, 0, NULL, 'pending', 0.00),
(1010, 10, 109, 5, '2024-10-01', 'Completed', -52.50);

SELECT 'MySQL dirty database created successfully' AS status;
