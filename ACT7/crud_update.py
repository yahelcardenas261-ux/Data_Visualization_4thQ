# crud_update.py
# Part C: UPDATE - Modify product stock

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("="*70)
print("CRUD PART C: UPDATE")
print("="*70)

conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='datauser', password='datapass123',
    database='inventory_db'
)
cursor = conn.cursor()

# Find products needing restock
print("\n1. Products Needing Restock")
print("-"*70)
cursor.execute("""
    SELECT product_id, name, stock, min_stock
    FROM productos
    WHERE stock < min_stock
    LIMIT 5
""")
products = cursor.fetchall()

if not products:
    # Create test scenario
    cursor.execute("""
        UPDATE productos SET stock = 3 
        WHERE product_id IN (1, 2, 3)
    """)
    conn.commit()
    cursor.execute("""
        SELECT product_id, name, stock, min_stock
        FROM productos
        WHERE stock < min_stock
        LIMIT 5
    """)
    products = cursor.fetchall()

df_before = pd.DataFrame(products,
    columns=['ID', 'Product', 'Current', 'Minimum'])
print(df_before.to_string(index=False))

# Perform UPDATE operations
print("\n2. Updating Stock Levels...")
print("-"*70)

updates = []
for product in products:
    pid, name, stock, min_stock = product
    qty_add = (min_stock + 10) - stock
    
    cursor.execute("""
        UPDATE productos
        SET stock = stock + %s
        WHERE product_id = %s
    """, (qty_add, pid))
    
    updates.append({
        'id': pid, 'name': name,
        'old': stock, 'new': stock + qty_add,
        'added': qty_add
    })
    print(f"   ✓ {name}: {stock} → {stock + qty_add} (+{qty_add})")

conn.commit()
print("\n   ✓ All updates committed!")

# Verify updates
print("\n3. Verification")
print("-"*70)
ids = [u['id'] for u in updates]
placeholders = ','.join(['%s'] * len(ids))
cursor.execute(f"""
    SELECT product_id, name, stock, min_stock
    FROM productos
    WHERE product_id IN ({placeholders})
""", ids)

verified = cursor.fetchall()
df_after = pd.DataFrame(verified,
    columns=['ID', 'Product', 'Current', 'Minimum'])
print(df_after.to_string(index=False))

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(updates))
width = 0.35

old_stocks = [u['old'] for u in updates]
new_stocks = [u['new'] for u in updates]
names = [u['name'][:30] for u in updates]

bars1 = ax.bar([i - width/2 for i in x], old_stocks, width,
               label='Before', color='#DC143C', 
               edgecolor='#1A202C', linewidth=1.5)
bars2 = ax.bar([i + width/2 for i in x], new_stocks, width,
               label='After', color='#6B46C1',
               edgecolor='#1A202C', linewidth=1.5)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, fontweight='bold')

ax.set_title('Stock Levels: Before vs After UPDATE',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Product', fontsize=11)
ax.set_ylabel('Stock Quantity', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('crud_update.png', dpi=300, bbox_inches='tight')
print("\n4. Visualization saved: crud_update.png")
plt.show()

conn.close()
print("\n" + "="*70)
print("UPDATE COMPLETE!")
print("="*70)