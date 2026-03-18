# data_quality_assessment.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import psycopg2
from collections import Counter

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

def connect_to_databases():
    """Establish connections to both databases"""
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="datauser",
        password="datapass123",
        database="sales_data_raw"
    )
    
    pg_conn = psycopg2.connect(
        host="localhost",
        user="datauser",
        password="rootpass123",
        database="employee_data_raw"
    )
    
    return mysql_conn, pg_conn

def profile_dataframe(df, table_name):
    """Generate comprehensive data quality profile"""
    profile = {
        'table_name': table_name,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    
    # Check for negative values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    profile['negative_values'] = {}
    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            profile['negative_values'][col] = neg_count
    
    # Check for zero values in amount/price columns
    profile['zero_values'] = {}
    for col in numeric_cols:
        zero_count = (df[col] == 0).sum()
        if zero_count > 0:
            profile['zero_values'][col] = zero_count
    
    # Check for empty strings
    string_cols = df.select_dtypes(include=[object]).columns
    profile['empty_strings'] = {}
    for col in string_cols:
        empty_count = (df[col] == '').sum()
        if empty_count > 0:
            profile['empty_strings'][col] = empty_count
    
    return profile

def detect_duplicates_details(df, table_name):
    """Detailed duplicate analysis"""
    if df.duplicated().sum() > 0:
        duplicates = df[df.duplicated(keep=False)].sort_values(by=df.columns[0])
        print(f"\n=== Duplicates in {table_name} ===")
        print(duplicates)
        return duplicates
    return None

def visualize_quality_issues(profiles):
    """Create comprehensive quality issue visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Data Quality Assessment - Overview', fontsize=16, fontweight='bold')
    
    # Plot 1: Missing Values Heatmap
    ax1 = axes[0, 0]
    missing_data = []
    labels = []
    for profile in profiles:
        table = profile['table_name']
        for col, pct in profile['missing_percentage'].items():
            if pct > 0:
                missing_data.append(pct)
                labels.append(f"{table}.{col}")
    
    if missing_data:
        y_pos = np.arange(len(labels))
        bars = ax1.barh(y_pos, missing_data, color='#E53E3E', alpha=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(labels, fontsize=9)
        ax1.set_xlabel('Missing Data (%)', fontweight='bold')
        ax1.set_title('Missing Values by Column', fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Add percentage labels
        for bar, val in zip(bars, missing_data):
            ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=8)
    
    # Plot 2: Quality Issue Summary
    ax2 = axes[0, 1]
    issue_types = ['Missing', 'Duplicates', 'Negative', 'Zero', 'Empty Strings']
    issue_counts = [
        sum(len(p['missing_values']) for p in profiles),
        sum(p['duplicate_rows'] for p in profiles),
        sum(len(p.get('negative_values', {})) for p in profiles),
        sum(len(p.get('zero_values', {})) for p in profiles),
        sum(len(p.get('empty_strings', {})) for p in profiles)
    ]
    
    colors = ['#E53E3E', '#DD6B20', '#D69E2E', '#38B2AC', '#805AD5']
    bars = ax2.bar(issue_types, issue_counts, color=colors, alpha=0.7)
    ax2.set_ylabel('Number of Affected Columns', fontweight='bold')
    ax2.set_title('Data Quality Issues by Type', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add count labels
    for bar, count in zip(bars, issue_counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: Row Count by Table
    ax3 = axes[1, 0]
    table_names = [p['table_name'] for p in profiles]
    row_counts = [p['total_rows'] for p in profiles]
    bars = ax3.bar(table_names, row_counts, color='#6B46C1', alpha=0.7)
    ax3.set_ylabel('Number of Rows', fontweight='bold')
    ax3.set_title('Dataset Sizes', fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, count in zip(bars, row_counts):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 4: Data Completeness Score
    ax4 = axes[1, 1]
    completeness_scores = []
    for profile in profiles:
        total_cells = profile['total_rows'] * profile['total_columns']
        missing_cells = sum(profile['missing_values'].values())
        completeness = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0
        completeness_scores.append(completeness)
    
    bars = ax4.barh(table_names, completeness_scores, color='#48BB78', alpha=0.7)
    ax4.set_xlabel('Completeness (%)', fontweight='bold')
    ax4.set_title('Data Completeness by Table', fontweight='bold')
    ax4.set_xlim(0, 100)
    ax4.grid(axis='x', alpha=0.3)
    
    for bar, score in zip(bars, completeness_scores):
        ax4.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{score:.1f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('data_quality_assessment.png', dpi=300, bbox_inches='tight')
    print("\n✓ Quality assessment visualization saved as 'data_quality_assessment.png'")
    plt.show()

def print_quality_report(profile):
    """Print detailed quality report"""
    print(f"\n{'='*60}")
    print(f"DATA QUALITY REPORT: {profile['table_name']}")
    print(f"{ '='*60}")
    print(f"Total Rows: {profile['total_rows']}")
    print(f"Total Columns: {profile['total_columns']}")
    print(f"Duplicate Rows: {profile['duplicate_rows']}")
    print(f"Memory Usage: {profile['memory_usage']:.2f} MB")
    
    print(f"\n--- Missing Values ---")
    for col, count in profile['missing_values'].items():
        if count > 0:
            pct = profile['missing_percentage'][col]
            print(f"  {col}: {count} ({pct:.1f}%)")
    
    if profile.get('negative_values'):
        print(f"\n--- Negative Values (Invalid) ---")
        for col, count in profile['negative_values'].items():
            print(f"  {col}: {count} rows")
    
    if profile.get('zero_values'):
        print(f"\n--- Zero Values (Suspicious) ---")
        for col, count in profile['zero_values'].items():
            print(f"  {col}: {count} rows")
    
    if profile.get('empty_strings'):
        print(f"\n--- Empty Strings ---")
        for col, count in profile['empty_strings'].items():
            print(f"  {col}: {count} rows")

# Main execution
if __name__ == "__main__":
    print("Starting Data Quality Assessment...")
    
    # Connect to databases
    mysql_conn, pg_conn = connect_to_databases()
    
    # Load all tables
    customers_df = pd.read_sql("SELECT * FROM customers", mysql_conn)
    products_df = pd.read_sql("SELECT * FROM products", mysql_conn)
    orders_df = pd.read_sql("SELECT * FROM customer_orders", mysql_conn)
    employees_df = pd.read_sql("SELECT * FROM employees", pg_conn)
    departments_df = pd.read_sql("SELECT * FROM departments", pg_conn)
    
    # Profile each table
    profiles = [
        profile_dataframe(customers_df, "customers"),
        profile_dataframe(products_df, "products"),
        profile_dataframe(orders_df, "customer_orders"),
        profile_dataframe(employees_df, "employees"),
        profile_dataframe(departments_df, "departments")
    ]
    
    # Print detailed reports
    for profile in profiles:
        print_quality_report(profile)
    
    # Detect duplicates
    print(f"\n\n{'='*60}")
    print("DUPLICATE RECORDS ANALYSIS")
    print(f"{ '='*60}")
    detect_duplicates_details(customers_df, "customers")
    detect_duplicates_details(products_df, "products")
    detect_duplicates_details(orders_df, "customer_orders")
    detect_duplicates_details(employees_df, "employees")
    detect_duplicates_details(departments_df, "departments")
    
    # Create visualizations
    visualize_quality_issues(profiles)
    
    # Close connections
    mysql_conn.close()
    pg_conn.close()
    
    print("\n✓ Data Quality Assessment Complete!")
