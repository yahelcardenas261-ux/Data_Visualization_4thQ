# Part A: CREATE - Insert new products

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("="*70)
print("CRUD PART A: CREATE (INSERT)")
print("="*70)

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='datauser', password='datapass123',
    database='inventory_db'
)
cursor = conn.cursor()

# Count products before insertion
cursor.execute("SELECT COUNT(*) FROM productos")
before_count = cursor.fetchone()[0]
print(f"\n1. Products before: {before_count}")

# Insert new products
new_products = [
    ('Google Pixel 8', 'Electronics', 699.99, 12, 5),
    ('Bose QuietComfort Earbuds', 'Audio', 279.99, 28, 12),
    ('Apple Magic Trackpad', 'Accessories', 129.99, 20, 8)
]

insert_query = """
    INSERT INTO productos (name, category, price, stock, min_stock)
    VALUES (%s, %s, %s, %s, %s)
"""

print("\n2. Inserting new products...")
for product in new_products:
    cursor.execute(insert_query, product)
    print(f"   ✓ Inserted: {product[0]} (ID: {cursor.lastrowid})")

# Commit transaction
conn.commit()
print("\n   ✓ All insertions committed!")

# Count after insertion
cursor.execute("SELECT COUNT(*) FROM productos")
after_count = cursor.fetchone()[0]
print(f"\n3. Products after: {after_count}")
print(f"   New products added: {after_count - before_count}")

# Visualization: Category distribution
cursor.execute("""
    SELECT category, COUNT(*) as count
    FROM productos
    GROUP BY category
""")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=['Category', 'Count'])

plt.figure(figsize=(10, 6))
bars = plt.bar(df['Category'], df['Count'], 
               color='#6B46C1', edgecolor='#1A202C', linewidth=1.5)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom', 
             fontsize=11, fontweight='bold')

plt.title('Product Distribution by Category', fontsize=14, fontweight='bold')
plt.xlabel('Category', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('crud_create.png', dpi=300, bbox_inches='tight')
print("\n4. Visualization saved: crud_create.png")
plt.show()

conn.close()
print("\n" + "="*70)
print("CREATE COMPLETE!")
print("="*70)