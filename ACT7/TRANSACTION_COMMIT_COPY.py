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
    autocommit=False
)
cursor = conn.cursor()

# Transaction parameters
product_name = 'iPhone 15 Pro'
quantity_to_sell = 2

try:
    # 1-7: Transaction logic
    cursor.execute("""
        SELECT product_id, name, price, stock
        FROM productos WHERE name = %s FOR UPDATE
    """, (product_name,))
    
    product = cursor.fetchone()
    if not product:
        raise Exception(f"Product '{product_name}' not found")
    
    product_id, name, price, current_stock = product
    total_amount = price * quantity_to_sell
    
    # Update inventory
    cursor.execute("UPDATE productos SET stock = stock - %s WHERE product_id = %s", 
                   (quantity_to_sell, product_id))
    
    # Insert sale
    cursor.execute("INSERT INTO ventas (product_id, quantity, total_amount) VALUES (%s, %s, %s)", 
                   (product_id, quantity_to_sell, total_amount))
    
    conn.commit()
    print("   ✓ TRANSACTION COMMITTED")

    # Step 8: Verify results
    cursor.execute("SELECT stock FROM productos WHERE product_id = %s", (product_id,))
    verified_stock = cursor.fetchone()[0]

    # Step 10: Visualization (DENTRO DEL TRY PARA QUE FUNCIONE BIEN)
    print("\n10. Creating Transaction Visualization...")
    
    cursor.execute("""
        SELECT v.sale_id, p.name, v.quantity, v.total_amount, v.sale_date
        FROM ventas v
        JOIN productos p ON v.product_id = p.product_id
        ORDER BY v.sale_date DESC LIMIT 10
    """)
    recent_sales = cursor.fetchall()
    df_sales = pd.DataFrame(recent_sales, columns=['Sale ID', 'Product', 'Qty', 'Amount', 'Date'])
    
    # SOLUCIÓN AL ERROR DE TIPO: Convertir a float
    df_sales['Amount'] = df_sales['Amount'].astype(float)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Ventas recientes
    colors = ['#D69E2E' if i == 0 else '#6B46C1' for i in range(len(df_sales))]
    ax1.barh(range(len(df_sales)), df_sales['Amount'], color=colors, edgecolor='#1A202C')
    ax1.set_yticks(range(len(df_sales)))
    ax1.set_yticklabels([f"Sale {sid}" for sid in df_sales['Sale ID']])
    ax1.invert_yaxis()
    
    # AJUSTE 1: Espacio extra en eje X para que el texto no se corte
    if not df_sales.empty:
        max_amount = df_sales['Amount'].max()
        ax1.set_xlim(0, max_amount * 1.35) 
        for i, v in enumerate(df_sales['Amount']):
            ax1.text(v + (max_amount * 0.02), i, f'${v:.2f}', va='center', fontweight='bold')

    # Gráfico 2: Impacto de Stock
    stock_data = {'Status': ['Before', 'After'], 'Stock': [float(current_stock), float(verified_stock)]}
    df_stock = pd.DataFrame(stock_data)
    
    # AJUSTE 2: Espacio extra en eje Y para la flecha roja
    ax2.set_ylim(0, max(df_stock['Stock']) * 1.35)
    
    bars = ax2.bar(df_stock['Status'], df_stock['Stock'], color=['#6B46C1', '#D69E2E'], edgecolor='#1A202C')
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{int(bar.get_height())}', ha='center', fontweight='bold')

    # Anotación de la resta
    mid_point = (float(current_stock) + float(verified_stock)) / 2
    ax2.annotate(f'-{quantity_to_sell}', xy=(0.5, mid_point), 
                xytext=(0.5, mid_point + (max(df_stock['Stock']) * 0.2)),
                ha='center', fontsize=12, fontweight='bold', color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

    plt.tight_layout()
    fig.subplots_adjust(right=0.95)
    plt.savefig('transaction_commit.png', dpi=300, bbox_inches='tight')
    plt.show()

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()