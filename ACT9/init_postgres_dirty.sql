DROP DATABASE IF EXISTS employee_data_raw;
CREATE DATABASE employee_data_raw;
\c employee_data_raw

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date VARCHAR(50),
    performance_score DECIMAL(3,2)
);

INSERT INTO employees VALUES
(1, 'Alice', 'Johnson', 'alice.johnson@company.com', 'Engineering', 85000.00, '2022-01-15', 4.5),
(2, 'alice', 'johnson', 'alice.johnson@company.com', 'engineering', 85000.00, '15/01/2022', 4.5),
(3, 'Bob', NULL, 'bob.unknown@company.com', 'Sales', NULL, '2022-03-20', 3.8),
(4, 'Carol', 'Davis', NULL, 'Marketing', 72000.00, NULL, NULL),
(5, 'David', 'Wilson', 'david.wilson@', 'IT', -50000.00, '2023-01-10', 4.2),
(6, NULL, 'Brown', 'unknown.brown@company.com', 'HR', 68000.00, '2023-02-15', 9.5),
(7, 'Frank', 'Miller', 'frank.miller@company.com', 'engineering', 92000.00, '15/03/2023', 4.1),
(8, 'Grace', 'Taylor', 'grace.taylor@company.com', 'SALES', 999999.99, '2023-04-20', 0.0),
(9, 'Henry', 'Anderson', 'henry.anderson@company.com', '', 78000.00, '2023-05-25', -1.5),
(10, 'Ivy', 'Thomas', 'ivy.thomas@company.com', 'Marketing', 71000.00, '2025-12-31', 3.9),
(11, 'Jack', 'Martinez', 'jack.martinez@company.com', 'Sales', 0.00, NULL, 4.0),
(12, 'Karen', 'Garcia', 'karen.garcia@company.com', 'IT', 88000.00, '2023-08-15', NULL);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    manager_name VARCHAR(100),
    budget DECIMAL(12,2),
    location VARCHAR(100)
);

INSERT INTO departments VALUES
(1, 'Engineering', 'John Smith', 500000.00, 'New York'),
(2, 'engineering', 'John Smith', 500000.00, 'new york'),
(3, 'Sales', NULL, -100000.00, 'Los Angeles'),
(4, 'Marketing', 'Jane Doe', NULL, NULL),
(5, 'IT', 'Mike Johnson', 350000.00, ''),
(6, 'HR', '', 200000.00, 'Chicago'),
(7, NULL, 'Sarah Williams', 400000.00, 'Boston');

SELECT 'PostgreSQL dirty database created successfully' AS status;
