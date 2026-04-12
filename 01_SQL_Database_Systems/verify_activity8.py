import mysql.connector
import psycopg2

print("="*60)
print("ACTIVITY 8 SETUP VERIFICATION")
print("="*60)

# Test MySQL
print("\n1. Testing MySQL...")
try:
    conn = mysql.connector.connect(
        host='localhost', port=3306,
        user='datauser', password='datapass123',
        database='inventory_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    print(f"   ✓ MySQL Connected")
    print(f"   ✓ Products in inventory: {count}")
    cursor.execute("SELECT COUNT(*) FROM ventas")
    sales = cursor.fetchone()[0]
    print(f"   ✓ Sales records: {sales}")
    conn.close()
except Exception as e:
    print(f"   ✗ MySQL Error: {e}")

# Test PostgreSQL
print("\n2. Testing PostgreSQL...")
try:
    conn = psycopg2.connect(
        host='localhost', port=5432,
        user='datauser', password='rootpass123',
        database='postgres', options='-c search_path=sales_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    print(f"   ✓ PostgreSQL Connected")
    print(f"   ✓ Products in catalog: {count}")
    cursor.execute("SELECT COUNT(*) FROM ordenes")
    orders = cursor.fetchone()[0]
    print(f"   ✓ Orders in system: {orders}")
    conn.close()
except Exception as e:
    print(f"   ✗ PostgreSQL Error: {e}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE - READY TO START!")
print("="*60)