from utils.database import connect_db, insert_db
from utils.transform import process_message
from utils.sqs import get_messages, delete_message
from utils.config import SQSConfig
import logging

# configure logging
logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to process messages from the SQS queue, transform them, and insert them into the database.
    """

    # Connect to the database
    logger.info("Connecting to the database...")
    conn = connect_db()
    if conn is None:
        return

    # Get messages from the SQS queue
    logger.info("Getting messages from the SQS queue...")
    messages = get_messages(SQSConfig.SQS_QUEUE_URL.value)
    if not messages:
        return

    # Process- trasnsform, validate schema and mask PII data in the message
    logger.info("Processing messages...")
    processed_messages = []
    for message in messages:
        processed_message = process_message(message)
        delete_message(SQSConfig.SQS_QUEUE_URL.value, message['ReceiptHandle'])
        if processed_message:
            processed_messages.append(processed_message)
        else:
            logger.error(f"Invalid message: {message}")
    
    if not processed_messages:
        logger.error("No valid messages to process.")
        return
    
    # Insert processed messages into the database
    logger.info("Inserting messages into the database...")
    db_insert_flag = insert_db(conn, processed_messages)
    if not db_insert_flag:
        return

if __name__ == '__main__':
    main()