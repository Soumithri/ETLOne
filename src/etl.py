import json
import logging

import awswrangler as wr
from datetime import date, datetime
import pandas as pd
from pydantic.error_wrappers import ValidationError

from validation import UserValidation

TABLE_NAME = 'dw_users'
S3_OUTPUT_FOLDER = f's3://etlone-data-lake-silver/{TABLE_NAME}/'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def data_validation(df: pd.DataFrame):
    for _, record in df.iterrows():
        try:
            UserValidation(**record.to_dict())
        except ValidationError as error:
            logger.error(f'Validation Error {error} in record: {record}')


def transform_data(df: pd.DataFrame):
    df = df.drop_duplicates()
    df.loc[:, 'insert_timestamp'] = datetime.utcnow().isoformat()
    return df


def handler(event, context):
    logger.info(f'Event triggered: {json.dumps(event)}')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    logger.info(f'File {key} was uploaded to S3 bucket: {bucket}')

    data_df = wr.s3.read_csv(f's3://{bucket}/{key}')
    # data_df = pd.read_csv('DATA.csv')
    data_validation(data_df)
    logger.info('Data Validation completed...')
    data_df = transform_data(data_df)
    logger.info('Data Transformation completed...')
    wr.s3.to_parquet(df=data_df, index=False, compression='snappy',
                     dataset=True, mode='append', database='etlone',
                     table=TABLE_NAME, sanitize_columns=True,
                     path=f'{S3_OUTPUT_FOLDER}')
    logger.info(f'Data successfully loaded in SILVER stage...')


if __name__ == '__main__':
    handler('', '')
