import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import psycopg2

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

def detect_outliers_iqr(df, column):
    """Detecta outliers usando el método IQR"""
    data = df[column].dropna()
    Q1  = data.quantile(0.25)
    Q3  = data.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower) | (df[column] > upper)][column]
    return outliers, lower, upper

def detect_outliers_zscore(df, column, threshold=2.5):
    """Detecta outliers usando Z-score"""
    data = df[column].dropna()
    mean = data.mean()
    std  = data.std()
    z_scores = np.abs((df[column] - mean) / std)
    outliers = df[z_scores > threshold][column]
    return outliers

def cap_outliers(df, column, lower, upper):
    """Trata outliers por capping (winsorizing)"""
    df_clean = df.copy()
    df_clean[column] = df_clean[column].clip(lower=lower, upper=upper)
    return df_clean

def print_outlier_report(df, column, table_name):
    outliers_iqr, lower, upper = detect_outliers_iqr(df, column)
    outliers_z   = detect_outliers_zscore(df, column)
    print(f"\n  [{table_name}] columna '{column}':")
    print(f"    Rango IQR válido:  [{lower:.2f}, {upper:.2f}]")
    print(f"    Outliers IQR:      {len(outliers_iqr)} filas → valores: {outliers_iqr.values.tolist()}")
    print(f"    Outliers Z-score:  {len(outliers_z)} filas")
    return lower, upper

def visualize_outliers(df_before, df_after, column, title):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Outlier Detection & Treatment: {title} - {column}', fontsize=14, fontweight='bold')

    # Boxplot antes
    axes[0, 0].boxplot(df_before[column].dropna(), vert=True, patch_artist=True,
                       boxprops=dict(facecolor='#FC8181', alpha=0.7))
    axes[0, 0].set_title('ANTES: Boxplot', fontweight='bold', color='#E53E3E')
    axes[0, 0].set_ylabel(column)

    # Boxplot después
    axes[0, 1].boxplot(df_after[column].dropna(), vert=True, patch_artist=True,
                       boxprops=dict(facecolor='#68D391', alpha=0.7))
    axes[0, 1].set_title('DESPUÉS: Boxplot', fontweight='bold', color='#38A169')
    axes[0, 1].set_ylabel(column)

    # Histograma antes
    axes[1, 0].hist(df_before[column].dropna(), bins=10, color='#FC8181', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('ANTES: Distribución', fontweight='bold', color='#E53E3E')
    axes[1, 0].set_xlabel(column)
    axes[1, 0].set_ylabel('Frecuencia')

    # Histograma después
    axes[1, 1].hist(df_after[column].dropna(), bins=10, color='#68D391', alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('DESPUÉS: Distribución', fontweight='bold', color='#38A169')
    axes[1, 1].set_xlabel(column)
    axes[1, 1].set_ylabel('Frecuencia')

    plt.tight_layout()
    fname = f'outliers_{title.lower()}_{column}.png'
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print(f"  ✓ Guardado: {fname}")
    plt.show()

if __name__ == "__main__":
    print("Iniciando Outlier Detection...\n")
    mysql_conn, pg_conn = connect_to_databases()

    products  = pd.read_sql("SELECT * FROM products",  mysql_conn)
    customers = pd.read_sql("SELECT * FROM customers", mysql_conn)
    employees = pd.read_sql("SELECT * FROM employees", pg_conn)

    print("="*55)
    print("REPORTE DE OUTLIERS")
    print("="*55)

    # --- Products: price ---
    lower_p, upper_p = print_outlier_report(products, 'price', 'products')[0:2]
    products_clean   = cap_outliers(products, 'price', lower_p, upper_p)
    visualize_outliers(products, products_clean, 'price', 'products')

    # --- Customers: age ---
    lower_a, upper_a = print_outlier_report(customers, 'age', 'customers')[0:2]
    # Para age: reemplazar outliers con mediana en vez de capping
    customers_clean  = customers.copy()
    valid_ages       = customers['age'][(customers['age'] > 0) & (customers['age'] < 120)]
    median_age       = valid_ages.median()
    customers_clean.loc[(customers_clean['age'] < lower_a) | (customers_clean['age'] > upper_a), 'age'] = median_age
    visualize_outliers(customers, customers_clean, 'age', 'customers')

    # --- Employees: salary ---
    lower_s, upper_s = print_outlier_report(employees, 'salary', 'employees')[0:2]
    employees_clean  = cap_outliers(employees, 'salary', lower_s, upper_s)
    visualize_outliers(employees, employees_clean, 'salary', 'employees')

    # Resumen final
    print("\n" + "="*55)
    print("RESUMEN FINAL")
    print("="*55)
    for df_b, df_a, col, name in [
        (products,  products_clean,  'price',  'products'),
        (customers, customers_clean, 'age',    'customers'),
        (employees, employees_clean, 'salary', 'employees'),
    ]:
        antes  = df_b[col].describe()
        despues = df_a[col].describe()
        print(f"\n  {name}.{col}:")
        print(f"    Media:   {antes['mean']:.2f}  →  {despues['mean']:.2f}")
        print(f"    Máximo:  {antes['max']:.2f}  →  {despues['max']:.2f}")
        print(f"    Mínimo:  {antes['min']:.2f}  →  {despues['min']:.2f}")

    mysql_conn.close()
    pg_conn.close()
    print("\n✓ Ejercicio 4 completo!")
    print("✓ Actividad 9 finalizada!")
