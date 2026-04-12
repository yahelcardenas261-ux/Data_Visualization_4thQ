import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("EXERCISE 3: PostgreSQL DATABASE CONNECTION")
print("="*60)

# Step 1: Establish connection to PostgreSQL
print("\nStep 1: Connecting to PostgreSQL database...")
try:
    connection = psycopg2.connect(
        host='localhost',
        port=5432,
        user='datauser',
        password='rootpass123',
        database='finance_db'
    )
    print("✓ Successfully connected to PostgreSQL database")
    print(f"✓ Connected to database: finance_db")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit()

# Step 2: Create cursor and execute query
print("\nStep 2: Executing SQL query...")
cursor = connection.cursor()

sql_query = """
    SELECT 
        category,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount
    FROM transactions
    GROUP BY category
    ORDER BY total_amount DESC
"""

cursor.execute(sql_query)
results = cursor.fetchall()

# Get column names
column_names = [desc[0] for desc in cursor.description]

print(f"✓ Query executed successfully")
print(f"✓ Retrieved {len(results)} category records")

# Step 3: Convert to DataFrame
print("\nStep 3: Processing query results...")
df = pd.DataFrame(results, columns=column_names)
print("\nQuery Results:")
print(df.to_string(index=False))

# Calculate total and percentages
total_amount = df['total_amount'].sum()
df['percentage'] = (df['total_amount'] / total_amount * 100).round(2)

print(f"\nTotal Expenses: ${total_amount:,.2f}")

# Step 4: Create visualization
print("\nStep 4: Creating visualization...")
fig, ax = plt.subplots(figsize=(10, 8))

# Define custom colors (purple-gold theme)
colors = ['#6B46C1', '#9F7AEA', '#D69E2E', '#F6E05E', '#553C9A', '#B794F4']

# Create pie chart
wedges, texts, autotexts = ax.pie(
    df['total_amount'],
    labels=df['category'],
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    pctdistance=0.85
)

# Enhance text styling
for text in texts:
    text.set_fontsize(12)
    text.set_fontweight('bold')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# Add title
plt.title('Expense Distribution by Category', 
          fontsize=16, fontweight='bold', color='#1A202C', pad=20)

# Add center text showing total
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax.add_artist(centre_circle)
ax.text(0, 0, f'Total\n${total_amount:.2f}',
        ha='center', va='center', fontsize=14, fontweight='bold')

plt.tight_layout()

# Save figure
plt.savefig('exercise3_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as: exercise3_visualization.png")
plt.show()

# Step 5: Detailed breakdown
print("\nStep 5: Category Breakdown")
for idx, row in df.iterrows():
    print(f"{row['category']:.<20} ${row['total_amount']:>8,.2f} ({row['percentage']:>5.1f}%)")

print(f"\nHighest Expense Category: {df.iloc[0]['category']} (${df.iloc[0]['total_amount']:,.2f})")
print(f"Lowest Expense Category: {df.iloc[-1]['category']} (${df.iloc[-1]['total_amount']:,.2f})")

# Step 6: Close connection
cursor.close()
connection.close()
print("\n✓ Database connection closed")

print("\n" + "="*60)
print("Exercise 3 Complete!")
print("="*60)