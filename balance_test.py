import unittest
from unittest.mock import mock_open, patch
import json

from balance import get_account_balance, update_account_balance


class TestGetAccountBalance(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"account_id": "0001", "account_balance": 500.0},
        {"account_id": "0020", "account_balance": 1000.0}
    ]))
    def test_get_account_balance_success(self, mock_file):
        # Call the function
        balance = get_account_balance("0001")

        # Assertions
        self.assertEqual(balance, 500.0)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"account_id": "0001", "account_balance": 500.0},
        {"account_id": "0020", "account_balance": 1000.0}
    ]))
    def test_get_account_balance_account_not_found(self, mock_file):
        # Call the function
        balance = get_account_balance("0003")

        # Assertions
        self.assertIsNone(balance)


class TestUpdateAccountBalance(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"account_id": "0001", "account_balance": 500.0},
        {"account_id": "0020", "account_balance": 1000.0}
    ]))
    def test_update_account_balance_success(self, mock_file):
        # Call the function
        new_balance = update_account_balance("0001", -150.0)

        # Assertions
        self.assertEqual(new_balance, 350.0)

        # Check the file was written to with the correct data
        expected_data = [
            {"account_id": "0001", "account_balance": 350.0},
            {"account_id": "0020", "account_balance": 1000.0}
        ]

        # Aggregate all the write calls
        handle = mock_file()
        written_data = ''.join(call.args[0]
                               for call in handle.write.call_args_list)

        # Check the final written content
        expected_json = json.dumps(expected_data, indent=4)
        self.assertEqual(written_data, expected_json)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"account_id": "0001", "account_balance": 500.0},
        {"account_id": "0020", "account_balance": 1000.0}
    ]))
    def test_update_account_balance_account_not_found(self, mock_file):
        # Call the function
        new_balance = update_account_balance("0003", 100.0)

        # Assertions
        self.assertIsNone(new_balance)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"account_id": "0001", "account_balance": 500.0},
        {"account_id": "0020", "account_balance": 1000.0}
    ]))
    def test_update_account_balance_file_write_error(self, mock_file):
        # Mocking return values
        mock_file.side_effect = IOError("File write error")

        # Call the function and Assertions
        with self.assertRaises(IOError):
            update_account_balance("0001", 100.0)


if __name__ == "__main__":
    unittest.main()
