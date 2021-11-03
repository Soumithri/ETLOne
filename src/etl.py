import json
import logging

import awswrangler as wr
from datetime import date, datetime
import pandas as pd
from pydantic.error_wrappers import ValidationError

from validation import UserValidation

DYNAMO_DB_TABLE_TABLE = 'dynamodb_users'
TABLE_NAME = 'dw_users'
S3_OUTPUT_FOLDER = f's3://etlone-data-lake-silver/{TABLE_NAME}/'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def data_validation(df: pd.DataFrame):
    """Helper to validate the input data

    Args:
        df (pd.DataFrame): input dataframe
    """
    for _, record in df.iterrows():
        try:
            UserValidation(**record.to_dict())
        except ValidationError as error:
            logger.error(f'Validation Error {error} in record: {record}')


def transform_data(df: pd.DataFrame):
    """Helper to transform input data

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        pd.DaraFrame: transformed pandas dataframe
    """
    df = df.drop_duplicates()
    df.loc[:, 'insert_timestamp'] = datetime.utcnow().isoformat()
    return df


def create_payload(data: dict):
    """Creates the payload

    Args:
        data (dict): input data

    Returns:
        dict: payload request
    """
    try:
        payload = UserValidation(**data).dict()
    except ValidationError:
        logger.error(f'cannot create payload for the inout data')
        return {
            'statusCode': 400,
            'reason': json.dumps('Invalid Input')
        }
    return payload


def handler(event, context):
    """Handler which gets invokes from Lambda and s3

    Args:
        event (dict): event that is captured when handler is invoked
        context (): [description]
    """
    logger.info(f'Event triggered: {json.dumps(event)}')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    logger.info(f'File {key} was uploaded to S3 bucket: {bucket}')

    data_df = wr.s3.read_csv(f's3://{bucket}/{key}')
    data_validation(data_df)
    logger.info('Data Validation completed...')
    data_df = transform_data(data_df)
    logger.info('Data Transformation completed...')
    wr.s3.to_parquet(df=data_df, index=False, compression='snappy',
                     dataset=True, mode='append', database='etlone',
                     table=TABLE_NAME, sanitize_columns=True,
                     path=f'{S3_OUTPUT_FOLDER}')
    logger.info(f'Data successfully loaded in SILVER stage...')

    # uncomment if you want to write to dynamo db
    # wr.dynamodb.put_df(df=data_df, table_name=DYNAMO_DB_TABLE_TABLE)
    # logger.info(f'Data successfully loaded in dynamo db...')
