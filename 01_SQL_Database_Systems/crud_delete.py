# crud_delete.py
# Part D: DELETE - Remove discontinued products

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("="*70)
print("CRUD PART D: DELETE")
print("="*70)

conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='datauser', password='datapass123',
    database='inventory_db'
)
cursor = conn.cursor()

# Count before
cursor.execute("""
    SELECT category, COUNT(*) as count
    FROM productos GROUP BY category
""")
before_counts = cursor.fetchall()
df_before = pd.DataFrame(before_counts, 
                         columns=['Category', 'Count'])
total_before = df_before['Count'].sum()

print("\n1. Current Inventory Status")
print("-"*70)
print(df_before.to_string(index=False))
print(f"\nTotal products: {total_before}")

# Find products to delete
print("\n2. Finding Products for Deletion")
print("-"*70)
cursor.execute("""
    SELECT product_id, name, category, stock
    FROM productos
    WHERE stock < 5
    ORDER BY stock ASC
    LIMIT 3
""")
to_delete = cursor.fetchall()

if not to_delete:
    cursor.execute("""
        INSERT INTO productos (name, category, price, stock, min_stock)
        VALUES ('Demo Product', 'Accessories', 9.99, 1, 0)
    """)
    conn.commit()
    demo_id = cursor.lastrowid
    to_delete = [(demo_id, 'Demo Product', 'Accessories', 1)]

df_delete = pd.DataFrame(to_delete,
    columns=['ID', 'Product', 'Category', 'Stock'])
print(df_delete.to_string(index=False))

# Check foreign key constraints
print("\n3. Checking Foreign Key Constraints")
print("-"*70)
ids = [p[0] for p in to_delete]
placeholders = ','.join(['%s'] * len(ids))

cursor.execute(f"""
    SELECT product_id, COUNT(*) as sale_count
    FROM ventas
    WHERE product_id IN ({placeholders})
    GROUP BY product_id
""", ids)
sales_refs = cursor.fetchall()

if sales_refs:
    print("   ⚠ Some products have sales history")
    for pid, count in sales_refs:
        print(f"      Product ID {pid}: {count} sales")
    
    # Only delete products without sales
    cursor.execute(f"""
        SELECT product_id, name, category, stock
        FROM productos
        WHERE product_id IN ({placeholders})
        AND product_id NOT IN (SELECT DISTINCT product_id FROM ventas)
    """, ids)
    safe_delete = cursor.fetchall()
    
    if not safe_delete:
        print("\n   Creating demo product for deletion...")
        cursor.execute("""
            INSERT INTO productos (name, category, price, stock, min_stock)
            VALUES ('Delete Demo', 'Accessories', 1.99, 1, 0)
        """)
        conn.commit()
        demo_id = cursor.lastrowid
        safe_delete = [(demo_id, 'Delete Demo', 'Accessories', 1)]
    
    to_delete = safe_delete
    ids = [p[0] for p in to_delete]

# Perform DELETE
print("\n4. Executing DELETE Operations")
print("-"*70)

for product in to_delete:
    pid, name = product[0], product[1]
    cursor.execute("DELETE FROM productos WHERE product_id = %s", (pid,))
    print(f"   ✓ Deleted: {name} (ID: {pid})")

conn.commit()
print(f"\n   ✓ Deleted {len(to_delete)} product(s)")

# Count after
cursor.execute("""
    SELECT category, COUNT(*) as count
    FROM productos GROUP BY category
""")
after_counts = cursor.fetchall()
df_after = pd.DataFrame(after_counts,
                        columns=['Category', 'Count'])
total_after = df_after['Count'].sum()

print("\n5. Final Inventory Status")
print("-"*70)
print(df_after.to_string(index=False))
print(f"\nTotal products: {total_after}")
print(f"Products deleted: {total_before - total_after}")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Merge for comparison
df_comp = df_before.merge(df_after, on='Category', how='outer',
                          suffixes=(' Before', ' After')).fillna(0)

categories = df_comp['Category']
x = range(len(categories))
width = 0.35

# Chart 1: Side-by-side
bars1 = ax1.bar([i - width/2 for i in x], df_comp['Count Before'], width,
                label='Before', color='#6B46C1', 
                edgecolor='#1A202C', linewidth=1.5)
bars2 = ax1.bar([i + width/2 for i in x], df_comp['Count After'], width,
                label='After', color='#D69E2E',
                edgecolor='#1A202C', linewidth=1.5)

ax1.set_title('Category Counts: Before vs After DELETE',
              fontsize=12, fontweight='bold')
ax1.set_xlabel('Category', fontsize=11)
ax1.set_ylabel('Count', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, rotation=45, ha='right')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Chart 2: Total comparison
totals = [total_before, total_after]
colors = ['#6B46C1', '#D69E2E']
bars = ax2.bar(['Before DELETE', 'After DELETE'], totals,
               color=colors, edgecolor='#1A202C', linewidth=2)

for bar, total in zip(bars, totals):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
             f'{int(total)}', ha='center', va='bottom',
             fontsize=12, fontweight='bold')

ax2.set_title('Total Product Count', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Products', fontsize=11)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('crud_delete.png', dpi=300, bbox_inches='tight')
print("\n6. Visualization saved: crud_delete.png")
plt.show()

conn.close()
print("\n" + "="*70)
print("DELETE COMPLETE!")
print("="*70)
print("\n" + "="*70)
print("ALL CRUD OPERATIONS COMPLETED SUCCESSFULLY!")
print("="*70)