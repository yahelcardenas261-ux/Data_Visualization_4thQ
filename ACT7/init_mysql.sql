-- MySQL Initialization Script
-- This script runs automatically when the container starts for the first time

USE company_db;

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    hire_date DATE NOT NULL
);

-- Insert sample employee data
INSERT INTO employees (name, department, salary, hire_date) VALUES
    ('Alice Johnson', 'Engineering', 95000.00, '2020-01-15'),
    ('Bob Smith', 'Engineering', 88000.00, '2019-06-20'),
    ('Carol White', 'Engineering', 102000.00, '2018-03-10'),
    ('David Brown', 'Marketing', 72000.00, '2021-02-01'),
    ('Emma Davis', 'Marketing', 68000.00, '2020-09-15'),
    ('Frank Miller', 'Sales', 85000.00, '2019-11-30'),
    ('Grace Lee', 'Sales', 78000.00, '2021-04-22'),
    ('Henry Wilson', 'Sales', 92000.00, '2018-07-18'),
    ('Iris Martinez', 'HR', 65000.00, '2020-12-05'),
    ('Jack Anderson', 'HR', 58000.00, '2021-08-10'),
    ('Karen Taylor', 'Engineering', 98000.00, '2019-02-28'),
    ('Leo Garcia', 'Marketing', 75000.00, '2020-05-17');

-- Verify data insertion
SELECT 'MySQL initialization complete!' AS status;
SELECT COUNT(*) AS employee_count FROM employees;