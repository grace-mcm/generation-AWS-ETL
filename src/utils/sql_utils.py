# This file exists to separate the direct use of psycopg2 in 'connect_to_db.py'
# from functions here that only care about the Connection and Cursor - this makes these easier to unit test.

import uuid
import logging

LOGGER = logging.getLogger()

LOGGER.setLevel(logging.INFO)

# creating tables
def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    try:
        LOGGER.info('create_db_tables: creating stores data table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS stores (
                store_id VARCHAR(500) PRIMARY KEY,
                store_name VARCHAR(255) NOT NULL
            );
            '''
        )

        LOGGER.info('create_db_tables: creating orders data table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS orders (
                order_id VARCHAR(500) PRIMARY KEY,
                date_time TIMESTAMP,
                store_name VARCHAR(255) NOT NULL,
                order_cost DECIMAL(10,2) NOT NULL,
                payment_type VARCHAR(50) NOT NULL
            );
            '''
        )

        LOGGER.info('create_db_tables: creating products data table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS products (
                product_id VARCHAR(500),
                product_name VARCHAR(MAX),
                product_price DECIMAL(10,2)
            );
            '''
        )

        LOGGER.info('create_db_tables: creating orderline data table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS order_line (
                orderline_id VARCHAR(500) PRIMARY KEY,
                order_id VARCHAR(500),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                product_name VARCHAR(500)
            );
            '''
        )

        LOGGER.info('create_db_tables: committing')
        connection.commit()

        LOGGER.info('create_db_tables: done')
    except Exception as ex:
        LOGGER.info(f'create_db_tables: failed to run sql: {ex}')
        raise ex


def save_data_in_stores(connection, cursor, bucket_name, file_path, stores_list):
    LOGGER.info(f'save_data_in_stoers: started: file_path={file_path}, rows={len(stores_list)}')
    
    try:
        for record in stores_list:
            record_key = 'store_name'
            record_value = record[record_key]

            cursor.execute(f"SELECT 1 FROM stores WHERE {record_key} = %s", (record_value,))
            if cursor.fetchone():
                LOGGER.info(f'save_data_in_stores: skipping existing record with {record_key}={record_value}')
                continue

            columns = ', '.join(record.keys())
            values = tuple(record.values())
            values_placeholder = ', '.join(['%s'] * len(record))

            sql_insert_template = f'INSERT INTO stores ({columns}) VALUES ({values_placeholder})'

            LOGGER.info(
                f'save_data_in_stores: inserting new record: {record_key}={record_value}, sql={sql_insert_template}'
            )
    
            cursor.execute(sql_insert_template, values)

        connection.commit()
        LOGGER.info(f'save_data_in_stores: done: file_path={file_path}, rows={len(stores_list)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_stores: error: ex={ex}, file_path={file_path}')
        raise ex

def save_data_in_products(connection, cursor, bucket_name, file_path, products_list):
    LOGGER.info(f'save_data_in_products: started: file_path={file_path}, rows={len(products_list)}')

    try:
        for record in products_list:
            record_key = 'product_name'
            record_value = record[record_key]

            cursor.execute(f"SELECT 1 FROM products WHERE {record_key} = %s", (record_value,))
            if cursor.fetchone():
                LOGGER.info(f'save_data_in_products: skipping existing record with {record_key}={record_value}')
                continue

            columns = ', '.join(record.keys())
            values = tuple(record.values())
            values_placeholder = ', '.join(['%s'] * len(record))

            sql_insert_template = f'INSERT INTO products ({columns}) VALUES ({values_placeholder})'

            LOGGER.info(
                f'save_data_in_products: inserting new record: {record_key}={record_value}, sql={sql_insert_template}'
            )
    
            cursor.execute(sql_insert_template, values)

        connection.commit()
        LOGGER.info(f'save_data_in_products: done: file_path={file_path}, rows={len(products_list)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_products: error: ex={ex}, file_path={file_path}')
        raise ex
    
def save_data_in_orders(connection, cursor, bucket_name, file_path, orders_list):
    LOGGER.info(f'save_data_in_orders: started: file_path={file_path}, rows={len(orders_list)}')

    try:
        for record in orders_list:
            columns = ', '.join(record.keys())
            values = tuple(record.values())
            values_placeholder = ', '.join(['%s'] * len(record))

            sql_insert_template = f'INSERT INTO orders ({columns}) VALUES ({values_placeholder})'

            LOGGER.info(
                f'save_data_in_orders: columns={columns}, sql_insert_template={sql_insert_template}, values_placeholder={values_placeholder}'
            )

            cursor.execute(sql_insert_template, values)

        connection.commit()
        LOGGER.info(f'save_data_in_orders: done: file_path={file_path}, rows={len(orders_list)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_orders: error: ex={ex}, file_path={file_path}')
        raise ex
    
def save_data_in_order_line(connection, cursor, bucket_name, file_path, orderline_list):
    LOGGER.info(f'save_data_in_order_line: started: file_path={file_path}, rows={len(orderline_list)}')

    try:
        for record in orderline_list:
            columns = ', '.join(record.keys())
            values = tuple(record.values())
            values_placeholder = ', '.join(['%s'] * len(record))

            sql_insert_template = f'INSERT INTO order_line ({columns}) VALUES ({values_placeholder})'

            LOGGER.info(
                f'save_data_in_order_line: columns={columns}, sql_insert_template={sql_insert_template}, values_placeholder={values_placeholder}'
            )

            cursor.execute(sql_insert_template, values)

        connection.commit()
        LOGGER.info(f'save_data_in_order_line: done: file_path={file_path}, rows={len(orderline_list)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_order_line: error: ex={ex}, file_path={file_path}')
        raise ex