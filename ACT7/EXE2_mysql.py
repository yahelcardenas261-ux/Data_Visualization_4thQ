# Exercise 2: MySQL Database Connection

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("EXERCISE 2: MySQL DATABASE CONNECTION")
print("="*60)

# Step 1: Establish connection to MySQL
print("\nStep 1: Connecting to MySQL database...")
try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='datauser',
        password='datapass123',
        database='company_db'
    )
    print("✓ Successfully connected to MySQL database")
    print(f"✓ Connected to database: company_db")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit()

# Step 2: Create cursor and execute query
print("\nStep 2: Executing SQL query...")
cursor = connection.cursor()

sql_query = """
    SELECT 
        department,
        COUNT(*) as employee_count,
        AVG(salary) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
"""

cursor.execute(sql_query)
results = cursor.fetchall()

# Get column names
column_names = [desc[0] for desc in cursor.description]

print(f"✓ Query executed successfully")
print(f"✓ Retrieved {len(results)} department records")

# Step 3: Convert to DataFrame for easier manipulation
print("\nStep 3: Processing query results...")
df = pd.DataFrame(results, columns=column_names)
print("\nQuery Results:")
print(df.to_string(index=False))

# Step 4: Create visualization
print("\nStep 4: Creating visualization...")
plt.figure(figsize=(10, 6))

# Create horizontal bar chart
bars = plt.barh(df['department'], df['avg_salary'], color='#D69E2E', edgecolor='#1A202C', linewidth=1.5)

# Add value labels on bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 1000, bar.get_y() + bar.get_height()/2,
             f'${width:,.0f}',
             ha='left', va='center', fontsize=10, fontweight='bold')

plt.title('Average Salary by Department', fontsize=16, fontweight='bold', color='#1A202C')
plt.xlabel('Average Salary ($)', fontsize=12)
plt.xlim(0, 120000)
plt.ylabel('Department', fontsize=12)
plt.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()

# Save figure
plt.savefig('exercise2_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as: exercise2_visualization.png")
plt.show()

# Step 5: Additional analysis
print("\nStep 5: Summary Statistics")
print(f"Total Employees: {df['employee_count'].sum()}")
print(f"Highest Avg Salary: {df.iloc[0]['department']} (${df.iloc[0]['avg_salary']:,.2f})")
print(f"Lowest Avg Salary: {df.iloc[-1]['department']} (${df.iloc[-1]['avg_salary']:,.2f})")
print(f"Overall Average: ${df['avg_salary'].mean():,.2f}")

# Step 6: Close connection
cursor.close()
connection.close()
print("\n✓ Database connection closed")

print("\n" + "="*60)
print("Exercise 2 Complete!")
print("="*60)