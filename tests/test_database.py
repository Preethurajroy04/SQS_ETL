import unittest
from unittest.mock import patch, MagicMock
from utils.database import insert_db, connect_db

class TestDatabaseOperations(unittest.TestCase):
    @patch('utils.database.psycopg2.connect')
    def test_connect_db(self, mock_connect):
        # Mock the connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Test connection to the database
        conn = connect_db()
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()
        conn.close()
        mock_conn.close.assert_called_once()

    @patch('utils.database.psycopg2.connect')
    def test_insert_db(self, mock_connect):
        # Mock the connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # sample records
        data = [('user_1', 'android', 'masked_ip1', 'masked_device_1', 'US', 123, '2024-06-08')]

        insert_db(mock_conn, data)


        mock_cursor.executemany.assert_called_once()

        # Check if the connection committed
        mock_conn.commit.assert_called_once()

        # Check if the cursor and connection were closed
        mock_cursor.close.assert_called_once()
       
        
if __name__ == '__main__':
    unittest.main()