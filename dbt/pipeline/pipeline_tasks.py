import os
import pandas as pd
import requests
import json
from io import StringIO
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import subprocess
import sys
from dotenv import load_dotenv
import logging



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def load_env_vars():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        'SF_USER': os.getenv('SF_USER'),
        'SF_ACCOUNT': os.getenv('SF_ACCOUNT'),
        'SF_ROLE': os.getenv('SF_ROLE'),
        'SF_SERVICE_USER_KEY': os.getenv('SF_SERVICE_USER_KEY', ''),
        'SF_PASSWORD': os.getenv('SF_PASSWORD', ''),
        'SF_WAREHOUSE': os.getenv('SF_WAREHOUSE'),
        'SF_DATABASE': os.getenv('SF_DATABASE'),
        'SF_SCHEMA': os.getenv('SF_SCHEMA'),
        'SF_RAW_SCHEMA': os.getenv('SF_RAW_SCHEMA'),
        'SF_RAW_DB_TABLE': os.getenv('SF_RAW_DB_TABLE'),
        'CSV_DATA_URL': os.getenv('CSV_DATA_URL')
    }


def download_csv(url: str) -> pd.DataFrame:
    """Download CSV from URL with enhanced error handling"""
    try:
        logger.info(f"Downloading CSV from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Raises an error if response code is not 200
        
        # Detect encoding automatically
        df = pd.read_csv(StringIO(response.text), encoding_errors='strict')
        
        if df.empty:
            raise ValueError("Downloaded CSV is empty")
            
        logger.info(f"Successfully downloaded {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"CSV download failed: {str(e)}")
        raise


def create_snowflake_connection(config: dict):
    """Create Snowflake connection with retry logic"""
    connection_args = {
        'user': config['SF_USER'],
        'account': config['SF_ACCOUNT'],
        'warehouse': config['SF_WAREHOUSE'],
        'database': config['SF_DATABASE'],
        'role': config['SF_ROLE'],
        'autocommit': False
    }

    if 'SF_PASSWORD' in config and config['SF_PASSWORD']:
        connection_args['password'] = config['SF_PASSWORD']
    elif 'SF_SERVICE_USER_KEY' in config and config['SF_SERVICE_USER_KEY']:
        connection_args['private_key'] = config['SF_SERVICE_USER_KEY']
    else:
        raise ValueError("Neither SNOWFLAKE_PASSWORD nor SNOWFLAKE_PRIVATE_KEY provided in config.")
    
    try:
        return snowflake.connector.connect(**connection_args)
    except Exception as e:
        logger.error(f"Snowflake connection failed: {str(e)}")
        raise


def load_to_snowflake(config: dict, df: pd.DataFrame, conn):
    """Load data to Snowflake with schema management"""
    try:
        schema = config['SF_RAW_SCHEMA']
        table = config['SF_RAW_DB_TABLE']

        success, _, nrows, _ = write_pandas(
            conn,
            df,
            table_name=table,
            schema=schema,
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False # Set to True in case of non-standard mixed/lower-case column or table names created with double quotes
        )
        if not success:
            raise RuntimeError("Snowflake load partially failed")

        logger.info(f"Successfully loaded {nrows} rows to {schema}.{table}")
    except Exception as e:
        logger.error(f"Snowflake load failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()


def run_dbt():
    """Run dbt commands with proper environment"""
    try:
        commands = [
            ['dbt', 'deps'],
            ['dbt', 'run', '--full-refresh'],
            ['dbt', 'test']
        ]
        
        for cmd in commands:
            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd='dbt_astro/dbt/dbt_astro_demo',
                check=True,
                text=True,
                capture_output=True
            )
            logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"dbt command failed: {e.stderr}")
        raise
