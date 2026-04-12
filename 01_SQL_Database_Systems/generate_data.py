# Script to create synthetic CSV and JSON data files

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# ============================================
# GENERATE CSV FILE: Monthly Sales Data
# ============================================
print("Generating CSV file: sales_data.csv")

# Create 12 months of sales data
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

products = ['Product_A', 'Product_B', 'Product_C']
sales_records = []

for month in months:
    for product in products:
        # Generate random sales quantity and price
        quantity = np.random.randint(50, 200)
        price = np.random.uniform(15.0, 50.0)
        revenue = quantity * price
        
        sales_records.append({
            'Month': month,
            'Product': product,
            'Quantity': quantity,
            'Price': round(price, 2),
            'Revenue': round(revenue, 2)
        })

# Create DataFrame and save to CSV
df_sales = pd.DataFrame(sales_records)
df_sales.to_csv('sales_data.csv', index=False)
print(f"  -> Created sales_data.csv with {len(df_sales)} records")

# ============================================
# GENERATE JSON FILE: IoT Sensor Data
# ============================================
print("\nGenerating JSON file: sensor_data.json")

# Create 100 sensor readings
sensor_data = []
base_time = datetime.now()

for i in range(100):
    timestamp = base_time + timedelta(minutes=i*5)
    
    # Generate correlated temperature and humidity
    temperature = np.random.uniform(18.0, 32.0)
    # Humidity inversely correlated with temperature
    humidity = 90 - (temperature - 18) * 2.5 + np.random.uniform(-5, 5)
    humidity = max(30, min(100, humidity))  # Clamp between 30-100
    
    sensor_data.append({
        'timestamp': timestamp.isoformat(),
        'sensor_id': f'SENSOR_{(i % 5) + 1:03d}',
        'temperature': round(temperature, 2),
        'humidity': round(humidity, 2),
        'location': np.random.choice(['Zone_A', 'Zone_B', 'Zone_C'])
    })

# Save to JSON file
with open('sensor_data.json', 'w') as f:
    json.dump(sensor_data, f, indent=2)

print(f"  -> Created sensor_data.json with {len(sensor_data)} records")

# ============================================
# DISPLAY SAMPLE DATA
# ============================================
print("\n" + "="*60)
print("SAMPLE DATA PREVIEW")
print("="*60)

print("\nCSV File (first 5 rows):")
print(df_sales.head())

print("\nJSON File (first 2 records):")
print(json.dumps(sensor_data[:2], indent=2))

print("\n" + "="*60)
print("Data generation complete!")
print("="*60)