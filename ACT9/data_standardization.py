import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import mysql.connector
import psycopg2
from datetime import datetime

sns.set_style("whitegrid")

def connect_to_databases():
    mysql_conn = mysql.connector.connect(
        host="localhost", user="datauser",
        password="datapass123", database="sales_data_raw"
    )
    pg_conn = psycopg2.connect(
        host="localhost", user="datauser",
        password="rootpass123", database="employee_data_raw"
    )
    return mysql_conn, pg_conn

def standardize_dates(date_str):
    if pd.isna(date_str):
        return date_str
    date_str = str(date_str).strip()
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return date_str

def standardize_text(text):
    if pd.isna(text):
        return text
    return re.sub(r'\s+', ' ', str(text).strip().lower())

def standardize_phone(phone):
    if pd.isna(phone):
        return phone
    digits = re.sub(r'[^\d+]', '', str(phone))
    if not digits.startswith('+'):
        digits = '+1' + digits
    return digits

def standardize_customers(df):
    df_clean = df.copy()
    df_clean['registration_date'] = df_clean['registration_date'].apply(standardize_dates)
    df_clean['name']    = df_clean['name'].apply(standardize_text)
    df_clean['email']   = df_clean['email'].str.lower().str.strip()
    df_clean['country'] = df_clean['country'].apply(standardize_text)
    df_clean['phone']   = df_clean['phone'].apply(standardize_phone)
    median_age = df_clean['age'][(df_clean['age'] > 0) & (df_clean['age'] < 120)].median()
    df_clean.loc[(df_clean['age'] < 0) | (df_clean['age'] > 120), 'age'] = median_age
    df_clean.loc[df_clean['account_balance'] < 0, 'account_balance'] = 0.0
    return df_clean

def standardize_products(df):
    df_clean = df.copy()
    df_clean['last_updated']  = df_clean['last_updated'].apply(standardize_dates)
    df_clean['product_name']  = df_clean['product_name'].apply(standardize_text)
    df_clean['category']      = df_clean['category'].apply(standardize_text)
    df_clean['supplier']      = df_clean['supplier'].str.strip()
    median_price = df_clean['price'][df_clean['price'] > 0].median()
    df_clean.loc[df_clean['price'] < 0, 'price'] = median_price
    df_clean.loc[df_clean['stock'] < 0, 'stock'] = 0
    return df_clean

def standardize_employees(df):
    df_clean = df.copy()
    df_clean['hire_date']   = df_clean['hire_date'].apply(standardize_dates)
    df_clean['first_name']  = df_clean['first_name'].apply(standardize_text)
    df_clean['last_name']   = df_clean['last_name'].apply(standardize_text)
    df_clean['email']       = df_clean['email'].str.lower().str.strip()
    df_clean['department']  = df_clean['department'].apply(standardize_text)
    median_salary = df_clean['salary'][df_clean['salary'] > 0].median()
    df_clean.loc[df_clean['salary'] < 0, 'salary'] = median_salary
    median_score = df_clean['performance_score'][(df_clean['performance_score'] >= 0) & (df_clean['performance_score'] <= 5)].median()
    df_clean.loc[(df_clean['performance_score'] < 0) | (df_clean['performance_score'] > 5), 'performance_score'] = median_score
    return df_clean

def remove_duplicates(df, name):
    before = len(df)
    df_clean = df.drop_duplicates(keep='first')
    after = len(df_clean)
    print(f"  {name}: {before - after} duplicados eliminados ({before} → {after} filas)")
    return df_clean

def visualize_standardization(df_before, df_after, title, field):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Standardization: {title} - campo: {field}', fontsize=14, fontweight='bold')

    before_counts = df_before[field].value_counts().head(8)
    axes[0].barh(range(len(before_counts)), before_counts.values, color='#E53E3E', alpha=0.7)
    axes[0].set_yticks(range(len(before_counts)))
    axes[0].set_yticklabels([str(x)[:25] for x in before_counts.index], fontsize=9)
    axes[0].set_title(f'ANTES: {df_before[field].nunique()} valores únicos', fontweight='bold', color='#E53E3E')
    axes[0].set_xlabel('Count')

    after_counts = df_after[field].value_counts().head(8)
    axes[1].barh(range(len(after_counts)), after_counts.values, color='#48BB78', alpha=0.7)
    axes[1].set_yticks(range(len(after_counts)))
    axes[1].set_yticklabels([str(x)[:25] for x in after_counts.index], fontsize=9)
    axes[1].set_title(f'DESPUÉS: {df_after[field].nunique()} valores únicos', fontweight='bold', color='#48BB78')
    axes[1].set_xlabel('Count')

    plt.tight_layout()
    fname = f'std_{title.lower()}_{field}.png'
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print(f"  ✓ Guardado: {fname}")
    plt.show()

def visualize_deduplication(tables):
    fig, ax = plt.subplots(figsize=(10, 6))
    names   = [t[0] for t in tables]
    before  = [t[1] for t in tables]
    after   = [t[2] for t in tables]
    x = np.arange(len(names))
    w = 0.35
    ax.bar(x - w/2, before, w, label='Antes', color='#E53E3E', alpha=0.7)
    ax.bar(x + w/2, after,  w, label='Después', color='#48BB78', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel('Número de filas')
    ax.set_title('Deduplicación: Antes vs Después', fontweight='bold')
    ax.legend()
    for i, (b, a) in enumerate(zip(before, after)):
        ax.text(i - w/2, b + 0.1, str(b), ha='center', fontweight='bold')
        ax.text(i + w/2, a + 0.1, str(a), ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('deduplication_results.png', dpi=300, bbox_inches='tight')
    print("  ✓ Guardado: deduplication_results.png")
    plt.show()

if __name__ == "__main__":
    print("Iniciando Data Standardization & Deduplication...\n")
    mysql_conn, pg_conn = connect_to_databases()

    customers  = pd.read_sql("SELECT * FROM customers", mysql_conn)
    products   = pd.read_sql("SELECT * FROM products", mysql_conn)
    employees  = pd.read_sql("SELECT * FROM employees", pg_conn)

    # Estandarizar
    customers_std  = standardize_customers(customers)
    products_std   = standardize_products(products)
    employees_std  = standardize_employees(employees)

    # Visualizar estandarización
    print("Generando visualizaciones de estandarización...")
    visualize_standardization(customers, customers_std,  "customers", "country")
    visualize_standardization(products,  products_std,   "products",  "category")
    visualize_standardization(employees, employees_std,  "employees", "department")

    # Deduplicar
    print("\nEliminando duplicados...")
    tables_dedup = []
    for df, name in [(customers_std, "customers"), (products_std, "products"), (employees_std, "employees")]:
        b = len(df)
        df_dd = remove_duplicates(df, name)
        tables_dedup.append((name, b, len(df_dd)))

    visualize_deduplication(tables_dedup)

    mysql_conn.close()
    pg_conn.close()
    print("\n✓ Ejercicio 3 completo!")
