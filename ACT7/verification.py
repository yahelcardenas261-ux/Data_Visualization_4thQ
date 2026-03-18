# Quick script to verify all connections

import mysql.connector
import psycopg2
import pandas as pd
import json
import os

print("="*60)
print("CONNECTION VERIFICATION")
print("="*60)

# Check 1: CSV file exists
print("\n1. Checking CSV file...")
if os.path.exists('sales_data.csv'):
    df = pd.read_csv('sales_data.csv')
    print(f"   ✓ sales_data.csv found ({len(df)} records)")
else:
    print("   ✗ sales_data.csv not found!")

# Check 2: JSON file exists
print("\n2. Checking JSON file...")
if os.path.exists('sensor_data.json'):
    with open('sensor_data.json', 'r') as f:
        data = json.load(f)
    print(f"   ✓ sensor_data.json found ({len(data)} records)")
else:
    print("   ✗ sensor_data.json not found!")

# Check 3: MySQL connection
print("\n3. Testing MySQL connection...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='datauser',
        password='datapass123',
        database='company_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    print(f"   ✓ MySQL connected ({count} employees found)")
    conn.close()
except Exception as e:
    print(f"   ✗ MySQL connection failed: {e}")

# Check 4: PostgreSQL connection
print("\n4. Testing PostgreSQL connection...")
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='datauser',
        password='rootpass123',
        database='finance_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"   ✓ PostgreSQL connected ({count} transactions found)")
    conn.close()
except Exception as e:
    print(f"   ✗ PostgreSQL connection failed: {e}")

print("\n" + "="*60)
print("If all checks passed, you're ready to start!")
print("="*60)