-- MySQL Initialization Script for Activity 8
-- Sales and Inventory Management System

DROP DATABASE IF EXISTS inventory_db;
CREATE DATABASE inventory_db;
USE inventory_db;

-- Table: productos (Products)
CREATE TABLE productos (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    min_stock INT NOT NULL DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: ventas (Sales)
CREATE TABLE ventas (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount > 0),
    FOREIGN KEY (product_id) REFERENCES productos(product_id)
);

-- Insert initial product data
INSERT INTO productos (name, category, price, stock, min_stock) VALUES
    ('Laptop Dell XPS 13', 'Electronics', 1299.99, 15, 5),
    ('iPhone 15 Pro', 'Electronics', 999.99, 25, 10),
    ('Samsung Galaxy S24', 'Electronics', 899.99, 20, 10),
    ('Sony WH-1000XM5 Headphones', 'Audio', 349.99, 30, 15),
    ('iPad Air', 'Electronics', 599.99, 18, 8),
    ('MacBook Pro 14"', 'Electronics', 1999.99, 10, 5),
    ('AirPods Pro', 'Audio', 249.99, 50, 20),
    ('Dell Monitor 27"', 'Accessories', 299.99, 22, 10),
    ('Logitech MX Master 3', 'Accessories', 99.99, 45, 20),
    ('Mechanical Keyboard', 'Accessories', 149.99, 35, 15);

-- Insert historical sales
INSERT INTO ventas (product_id, quantity, sale_date, total_amount) VALUES
    (1, 2, '2024-01-15 10:30:00', 2599.98),
    (2, 1, '2024-01-16 14:20:00', 999.99),
    (4, 3, '2024-01-17 09:15:00', 1049.97),
    (7, 2, '2024-01-18 16:45:00', 499.98),
    (3, 1, '2024-01-19 11:30:00', 899.99);

-- Create indexes
CREATE INDEX idx_category ON productos(category);
CREATE INDEX idx_sale_date ON ventas(sale_date);
CREATE INDEX idx_product_sales ON ventas(product_id);

-- Verify
SELECT 'MySQL initialization complete!' AS status;
SELECT COUNT(*) AS product_count FROM productos;
SELECT COUNT(*) AS sales_count FROM ventas;