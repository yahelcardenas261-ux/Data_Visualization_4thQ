-- PostgreSQL Initialization Script
-- This script runs automatically when the container starts for the first time

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT
);

-- Insert sample transaction data
INSERT INTO transactions (category, amount, transaction_date, description) VALUES
    ('Food', 45.50, '2024-01-15', 'Grocery shopping'),
    ('Food', 23.75, '2024-01-18', 'Restaurant lunch'),
    ('Transport', 65.00, '2024-01-16', 'Monthly metro pass'),
    ('Transport', 15.30, '2024-01-20', 'Taxi ride'),
    ('Entertainment', 120.00, '2024-01-17', 'Concert tickets'),
    ('Entertainment', 35.50, '2024-01-22', 'Movie theater'),
    ('Utilities', 89.00, '2024-01-10', 'Electricity bill'),
    ('Utilities', 45.00, '2024-01-12', 'Internet service'),
    ('Healthcare', 150.00, '2024-01-14', 'Doctor visit'),
    ('Shopping', 89.99, '2024-01-19', 'Clothing purchase'),
    ('Shopping', 45.00, '2024-01-23', 'Books'),
    ('Food', 67.80, '2024-01-25', 'Grocery shopping'),
    ('Transport', 22.50, '2024-01-26', 'Gas station'),
    ('Entertainment', 55.00, '2024-01-28', 'Streaming subscriptions');

-- Verify data insertion
SELECT 'PostgreSQL initialization complete!' AS status;
SELECT COUNT(*) AS transaction_count FROM transactions;