import unittest
from unittest.mock import mock_open, patch
import json

from recorder_code import bankTransfer, get_bank, recordTransaction

class TestTransactionFunctions(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_recordTransaction(self, mock_open):
        # Mock data to return
        mock_file = mock_open()
        mock_file.read.side_effect = '[]'
        
        with patch('json.dump') as mock_dump, patch('json.load', return_value=[]):
            recordTransaction("0001", "0003", 999.0, "AUG 08 2003")
            
            # Check if open is called correctly
            mock_open.assert_called_with('record.json', 'r+')
            
            # Verify that json.dump is called with the correct arguments
            mock_dump.assert_called_once_with(
                [{"sender": "0001", "receiver": "0003", "amount": 999.0, "date": "AUG 08 2003"}],
                mock_open(),
                indent=4
            )

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "Bank of America": 1000,
        "Chase Bank": 500
    }))
    @patch('json.load', return_value={
        "Bank of America": 1000,
        "Chase Bank": 500
    })
    @patch('json.dump')
    def test_bankTransfer(self, mock_dump, mock_load, mock_open):
        # Mock data
        mock_file = mock_open()
        mock_file.read.side_effect = json.dumps({
            "Bank of America": 1000,
            "Chase Bank": 500
        })
        
        # Run the function
        with patch('get_bank', return_value='Bank of America'):
            bankTransfer("0001", "0003", 100)
        
        # Check if open is called correctly
        mock_open.assert_called_with('bank_record.json', 'w')
        
        # Verify json.dump is called with updated data
        mock_dump.assert_called_once_with({
            "Bank of America": 900,
            "Chase Bank": 600
        }, mock_open())

    def test_get_bank(self):
        # Test the function directly
        self.assertEqual(get_bank("0001"), "Bank of America")
        self.assertEqual(get_bank("1500"), "Chase Bank")

if __name__ == '__main__':
    unittest.main()
