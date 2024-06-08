import json
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Tuple
from utils.json_schema import schema
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)
# Validate the SQS message against the JSON schema

def validate_message(message: dict)->bool:
    """
    Validate the message against the JSON schema.

    :param message: message to validate
    :return: Boolean indicating success or failure
    """
    try:
        validate(instance=message, schema=schema)
        return True
    except ValidationError as e:
        return False

# Mask PII data received in the SQS message

def mask_pii(data: str)->str:
    """
    Mask PII data in the message.

    :param data: message data
    :return: masked data
    """
    if data:
        return hashlib.sha256(data.encode()).hexdigest()
    else:
        return None
   
# Transform messages for insertion into the database

def process_message(message:Dict[str, str])->Tuple[str, str, str, str, str, str, str]:
    """
    validate and process message for insertion into the database.

    :param message: message to process
    :return: a tuple of processed message data or None if invalid
    """
    try:
        # Flatten the message body
        body = json.loads(message['Body'])

        if validate_message(body):
            mask_ip = mask_pii(body.get('ip'))
            mask_device_id = mask_pii(body.get('device_id'))

            # convert the app_version to integer
            app_version = int(body.get('app_version').replace('.', ''))

            data = (
                body.get('user_id'),
                body.get('device_type') or 'unknown_device',
                mask_ip,
                mask_device_id,
                body.get('locale') or 'unknown_locale',
                app_version,
                body.get('create_date', datetime.now().strftime('%Y-%m-%d'))
            )

            return data
        else:
            logger.error(f"Invalid message: {body}")
            return None

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return None
