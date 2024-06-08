import hashlib
import unittest
from utils.transform import mask_pii
from utils.transform import validate_message


class TestTransformFunctions(unittest.TestCase):

    def test_validate_message_valid(self):
        # Sample valid message
        valid_message = {
            "user_id": "user_1",
            "device_type": "android",
            "ip": "192.168.1.1",
            "device_id": "device_1",
            "locale": "US",
            "app_version": "1.0",
            "create_date": "2024-06-08"
        }
        # Test if validate_message function returns True for valid message
        self.assertTrue(validate_message(valid_message))

    def test_validate_message_invalid(self):
        # Sample invalid message (missing required fields)
        invalid_message = {
            "user_id": "user_1",
            "device_type": "android"
            # Missing fields like 'ip', 'device_id', etc.
        }
        # Test if validate_message function returns False for invalid message
        self.assertFalse(validate_message(invalid_message))

class TestMaskPii(unittest.TestCase):

    def test_mask_pii_valid(self):
        data = "test_data"
        expected_output = hashlib.sha256(data.encode()).hexdigest()

        # Test if mask_pii function returns the expected output
        self.assertEqual(mask_pii(data), expected_output)

    def test_mask_pii_none(self):
        # Test if mask_pii function returns None for None input
        self.assertIsNone(mask_pii(None))

if __name__ == '__main__':
    unittest.main()
