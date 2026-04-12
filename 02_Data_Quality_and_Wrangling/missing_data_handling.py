import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import psycopg2

sns.set_style("whitegrid")

def load_dirty_data():
    mysql_conn = mysql.connector.connect(
        host="localhost", user="datauser",
        password="datapass123", database="sales_data_raw"
    )
    pg_conn = psycopg2.connect(
        host="localhost", user="datauser",
        password="rootpass123", database="employee_data_raw"
    )
    customers = pd.read_sql("SELECT * FROM customers", mysql_conn)
    products  = pd.read_sql("SELECT * FROM products", mysql_conn)
    employees = pd.read_sql("SELECT * FROM employees", pg_conn)
    mysql_conn.close()
    pg_conn.close()
    return customers, products, employees

def handle_missing_customers(df):
    df_clean = df.copy()
    df_clean['email']            = df_clean['email'].fillna('unknown@placeholder.com')
    df_clean['phone']            = df_clean['phone'].fillna('Unknown')
    median_age                   = df_clean['age'][(df_clean['age'] > 0) & (df_clean['age'] < 120)].median()
    df_clean['age']              = df_clean['age'].fillna(median_age)
    df_clean['account_balance']  = df_clean['account_balance'].fillna(0.0)
    df_clean['registration_date']= df_clean['registration_date'].fillna('2024-01-01')
    df_clean['name']             = df_clean['name'].fillna('Unknown Customer')
    return df_clean

def handle_missing_products(df):
    df_clean = df.copy()
    df_clean['category']     = df_clean['category'].fillna('Uncategorized')
    df_clean['stock']        = df_clean['stock'].fillna(0)
    df_clean['supplier']     = df_clean['supplier'].replace('', 'Unknown Supplier').fillna('Unknown Supplier')
    df_clean['last_updated'] = df_clean['last_updated'].fillna('2024-01-01')
    df_clean['product_name'] = df_clean['product_name'].fillna('Unknown Product')
    return df_clean

def handle_missing_employees(df):
    df_clean = df.copy()
    df_clean['first_name'] = df_clean['first_name'].fillna('Unknown')
    df_clean['last_name']  = df_clean['last_name'].fillna('Unknown')

    def generate_email(row):
        if pd.isna(row['email']):
            return f"{str(row['first_name']).lower()}.{str(row['last_name']).lower()}@company.com"
        return row['email']
    df_clean['email'] = df_clean.apply(generate_email, axis=1)

    df_clean['department'] = df_clean['department'].replace('', 'Unassigned').fillna('Unassigned')

    for dept in df_clean['department'].unique():
        mask = (df_clean['department'] == dept) & (df_clean['salary'].isna())
        dept_median = df_clean[df_clean['department'] == dept]['salary'].median()
        df_clean.loc[mask, 'salary'] = dept_median
    df_clean['salary'] = df_clean['salary'].fillna(df_clean['salary'].median())

    df_clean['hire_date'] = df_clean['hire_date'].fillna('2023-01-01')

    for dept in df_clean['department'].unique():
        mask = (df_clean['department'] == dept) & (df_clean['performance_score'].isna())
        dept_avg = df_clean[df_clean['department'] == dept]['performance_score'].mean()
        df_clean.loc[mask, 'performance_score'] = dept_avg
    df_clean['performance_score'] = df_clean['performance_score'].fillna(df_clean['performance_score'].mean())

    return df_clean

def visualize_missing_data_impact(df_before, df_after, title):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Missing Data Handling: {title}', fontsize=16, fontweight='bold')

    ax1 = axes[0]
    missing_before = df_before.isnull().sum()
    missing_before = missing_before[missing_before > 0].sort_values(ascending=False)
    if len(missing_before) > 0:
        bars = ax1.barh(range(len(missing_before)), missing_before.values, color='#E53E3E', alpha=0.7)
        ax1.set_yticks(range(len(missing_before)))
        ax1.set_yticklabels(missing_before.index)
        ax1.set_xlabel('Missing Values Count', fontweight='bold')
        ax1.set_title('BEFORE: Missing Data', fontweight='bold', color='#E53E3E')
        for bar, val in zip(bars, missing_before.values):
            ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{int(val)}', va='center', fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'No Missing Data', ha='center', va='center', transform=ax1.transAxes, fontsize=14)

    ax2 = axes[1]
    missing_after  = df_after.isnull().sum()
    total_fields   = len(df_after.columns)
    complete_fields = (missing_after == 0).sum()
    sizes  = [complete_fields, total_fields - complete_fields]
    colors = ['#48BB78', '#FC8181']
    labels = [f'Complete ({complete_fields})', f'Still Missing ({total_fields - complete_fields})']
    ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
            textprops={'fontweight': 'bold'})
    ax2.set_title('AFTER: Data Completeness', fontweight='bold', color='#48BB78')

    plt.tight_layout()
    filename = f'missing_data_{title.lower().replace(" ", "_")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {filename}")
    plt.show()

def print_missing_summary(df_before, df_after, name):
    print(f"\n{'='*60}")
    print(f"MISSING DATA SUMMARY: {name}")
    print(f"{'='*60}")
    missing_before = df_before.isnull().sum().sum()
    missing_after  = df_after.isnull().sum().sum()
    print(f"Missing values ANTES:  {missing_before}")
    print(f"Missing values DESPUÉS: {missing_after}")
    print(f"Valores rellenados:     {missing_before - missing_after}")
    total = len(df_after) * len(df_after.columns)
    print(f"Tasa de completitud:    {(1 - missing_after / total) * 100:.2f}%")

if __name__ == "__main__":
    print("Iniciando Missing Data Handling...")
    customers, products, employees = load_dirty_data()

    customers_clean = handle_missing_customers(customers)
    products_clean  = handle_missing_products(products)
    employees_clean = handle_missing_employees(employees)

    print_missing_summary(customers, customers_clean, "Customers")
    print_missing_summary(products,  products_clean,  "Products")
    print_missing_summary(employees, employees_clean, "Employees")

    visualize_missing_data_impact(customers, customers_clean, "Customers")
    visualize_missing_data_impact(products,  products_clean,  "Products")
    visualize_missing_data_impact(employees, employees_clean, "Employees")

    print("\n✓ Ejercicio 2 completo!")
