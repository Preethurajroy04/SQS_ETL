# This file contains the database connection and query functions.
import psycopg2
from utils.config import DBConfig
from typing import List
import logging

logger = logging.getLogger(__name__)

def connect_db():
    """
    Connect to the database and return the connection object.

    :return: connection object
    """
    try:
        conn = psycopg2.connect(
            host=DBConfig.HOST.value,
            port=DBConfig.PORT.value,
            database=DBConfig.DATABASE.value,
            user=DBConfig.USER.value,
            password=DBConfig.PASSWORD.value
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None


def insert_db(conn, records: List[dict])->bool:
    """
    Insert records into the table user_logins.

    :param conn: database connection object
    :param record: list of records to insert
    :return: Boolean indicating success or failure
    """
    try:
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id,locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cur = conn.cursor()

        # Execute batch insert of records
        cur.executemany(insert_query, records)

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cur.close()
            
        return True
    
    except Exception as e:
        logger.error(f"Error inserting records into the database: {e}")
        conn.rollback()

        return False
    
    finally:
        conn.close()
        logger.info("Database connection closed.")
