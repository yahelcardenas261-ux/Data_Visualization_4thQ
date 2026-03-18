import requests
import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("EXERCISE 5: PUBLIC API CONNECTION - JSONPlaceholder")
print("="*60)

# Step 1: Connect to API and retrieve data
print("\nStep 1: Connecting to JSONPlaceholder API...")
api_url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise exception for bad status codes
    print(f"✓ API request successful (Status Code: {response.status_code})")
except Exception as e:
    print(f"✗ API request failed: {e}")
    exit()

# Step 2: Parse JSON response
print("\nStep 2: Parsing JSON response...")
posts = response.json()
print(f"✓ Retrieved {len(posts)} posts")

# Step 3: Convert to DataFrame
print("\nStep 3: Converting to DataFrame...")
df = pd.DataFrame(posts)
print(f"✓ DataFrame created with shape: {df.shape}")
print(f"✓ Columns: {list(df.columns)}")

print("\nFirst 3 posts:")
print(df.head(3))

# Step 4: Analyze data - posts per user
print("\nStep 4: Analyzing posts per user...")
posts_per_user = df['userId'].value_counts().sort_index()
print("\nPosts per User:")
print(posts_per_user)

# Step 5: Create visualization
print("\nStep 5: Creating visualization...")
plt.figure(figsize=(12, 6))

bars = plt.bar(posts_per_user.index, posts_per_user.values,
               color='#6B46C1', edgecolor='#1A202C', linewidth=1.5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title('Number of Posts per User (API Data)',
          fontsize=16, fontweight='bold', color='#1A202C')
plt.xlabel('User ID', fontsize=12)
plt.ylabel('Number of Posts', fontsize=12)
plt.xticks(posts_per_user.index)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()

# Save figure
plt.savefig('exercise5_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as: exercise5_visualization.png")
plt.show()

# Step 6: Additional insights
print("\nStep 6: Data Insights")
print(f"Total Users: {df['userId'].nunique()}")
print(f"Total Posts: {len(df)}")
print(f"Average Posts per User: {len(df) / df['userId'].nunique():.1f}")
print(f"User with Most Posts: User {posts_per_user.idxmax()} ({posts_per_user.max()} posts)")
print(f"Average Title Length: {df['title'].str.len().mean():.1f} characters")
print(f"Average Body Length: {df['body'].str.len().mean():.1f} characters")

print("\n" + "="*60)
print("Exercise 5 Complete!")
print("="*60)