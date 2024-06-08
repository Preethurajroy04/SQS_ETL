import unittest
from unittest.mock import patch
from utils.sqs import get_messages, delete_message

class TestSQSOperations(unittest.TestCase):
    @patch('utils.sqs.sqs_client')
    def test_get_messages(self, mock_sqs_client):

        # Mock SQS client
        mock_sqs_client.receive_message.return_value = {
            'Messages': [
                {'MessageId': '1', 'ReceiptHandle': 'handle1', 'Body': '{"key": "value1"}'},
                {'MessageId': '2', 'ReceiptHandle': 'handle2', 'Body': '{"key": "value2"}'}
            ]
        }

        # Call the function
        messages = get_messages('test_queue_url')

        # Assert
        self.assertEqual(len(messages), 2)
        mock_sqs_client.receive_message.assert_called_once_with(
            QueueUrl='test_queue_url',
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )

    @patch('utils.sqs.sqs_client')
    def test_delete_message(self, mock_sqs_client):

        # Call the function
        delete_message('test_queue_url', 'test_receipt_handle')

        # Assert
        mock_sqs_client.delete_message.assert_called_once_with(
            QueueUrl='test_queue_url',
            ReceiptHandle='test_receipt_handle'
        )

if __name__ == '__main__':
    unittest.main()
