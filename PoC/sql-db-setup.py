import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

#def create_connection():
#    try:
#        #print("Opening connection...") #with to autoclose database
#        with psycopg.connect(f""" 
#            host = {host_name}
#            When you run:
#            dbname = {database_name}
#            user={user_name}
#            password={user_password}            
#""") as connection: 
#         return connection #passing this connection into every argument means that it's all the same database being edited throughout
#    except psycopg.DatabaseError as e:
#        print(f"Connection failed : {e}")

#Creating connection to test database
connection = psycopg2.connect(f"""
    host={host_name}
    dbname={database_name}
    user={user_name}
    password={user_password}
    """)

cursor = connection.cursor()

def create_products(connection): #creates a table for products
    cursor = connection.cursor()
    cursor.execute("""
            create table if not exists products (
            product_id serial primary key,
            product_name varchar UNIQUE not null,
            product_price float not null
                );""")
    
    connection.commit() #commits the sql to the database, so we use connection, cursor only executes the sql, but you need connection to push it to the database
    cursor.close()


# def create_transactions(connection): #creates a table for transactions
#     cursor = connection.cursor()
#     cursor.execute("""
#         create table if not exists transactions (
#           id serial primary key,
#           order_id integer not null,
#           foreign key(order_id) references order_status(order_id),
#           product_id integer not null,
#           foreign key(product_id) references products(id)
#                    );""")
#     connection.commit() #commits the sql to the database, so we use connection, cursor only executes the sql, but you need connection to push it to the database
#     cursor.close()

def create_order_line(connection): #creates a table for store locations
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_line(
                orderline_id serial PRIMARY KEY,
                order_id INT REFERENCES orders(order_id),
                product_name VARCHAR)
            """)
    connection.commit() #commits the sql to the database, so we use connection, cursor only executes the sql, but you need connection to push it to the database
    cursor.close()

# def create_payment_method(connection): #creates a table for payment method
#     cursor = connection.cursor()
#     cursor.execute("""
#         create table if not exists payment_method (
#             payment_id serial primary key
#                    );""")
#     connection.commit() #commits the sql to the database, so we use connection, cursor only executes the sql, but you need connection to push it to the database
#     cursor.close()

def create_raw_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        create table if not exists raw(
            order_id serial primary key, 
            date_time timestamp,
            store_name varchar, 
            customer_name varchar,
            order_detail varchar,
            order_cost float,
            payment_type varchar, 
            card_number varchar(16)         
                   )  
""")
    connection.commit()
    cursor.close()

def create_orders(connection): #creates a table to merge information from other tables to master orders table
    cursor = connection.cursor()
    cursor.execute("""
        create table if not exists orders (
            order_id serial primary key,
            date_time timestamp,
            store_name varchar not null, 
            payment_type varchar not null,
            order_cost float not null
                 );""")

    connection.commit()
    cursor.close()

def create_stores(connection): #creates a table to merge information from other tables to master orders table
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS stores (
                store_id serial PRIMARY KEY,
                store_name VARCHAR(255) UNIQUE NOT NULL
            );
            ''')

    connection.commit()
    cursor.close()
    
def main(connection): #will execute above code to create tables if they do not already exist
    create_orders(connection)
    create_products(connection)
    create_order_line(connection)
    create_raw_table(connection)
    create_stores(connection)
    
main(connection)

