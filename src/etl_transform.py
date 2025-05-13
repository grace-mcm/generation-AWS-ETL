import csv
import uuid
from datetime import datetime
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

CAFE_SALES_FIELDS = [
    'date_time',
    'store_name',
    'customer_name',
    'order_details',
    'order_cost',
    'payment_type',
    'card_number',
]


def create_guid():
    #Generate a UUID string
    return str(uuid.uuid4())


def extract(test_data):
    LOGGER.info('extract: starting')
    reader = csv.DictReader(
        test_data,
        fieldnames=CAFE_SALES_FIELDS,
        delimiter=',',
    )

    data = [row for row in reader]
    LOGGER.info(f'extract: done: rows={len(data)}')
    return data


def remove_fields(data, fields):
    #Remove sensitive information from each record
    LOGGER.info(f'remove_fields: removing {fields} from {len(data)} rows')
    return [{k: v for k, v in row.items() if k not in fields} for row in data]


def reformat_dates(data, input_fmt='%d/%m/%Y %H:%M', output_fmt='%Y-%m-%d %H:%M'):
    #Reformat date_time field in each record
    LOGGER.info('reformat_dates: starting')
    result = []
    for row in data:
        try:
            dt = datetime.strptime(row['date_time'], input_fmt)
            row['date_time'] = dt.strftime(output_fmt)
            result.append(row)
        except (ValueError, KeyError) as e:
            LOGGER.warning(f"Skipping invalid date: {row.get('date_time')} (error: {e})")
    LOGGER.info(f'reformat_dates: done: rows={len(result)}')
    return result


def add_order_ids(data):
    #Add unique order_id to each order record
    for row in data:
        row['order_id'] = create_guid()
    return data

def extract_stores(data):
    store_lookup = {}
    stores = []
    
    for row in data:
        store_name = row.get('store_name')
        if store_name and store_name not in store_lookup:
            store_id = create_guid()
            store_lookup[store_name] = store_id
            stores.append({
                'store_id': store_id,
                'store_name': store_name
            })
    
    return stores, store_lookup

def extract_orders(data, store_lookup):
    order_fields = ['order_id', 'date_time', 'order_cost', 'payment_type']
    return [{
        **{k: row[k] for k in order_fields if k in row},
        'store_name': row['store_name']
    } for row in data if 'store_name' in row]


def extract_products(data):
    # Create a unique list of product names and prices
    seen = set()
    products = []

    for row in data:
        for item in row.get('order_details', '').split(','):
            parts = item.strip().rsplit(' - ', 1)
            if len(parts) == 2:
                name, price = parts
                key = (name.strip(), price.strip())
                if key not in seen:
                    try:
                        products.append({
                            'product_id': create_guid(),
                            'product_name': name.strip(),
                            'product_price': float(price.strip())
                        })
                        seen.add(key)
                    except ValueError:
                        LOGGER.warning(f"Invalid price for item: {item}")
    
    LOGGER.info(f'extract_products: done: total={len(products)}')
    return products


def extract_orderlines(data, products):
    orderlines = []
    orderline_id = 1

    for row in data:
        order_id = row.get('order_id')
        for item in row.get('order_details', '').split(','):
            parts = item.strip().rsplit(' - ', 1)
            if len(parts) == 2:
                product_name, _ = parts
                product_name = product_name.strip()

                orderlines.append({
                    'orderline_id': orderline_id,
                    'order_id': order_id,
                    'product_name': product_name
                })
                orderline_id += 1

    return orderlines


def transform_pipeline(data):
    #Main ETL pipeline
    LOGGER.info('Pipeline: starting')
    data = remove_fields(data, ['customer_name', 'card_number'])
    data = reformat_dates(data)
    data = add_order_ids(data)

    stores, store_lookup = extract_stores(data)
    orders = extract_orders(data, store_lookup)
    products = extract_products(data)
    orderlines = extract_orderlines(data, products)


    LOGGER.info('Pipeline: complete')
    return {
        'stores': stores,
        'orders': orders,
        'orderlines': orderlines,
        'products': products
    }