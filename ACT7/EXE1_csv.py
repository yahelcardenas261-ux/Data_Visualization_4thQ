import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("EXERCISE 1: CSV FILE CONNECTION")
print("="*60)

# Step 1: Connect to CSV file (read into DataFrame)
print("\nStep 1: Reading CSV file...")
df = pd.read_csv('sales_data.csv')

print(f"✓ Successfully loaded {len(df)} records")
print(f"✓ Columns: {list(df.columns)}")

# Step 2: Display basic information
print("\nStep 2: Data Overview")
print(df.head(10))
print(f"\nData shape: {df.shape}")
print(f"\nData types:\n{df.dtypes}")

# Step 3: Calculate total revenue per month
print("\nStep 3: Calculating monthly totals...")
monthly_revenue = df.groupby('Month')['Revenue'].sum().reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])

print(monthly_revenue)

# Step 4: Create visualization
print("\nStep 4: Creating visualization...")
plt.figure(figsize=(12, 6))
plt.plot(monthly_revenue.index, monthly_revenue.values, 
         marker='o', linewidth=2, markersize=8, color='#6B46C1')

plt.title('Monthly Sales Revenue Trend', fontsize=16, fontweight='bold', color='#1A202C')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

# Save figure
plt.savefig('exercise1_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as: exercise1_visualization.png")
plt.show()

# Step 5: Summary statistics
print("\nStep 5: Summary Statistics")
print(f"Total Revenue (all months): ${monthly_revenue.sum():,.2f}")
print(f"Average Monthly Revenue: ${monthly_revenue.mean():,.2f}")
print(f"Highest Revenue Month: {monthly_revenue.idxmax()} (${monthly_revenue.max():,.2f})")
print(f"Lowest Revenue Month: {monthly_revenue.idxmin()} (${monthly_revenue.min():,.2f})")

print("\n" + "="*60)
print("Exercise 1 Complete!")
print("="*60)