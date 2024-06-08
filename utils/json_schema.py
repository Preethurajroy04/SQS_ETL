# JSON schema for the SQS message

schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "maxLength": 128
        },
        "device_type": {
            "type": ["string","null"],
            "maxLength": 32
        },
        "ip": {
            "type": "string",
            "maxLength": 128
        },
        "device_id": {
            "type": "string",
            "maxLength": 128
        },
        "locale": {
            "type": ["string","null"],
            "maxLength": 32
        },
        "app_version": {
            "type": ["string","null"],
            "maxLength": 32
        },
        "create_date": {
            "type": "string",
            "format": "date"
        }
    },
    "required": ["user_id", "ip", "device_id"],
    "additionalProperties": False
}
