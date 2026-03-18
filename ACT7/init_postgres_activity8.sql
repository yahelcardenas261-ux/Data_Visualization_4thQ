-- PostgreSQL Initialization Script for Activity 8
-- Sales and Order Management System

DROP SCHEMA IF EXISTS sales_db CASCADE;
CREATE SCHEMA sales_db;
SET search_path TO sales_db;

-- Table: productos
CREATE TABLE productos (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    supplier VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: ordenes
CREATE TABLE ordenes (
    order_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' 
        CHECK (status IN ('pending', 'processing', 'completed', 'cancelled')),
    FOREIGN KEY (product_id) REFERENCES productos(product_id)
);

-- Insert products
INSERT INTO productos (name, category, price, stock, supplier) VALUES
    ('Office Chair Pro', 'Furniture', 299.99, 40, 'ErgoSupply Inc'),
    ('Standing Desk Electric', 'Furniture', 599.99, 15, 'ErgoSupply Inc'),
    ('LED Desk Lamp', 'Accessories', 49.99, 60, 'LightWorks Ltd'),
    ('Wireless Mouse', 'Accessories', 29.99, 80, 'TechGear Co'),
    ('USB-C Hub', 'Accessories', 79.99, 55, 'TechGear Co'),
    ('Ergonomic Keyboard', 'Accessories', 89.99, 45, 'TechGear Co'),
    ('Monitor Arm Mount', 'Accessories', 149.99, 25, 'ErgoSupply Inc'),
    ('Webcam HD', 'Electronics', 119.99, 35, 'VisionTech'),
    ('Microphone USB', 'Electronics', 89.99, 30, 'AudioPro'),
    ('Cable Management Kit', 'Accessories', 24.99, 100, 'OfficePlus');

-- Insert orders
INSERT INTO ordenes (product_id, quantity, order_date, status) VALUES
    (1, 5, '2024-01-20 09:00:00', 'completed'),
    (3, 10, '2024-01-21 10:30:00', 'completed'),
    (4, 15, '2024-01-22 14:15:00', 'processing'),
    (2, 3, '2024-01-23 11:45:00', 'pending'),
    (6, 8, '2024-01-24 16:20:00', 'completed');

-- Create indexes
CREATE INDEX idx_product_category ON productos(category);
CREATE INDEX idx_order_status ON ordenes(status);
CREATE INDEX idx_order_date ON ordenes(order_date);

-- Verify
SELECT 'PostgreSQL initialization complete!' AS status;
SELECT COUNT(*) AS product_count FROM productos;
SELECT COUNT(*) AS order_count FROM ordenes;