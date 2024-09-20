import unittest
from unittest.mock import mock_open, patch
import json

from recorder_code import bankTransfer, get_bank, recordTransaction


class TestRecordTransaction(unittest.TestCase):

    @patch('builtins.print')
    @patch('recorder_code.bankTransfer')
    def test_record_transaction_successful(self, mock_bank_transfer, mock_print):
        # Patch open within the function
        with patch('builtins.open', new_callable=mock_open, read_data='[]') as mock_file:
            # Define test parameters
            sender = "sender123"
            receiver = "receiver456"
            amount = 100
            date = "2024-09-19 23:00:00.111111"

            # Call the function
            recordTransaction(sender, receiver, amount, date)

            # Assertions

            # Ensure the file was opened correctly
            mock_file.assert_called_once_with('record.json', 'r+')

            # Check that bankTransfer was called with correct arguments
            mock_bank_transfer.assert_called_once_with(
                sender, receiver, amount)

            # Check that the print function was called with the correct message
            mock_print.assert_called_once_with(
                f"{date}: {sender} transferred {receiver} {amount} baht.")

            # Check the file was written to with the correct data
            expected_data = [
                {
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    "date": date
                }
            ]
            # File pointer was moved to the beginning
            mock_file().seek.assert_called_once_with(0)
            # Ensure the file is truncated after writing
            mock_file().truncate.assert_called_once()

            # Aggregate all the write calls
            handle = mock_file()
            written_data = ''.join(call.args[0]
                                   for call in handle.write.call_args_list)

            # Check the final written content
            expected_json = json.dumps(expected_data, indent=4)
            self.assertEqual(written_data, expected_json)

    @patch('builtins.print')
    @patch('recorder_code.bankTransfer')
    def test_record_transaction_empty_file(self, mock_bank_transfer, mock_print):
        # Patch open with invalid JSON (simulate empty or corrupted file)
        with patch('builtins.open', new_callable=mock_open, read_data='') as mock_file:
            # Define test parameters
            sender = "sender123"
            receiver = "receiver456"
            amount = 100
            date = "2024-09-19 23:00:00.111111"

            # Call the function
            recordTransaction(sender, receiver, amount, date)

            # Assertions

            # Ensure the file was opened correctly
            mock_file.assert_called_once_with('record.json', 'r+')

            # Check that bankTransfer was called with correct arguments
            mock_bank_transfer.assert_called_once_with(
                sender, receiver, amount)

            # Check that the print function was called with the correct message
            mock_print.assert_called_once_with(
                f"{date}: {sender} transferred {receiver} {amount} baht.")

            # Check the file was written to with the correct data
            expected_data = [
                {
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    "date": date
                }
            ]
            mock_file().seek.assert_called_once_with(0)
            mock_file().truncate.assert_called_once()

            # Aggregate all write calls
            handle = mock_file()
            written_data = ''.join(call.args[0]
                                   for call in handle.write.call_args_list)

            # Check the final written content
            expected_json = json.dumps(expected_data, indent=4)
            self.assertEqual(written_data, expected_json)

    @patch('builtins.print')
    @patch('recorder_code.bankTransfer')
    def test_record_transaction_with_existing_data(self, mock_bank_transfer, mock_print):
        # Simulate existing data in the file
        existing_data = [
            {
                "sender": "sender001",
                "receiver": "receiver001",
                "amount": 200,
                "date": "2024-09-18 22:00:00.000000"
            }
        ]
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(existing_data)) as mock_file:
            # Define test parameters
            sender = "sender123"
            receiver = "receiver456"
            amount = 100
            date = "2024-09-19 23:00:00.111111"

            # Call the function
            recordTransaction(sender, receiver, amount, date)

            # Assertions

            # Ensure the file was opened correctly
            mock_file.assert_called_once_with('record.json', 'r+')

            # Check that bankTransfer was called with correct arguments
            mock_bank_transfer.assert_called_once_with(
                sender, receiver, amount)

            # Check that the print function was called with the correct message
            mock_print.assert_called_once_with(
                f"{date}: {sender} transferred {receiver} {amount} baht.")

            # Check the file was written to with the correct data
            expected_data = existing_data + [
                {
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    "date": date
                }
            ]
            mock_file().seek.assert_called_once_with(0)
            mock_file().truncate.assert_called_once()

            # Aggregate all write calls
            handle = mock_file()
            written_data = ''.join(call.args[0]
                                   for call in handle.write.call_args_list)

            # Check the final written content
            expected_json = json.dumps(expected_data, indent=4)
            self.assertEqual(written_data, expected_json)

    @patch('builtins.print')
    @patch('recorder_code.bankTransfer')
    def test_record_transaction_file_not_found(self, mock_bank_transfer, mock_print):
        # Simulate FileNotFoundError when trying to open the file in 'r+' mode
        mock_open_rplus = mock_open()
        # First call raises FileNotFoundError
        mock_open_rplus.side_effect = [FileNotFoundError, mock_open_rplus()]

        with patch('builtins.open', mock_open_rplus):
            # Define test parameters
            sender = "sender123"
            receiver = "receiver456"
            amount = 100
            date = "2024-09-19 23:00:00.111111"

            # Call the function
            recordTransaction(sender, receiver, amount, date)

            # Assertions

            # Check that bankTransfer was called with correct arguments
            mock_bank_transfer.assert_called_once_with(
                sender, receiver, amount)

            # Check that the print function was called with the correct message
            mock_print.assert_called_once_with(
                f"{date}: {sender} transferred {receiver} {amount} baht.")

            # Ensure that the file was attempted to be opened in 'r+' mode first
            mock_open_rplus.assert_any_call('record.json', 'r+')

            # Ensure that after FileNotFoundError, the file was opened in 'w' mode to create the file
            mock_open_rplus.assert_any_call('record.json', 'w')


class TestBankTransfer(unittest.TestCase):

    @patch('recorder_code.get_bank')
    def test_bank_transfer_successful(self, mock_get_bank):
        bank_data = {
            "bankA": 500,
            "bankB": 300
        }

        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(bank_data)) as mock_file:
            # Mock the return values
            mock_get_bank.side_effect = ["bankA", "bankB"]

            # Call the function
            bankTransfer("sender123", "receiver456", 100)

            # Assertions
            mock_get_bank.assert_any_call("sender123")
            mock_get_bank.assert_any_call("receiver456")

            # Ensure the file was opened correctly for reading
            mock_file.assert_any_call('bank_record.json', 'r')
            mock_file.assert_any_call('bank_record.json', 'w')

            # Check the file was written to with the correct data
            expected_data = {
                "bankA": 400,
                "bankB": 400
            }

            # # Ensure the file was opened correctly for writing
            # mock_file().write.assert_called_once_with(json.dumps())

            # Aggregate all the write calls
            handle = mock_file()
            written_data = ''.join(call.args[0]
                                   for call in handle.write.call_args_list)

            # Check the final written content
            expected_json = json.dumps(expected_data)
            self.assertEqual(written_data, expected_json)


    @patch('recorder_code.get_bank')
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_bank_transfer_file_not_found(self, mock_file, mock_get_bank):
        # Mock the return values for get_bank
        mock_get_bank.side_effect = ["bankA", "bankB"]

        # Call the function and assert that it raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            bankTransfer("sender123", "receiver456", 100)

        # Assertions

        # Ensure that get_bank was called for both sender and receiver
        mock_get_bank.assert_any_call("sender123")
        mock_get_bank.assert_any_call("receiver456")

        # Ensure the file was attempted to be opened in 'r' mode
        mock_file.assert_called_once_with('bank_record.json', 'r')

class TestGetBank(unittest.TestCase):

    def test_get_bank_below_threshold(self):
        # Test with ID below 15
        self.assertEqual(get_bank("10"), "Bank of America")

    def test_get_bank_at_threshold(self):
        # Test with ID exactly 15
        self.assertEqual(get_bank("15"), "Chase Bank")

    def test_get_bank_above_threshold(self):
        # Test with ID above 15
        self.assertEqual(get_bank("20"), "Chase Bank")

    def test_get_bank_non_numeric(self):
        # Test with non-numeric input
        with self.assertRaises(ValueError):
            get_bank("abc")

    def test_get_bank_negative(self):
        # Test with a negative ID
        self.assertEqual(get_bank("-5"), "Bank of America")


if __name__ == '__main__':
    unittest.main()
