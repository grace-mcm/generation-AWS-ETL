import csv
import psycopg2 as psycopg
from dotenv import load_dotenv 
import os
from datetime import datetime

load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

connection = psycopg.connect(f"""
    host={host_name}
    dbname={database_name}
    user={user_name}
    password={user_password}
    """)

cursor = connection.cursor()

csv_files = [
    'london_brixton_13-04-2025_08-00-00.csv',
    'london_brixton_14-04-2025_08-00-00.csv',
    'london_brixton_15-04-2025_08-00-00.csv',
    'london_brixton_16-04-2025_08-00-00.csv',
    'london_brixton_17-04-2025_08-00-00.csv',
    'london_brixton_18-04-2025_08-00-00.csv',
    'london_brixton_19-04-2025_08-00-00.csv',
    'london_camden_13-04-2025_09-00-00.csv',
    'london_camden_14-04-2025_09-00-00.csv',
    'london_camden_15-04-2025_09-00-00.csv',
    'london_camden_16-04-2025_09-00-00.csv',
    'london_camden_17-04-2025_09-00-00.csv',
    'london_camden_18-04-2025_09-00-00.csv',
    'london_camden_19-04-2025_09-00-00.csv',
    'london_greenwich_13-04-2025_08-00-00.csv',
    'london_greenwich_14-04-2025_08-00-00.csv',
    'london_greenwich_15-04-2025_08-00-00.csv',
    'london_greenwich_16-04-2025_08-00-00.csv',
    'london_greenwich_17-04-2025_08-00-00.csv',
    'london_greenwich_18-04-2025_08-00-00.csv',
    'london_greenwich_19-04-2025_08-00-00.csv'
]

for file_name in csv_files:
    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for record in reader:
            try:
                date_obj = datetime.strptime(record[0], "%d/%m/%Y %H:%M")
                record[0] = date_obj
                cursor.execute("""
                    INSERT INTO raw 
                    (date_time, store_name, customer_name, order_detail, order_cost, payment_type, card_number) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, record)
                connection.commit()
            except Exception as e:
                print(f"Error processing record in {file_name}: {e}")

#with open('london_brixton_14-04-2025_08-00-00.csv','r') as file:
#    reader = csv.reader(file)
#    for record in reader:
#       date_obj = datetime.strptime(record[0], "%d/%m/%Y %H:%M")
#       record[0] = date_obj
#       cursor.execute("""insert into raw (date_time, store_name, customer_name, order_detail, order_cost, payment_type, card_number) 
#                      values(%s, %s, %s, %s, %s, %s, %s) 
#                      """, record)
#       
#       connection.commit()

def extract_orders():
    cursor = connection.cursor()
    extract_order = """
        insert into orders (date_time, store_name, payment_type, order_cost)
        select date_time, store_name, payment_type, order_cost from raw 
    """
    cursor.execute(extract_order)
    connection.commit()
extract_orders()

def extract_stores():
    cursor = connection.cursor()
    extract_store = """
        INSERT INTO stores (store_name)
        SELECT store_name FROM raw
        ON CONFLICT (store_name) DO NOTHING
    """
    cursor.execute(extract_store)
    connection.commit()
extract_stores()

def extract_products():
    extract_product = """
        INSERT INTO products (product_name, product_price)
        SELECT 
            TRIM(SPLIT_PART(value, '-', 1) || 
                 CASE 
                    WHEN n > 2 THEN ' - ' || SPLIT_PART(value, '-', 2)
                    ELSE ''
                 END) AS product_name,
            CAST(TRIM(SPLIT_PART(value, '-', n)) AS NUMERIC) AS product_price
        FROM (
            SELECT 
                value,
                regexp_count(value, '-') + 1 AS n
            FROM raw,
            LATERAL regexp_split_to_table(raw.order_detail, ',') AS value
        ) sub
        ON CONFLICT (product_name) DO NOTHING;
    """
    cursor.execute(extract_product)
    connection.commit()


extract_products()

def extract_orderlines():
    extract_orderline = """
        INSERT INTO order_line (order_id, product_name)
        SELECT
            raw.order_id,
            TRIM(regexp_replace(raw_product, '\\s*-\\s*[^-]+$', '')) AS product_name
        FROM raw
        CROSS JOIN LATERAL regexp_split_to_table(raw.order_detail, ',') AS raw_product
        JOIN products
        ON TRIM(regexp_replace(raw_product, '\\s*-\\s*[^-]+$', '')) = products.product_name;
    """
    try:
        cursor.execute(extract_orderline)
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
extract_orderlines()
