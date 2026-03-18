# transaction_commit.py
# Exercise 2: Transaction with COMMIT

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print("="*70)
print("EXERCISE 2: TRANSACTION WITH COMMIT")
print("="*70)

# Connect with autocommit disabled
conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='datauser', password='datapass123',
    database='inventory_db',
    autocommit=False  # CRITICAL: Enables transaction control
)
cursor = conn.cursor()

# Transaction parameters
product_name = 'iPhone 15 Pro'
quantity_to_sell = 2

print(f"\nProcessing Sale: {quantity_to_sell}x {product_name}")
print("="*70)

try:
    # Step 1: BEGIN TRANSACTION (implicit with autocommit=False)
    print("\n1. Starting Transaction...")
    print("   ✓ Transaction initiated (autocommit disabled)")
    
    # Step 2: Lock row and get product info
    print("\n2. Locking Product Row...")
    cursor.execute("""
        SELECT product_id, name, price, stock
        FROM productos
        WHERE name = %s
        FOR UPDATE
    """, (product_name,))
    
    product = cursor.fetchone()
    if not product:
        raise Exception(f"Product '{product_name}' not found")
    
    product_id, name, price, current_stock = product
    print(f"   Product ID: {product_id}")
    print(f"   Current Stock: {current_stock}")
    print(f"   Price: ${price:.2f}")
    print(f"   ✓ Row locked (prevents concurrent modifications)")
    
    # Step 3: Validate stock
    print("\n3. Validating Stock...")
    if current_stock < quantity_to_sell:
        raise Exception(
            f"Insufficient stock! Available: {current_stock}, "
            f"Required: {quantity_to_sell}"
        )
    print(f"   ✓ Validation passed ({current_stock} >= {quantity_to_sell})")
    
    # Step 4: Calculate total
    total_amount = price * quantity_to_sell
    print(f"\n4. Calculating Total...")
    print(f"   Unit Price: ${price:.2f}")
    print(f"   Quantity: {quantity_to_sell}")
    print(f"   Total: ${total_amount:.2f}")
    
    # Step 5: UPDATE inventory (Operation 1)
    print("\n5. Updating Inventory...")
    new_stock = current_stock - quantity_to_sell
    cursor.execute("""
        UPDATE productos
        SET stock = stock - %s
        WHERE product_id = %s
    """, (quantity_to_sell, product_id))
    print(f"   ✓ Stock updated: {current_stock} → {new_stock}")
    print(f"   (Operation 1: UPDATE productos)")
    
    # Step 6: INSERT sale record (Operation 2)
    print("\n6. Creating Sales Record...")
    cursor.execute("""
        INSERT INTO ventas (product_id, quantity, total_amount)
        VALUES (%s, %s, %s)
    """, (product_id, quantity_to_sell, total_amount))
    sale_id = cursor.lastrowid
    print(f"   ✓ Sale record created (ID: {sale_id})")
    print(f"   (Operation 2: INSERT INTO ventas)")
    
    # Step 7: COMMIT transaction
    print("\n7. Committing Transaction...")
    print("   Both operations successful - committing...")
    conn.commit()
    print("   ✓ TRANSACTION COMMITTED")
    print("   ✓ Changes are now PERMANENT and DURABLE")
    
    # Step 8: Verify changes persisted
    print("\n8. Verifying Transaction Results...")
    cursor.execute("""
        SELECT stock FROM productos WHERE product_id = %s
    """, (product_id,))
    verified_stock = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT sale_id, quantity, total_amount, sale_date
        FROM ventas WHERE sale_id = %s
    """, (sale_id,))
    sale_record = cursor.fetchone()
    
    print(f"   Product Stock: {verified_stock}")
    print(f"   Sale Record: ID={sale_record[0]}, Qty={sale_record[1]}, "
          f"Total=${sale_record[2]:.2f}")
    print(f"   ✓ Transaction verified!")
    
    # Step 9: Demonstrate ACID properties
    print("\n9. ACID Properties Demonstrated:")
    print("="*70)
    print("   [A] ATOMICITY:")
    print("       Both UPDATE and INSERT completed as ONE unit")
    print("       If either had failed, BOTH would have been rolled back")
    print("       No partial completion possible")
    print()
    print("   [C] CONSISTENCY:")
    print(f"       Stock decreased by {quantity_to_sell}")
    print(f"       Sale recorded for {quantity_to_sell} units")
    print("       Database remains in valid state (no negative stock)")
    print("       Foreign key relationship maintained")
    print()
    print("   [I] ISOLATION:")
    print("       FOR UPDATE clause locked the product row")
    print("       Other transactions could not modify this product")
    print("       Prevented race conditions (two users buying last item)")
    print()
    print("   [D] DURABILITY:")
    print("       After COMMIT, changes are permanent")
    print("       Will persist even if database crashes")
    print("       Written to transaction log and disk")
    
   # ... (todo el código anterior igual hasta el Paso 10)

    # Step 10: Visualization
    print("\n10. Creating Transaction Visualization...")
    
    # Get recent sales
    cursor.execute("""
        SELECT v.sale_id, p.name, v.quantity, v.total_amount, v.sale_date
        FROM ventas v
        JOIN productos p ON v.product_id = p.product_id
        ORDER BY v.sale_date DESC
        LIMIT 10
    """)
    recent_sales = cursor.fetchall()
    df_sales = pd.DataFrame(recent_sales,
        columns=['Sale ID', 'Product', 'Qty', 'Amount', 'Date'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Chart 1: Recent sales (highlight new one)
    colors = ['#D69E2E' if i == 0 else '#6B46C1' 
              for i in range(len(df_sales))]
    bars = ax1.barh(range(len(df_sales)), df_sales['Amount'],
                    color=colors, edgecolor='#1A202C', linewidth=1.5)
    
    ax1.set_yticks(range(len(df_sales)))
    ax1.set_yticklabels([f"Sale {sid}" for sid in df_sales['Sale ID']])
    ax1.set_xlabel('Sale Amount ($)', fontsize=11)
    ax1.set_title('Recent Sales (Latest in Gold)',
                  fontsize=12, fontweight='bold')
    ax1.invert_yaxis()
    ax1.grid(axis='x', alpha=0.3)
    
    # --- AJUSTE 1: Dar espacio a los textos de los montos ---
    if not df_sales.empty:
        max_amount = df_sales['Amount'].max()
        ax1.set_xlim(0, max_amount * 1.25) # 25% de espacio extra a la derecha
    
    for i, v in enumerate(df_sales['Amount']):
        ax1.text(v + (max_amount * 0.02), i, f'${v:.2f}',
                va='center', fontsize=9, fontweight='bold')
    
    # Chart 2: Stock before/after
    stock_data = {
        'Status': ['Before Transaction', 'After Transaction'],
        'Stock': [current_stock, verified_stock]
    }
    df_stock = pd.DataFrame(stock_data)
    
    bars = ax2.bar(df_stock['Status'], df_stock['Stock'],
                   color=['#6B46C1', '#D69E2E'],
                   edgecolor='#1A202C', linewidth=2)
    
    # --- AJUSTE 2: Dar espacio superior para la anotación ---
    ax2.set_ylim(0, max(current_stock, verified_stock) * 1.2)

    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Stock Quantity', fontsize=11)
    ax2.set_title(f'Stock Impact for {product_name}',
                  fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add change annotation
    ax2.annotate(f'-{quantity_to_sell}',
                xy=(0.5, (current_stock + verified_stock)/2),
                xytext=(0.5, (current_stock + verified_stock)/2 + (max(current_stock, verified_stock) * 0.15)),
                ha='center', fontsize=12, fontweight='bold',
                color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    # --- AJUSTE 3: Asegurar que nada se corte en los bordes ---
    plt.tight_layout()
    fig.subplots_adjust(right=0.95) # Margen extra a la derecha
    
    plt.savefig('transaction_commit.png', dpi=300, bbox_inches='tight')
    print("   ✓ Visualization saved: transaction_commit.png")
    plt.show()


except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("   Rolling back transaction...")
    conn.rollback()
    print("   ✓ Transaction rolled back - no changes made")

finally:
    cursor.close()
    conn.close()

print("\n" + "="*70)
print("EXERCISE 2: TRANSACTION COMMIT - COMPLETE!")
print("="*70)