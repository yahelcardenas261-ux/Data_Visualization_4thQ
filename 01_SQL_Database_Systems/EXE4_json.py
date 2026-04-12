import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("EXERCISE 4: JSON FILE CONNECTION")
print("="*60)

# Step 1: Read JSON file
print("\nStep 1: Reading JSON file...")
with open('sensor_data.json', 'r') as file:
    data = json.load(file)

print(f"✓ Successfully loaded {len(data)} sensor records")

# Step 2: Convert to DataFrame for easier analysis
print("\nStep 2: Converting to DataFrame...")
df = pd.DataFrame(data)

print(f"✓ DataFrame created with shape: {df.shape}")
print(f"✓ Columns: {list(df.columns)}")

print("\nFirst 5 records:")
print(df.head())

# Step 3: Basic statistics
print("\nStep 3: Statistical Summary")
print("\nTemperature Statistics:")
print(f"  Mean: {df['temperature'].mean():.2f}°C")
print(f"  Std Dev: {df['temperature'].std():.2f}°C")
print(f"  Min: {df['temperature'].min():.2f}°C")
print(f"  Max: {df['temperature'].max():.2f}°C")

print("\nHumidity Statistics:")
print(f"  Mean: {df['humidity'].mean():.2f}%")
print(f"  Std Dev: {df['humidity'].std():.2f}%")
print(f"  Min: {df['humidity'].min():.2f}%")
print(f"  Max: {df['humidity'].max():.2f}%")

# Step 4: Create visualization
print("\nStep 4: Creating scatter plot...")
plt.figure(figsize=(10, 7))

# Create scatter plot colored by location
locations = df['location'].unique()
colors = ['#6B46C1', '#D69E2E', '#9F7AEA']

for i, location in enumerate(locations):
    location_data = df[df['location'] == location]
    plt.scatter(location_data['temperature'], 
                location_data['humidity'],
                c=colors[i],
                label=location,
                s=100,
                alpha=0.6,
                edgecolors='black',
                linewidth=0.5)

# Add trend line
z = np.polyfit(df['temperature'], df['humidity'], 1)
p = np.poly1d(z)
plt.plot(df['temperature'], p(df['temperature']),
         "r--", linewidth=2, alpha=0.8,
         label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')

plt.title('Temperature vs Humidity - IoT Sensor Data',
          fontsize=16, fontweight='bold', color='#1A202C')
plt.xlabel('Temperature (°C)', fontsize=12)
plt.ylabel('Humidity (%)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

# Save figure
plt.savefig('exercise4_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as: exercise4_visualization.png")
plt.show()

# Step 5: Correlation analysis
print("\nStep 5: Correlation Analysis")
correlation = df['temperature'].corr(df['humidity'])
print(f"Pearson Correlation Coefficient: {correlation:.4f}")

if correlation < -0.5:
    interpretation = "Strong negative correlation"
elif correlation < -0.3:
    interpretation = "Moderate negative correlation"
elif correlation < 0.3:
    interpretation = "Weak or no correlation"
elif correlation < 0.5:
    interpretation = "Moderate positive correlation"
else:
    interpretation = "Strong positive correlation"

print(f"Interpretation: {interpretation}")

# Step 6: Location breakdown
print("\nStep 6: Readings by Location")
location_counts = df['location'].value_counts()
for location, count in location_counts.items():
    avg_temp = df[df['location'] == location]['temperature'].mean()
    avg_humidity = df[df['location'] == location]['humidity'].mean()
    print(f"{location}: {count} readings | Avg Temp: {avg_temp:.2f}°C | Avg Humidity: {avg_humidity:.2f}%")

print("\n" + "="*60)
print("Exercise 4 Complete!")
print("="*60)