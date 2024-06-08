import boto3
import logging

logger = logging.getLogger(__name__)

sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566')

def get_messages(queue_url: str)->list:
    """
    Get messages from the SQS queue.

    :param queue_url: URL of the SQS queue
    :return: list of messages
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            WaitTimeSeconds=10,
            MaxNumberOfMessages=10
        )
        return response.get('Messages', [])
    
    except Exception as e:
        logger.error(f"Error getting messages from the queue: {e}")
        return []

def delete_message(queue_url: str, receipt_handle: str)->bool:
    """
    Delete a message from the SQS queue.

    :param queue_url: URL of the SQS queue
    :param receipt_handle: receipt handle of the message
    :return: Boolean indicating success or failure
    """
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return True
    
    except Exception as e:
        logger.error(f"Error deleting message from the queue: {e}")
        return False
