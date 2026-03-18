# crud_read.py
# Part B: READ - Complex queries with JOIN

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("="*70)
print("CRUD PART B: READ (SELECT with JOIN)")
print("="*70)

conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='datauser', password='datapass123',
    database='inventory_db'
)
cursor = conn.cursor()

# Query 1: Sales with product details (JOIN)
print("\n1. Sales History with Product Details")
print("-"*70)
query = """
    SELECT 
        v.sale_id,
        p.name AS product_name,
        p.category,
        v.quantity,
        p.price,
        v.total_amount,
        v.sale_date
    FROM ventas v
    INNER JOIN productos p ON v.product_id = p.product_id
    ORDER BY v.sale_date DESC
"""

cursor.execute(query)
results = cursor.fetchall()
df_sales = pd.DataFrame(results, 
    columns=['Sale ID', 'Product', 'Category', 'Qty', 
             'Unit Price', 'Total', 'Date'])
print(df_sales.to_string(index=False))

# Query 2: Revenue by category
print("\n2. Revenue Analysis by Category")
print("-"*70)
query_revenue = """
    SELECT 
        p.category,
        COUNT(v.sale_id) AS total_sales,
        SUM(v.quantity) AS units_sold,
        SUM(v.total_amount) AS total_revenue
    FROM ventas v
    INNER JOIN productos p ON v.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
"""

cursor.execute(query_revenue)
revenue_data = cursor.fetchall()
df_revenue = pd.DataFrame(revenue_data,
    columns=['Category', 'Sales', 'Units', 'Revenue'])
print(df_revenue.to_string(index=False))

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Revenue by category
ax1.barh(df_revenue['Category'], df_revenue['Revenue'],
         color='#D69E2E', edgecolor='#1A202C', linewidth=1.5)
ax1.set_title('Revenue by Category', fontsize=13, fontweight='bold')
ax1.set_xlabel('Revenue ($)', fontsize=11)
ax1.set_ylabel('Category', fontsize=11)
ax1.grid(axis='x', alpha=0.3)

for i, v in enumerate(df_revenue['Revenue']):
    ax1.text(float(v) + 50, i, f'${v:,.2f}', 
             va='center', fontsize=10, fontweight='bold')

# Chart 2: Units sold
ax2.bar(df_revenue['Category'], df_revenue['Units'],
        color='#6B46C1', edgecolor='#1A202C', linewidth=1.5)
ax2.set_title('Units Sold by Category', fontsize=13, fontweight='bold')
ax2.set_xlabel('Category', fontsize=11)
ax2.set_ylabel('Units', fontsize=11)
ax2.grid(axis='y', alpha=0.3)

for i, v in enumerate(df_revenue['Units']):
    ax2.text(i, float(v) + 0.2, str(int(v)),
             ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('crud_read.png', dpi=300, bbox_inches='tight')
print("\n3. Visualization saved: crud_read.png")
plt.show()

conn.close()
print("\n" + "="*70)
print("READ COMPLETE!")
print("="*70)