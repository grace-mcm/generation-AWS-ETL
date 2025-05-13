from utils import s3_utils, db_utils, sql_utils
import json

import etl_transform as etl
import logging
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'

def lambda_handler(event, context):
    LOGGER.info("lambda_handler: starting")
    # file_path = 'NOT_SET'  # makes the exception handler compile

    try:
        file_path = "NOT_SET"  # just here to make the exception handler compile

        ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')
        
        LOGGER.info(f'lambda_handler: ssm_param_name={ssm_param_name} from ssm_env_var_name={SSM_ENV_VAR_NAME}')
        bucket_name, file_path = s3_utils.get_file_info(event)

        # LOGGER.info(
        #     f"lambda_handler: event: file={file_path}, bucket_name={bucket_name}"
        # )

        # LOGGER.info(
        #     f"lambda_handler: s3.load_file: loading file_name={file_path} from bucket_name={bucket_name}"
        # )

        csv = s3_utils.load_file(bucket_name, file_path)
        LOGGER.info(f"lambda_handler: s3.load_file result={csv}")

        data = etl.extract(csv)
        LOGGER.info(f"lambda_handler: extract_csv_data result={data}")

        transformed_data = etl.transform_pipeline(data) #removes sensitive info and changes date format
        stores_list = transformed_data['stores']
        products_list = transformed_data['products']
        orders_list = transformed_data['orders']
        orderline_list = transformed_data['orderlines']
        LOGGER.info(f"lambda_handler: extract_csv_data result={data}")

        redshift_details = db_utils.get_ssm_param(ssm_param_name)
        conn, cur = db_utils.open_sql_database_connection_and_cursor(redshift_details)
        sql_utils.create_db_tables(conn, cur)
        #sql_utils.save_data_in_db(conn, cur, bucket_name, file_path, transformed_data)
        sql_utils.save_data_in_stores(conn, cur, bucket_name, file_path, stores_list)
        sql_utils.save_data_in_products(conn, cur, bucket_name, file_path, products_list)
        sql_utils.save_data_in_orders(conn, cur, bucket_name, file_path, orders_list)
        sql_utils.save_data_in_order_line(conn, cur, bucket_name, file_path, orderline_list)
        cur.close()
        conn.close()
        
        
        LOGGER.info(f"lambda_handler: transformed_data={transformed_data}")

    except Exception as err:
        LOGGER.error(f"lambda_handler: failure: error={err}, file={file_path}")
        raise err
