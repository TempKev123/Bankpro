import json
import unittest
from unittest.mock import patch, mock_open
from balance import get_account_balance, update_account_balance

class TestGetAccountBalance(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='[{"account_id": "0001", "account_balance": 100.0}]')
    def test_get_account_balance_success(self, mock_file):
        balance = get_account_balance('0001')
        self.assertEqual(balance, 100.0)
        mock_file.assert_called_once_with('accounts.json', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='[{"account_id": "0001", "account_balance": 100.0}]')
    def test_get_account_balance_not_found(self, mock_file):
        balance = get_account_balance('9999')
        self.assertIsNone(balance)
        mock_file.assert_called_once_with('accounts.json', 'r')
    
    @patch('builtins.open', new_callable=mock_open, read_data='[{"account_id": "0001", "account_balance": 100.0}]')
    @patch('json.load', return_value='[{"account_id": "0001", "account_balance": 100.0"}]')
    def test_update_account_balance_success(self, mock_json_load, mock_file):
        # Mock the file write operation
        with patch('builtins.open', mock_open()) as mock_file_write:
            # Call the function
            new_balance = update_account_balance('0001', 50.0)
            self.assertEqual(new_balance, 150.0)

            # Verify file read and write calls
            mock_file.assert_called_once_with('accounts.json', 'r')
            mock_file_write.assert_called_once_with('accounts.json', 'w')

            # Check the written data
            written_data = json.loads(mock_file_write().write.call_args[0][0])
            self.assertEqual(written_data, [{"account_id": "0001", "account_balance": 150.0}])
            
            # Verify json.dump is called with correct data
            with patch('json.dump') as mock_json_dump:
                mock_json_dump.assert_called_once_with([{"account_id": "0001", "account_balance": 150.0}], mock_file_write(), indent=4)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"account_id": "0001", "account_balance": 100.0}]')
    @patch('json.load', return_value=[{"account_id": "0001", "account_balance": 100.0}])
    def test_update_account_balance_not_found(self, mock_json_load, mock_file):
        # Mock the file write operation
        with patch('builtins.open', mock_open()) as mock_file_write:
            # Call the function
            new_balance = update_account_balance('9999', 50.0)
            self.assertIsNone(new_balance)

            # Verify file read and write calls
            mock_file.assert_called_once_with('accounts.json', 'r')
            mock_file_write.assert_not_called()  # Should not call write if account not found

if __name__ == '__main__':
    unittest.main()
