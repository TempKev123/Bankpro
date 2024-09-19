import unittest
from unittest.mock import patch
from transfer import main, transfer_money  # Import from transfer.py

class TestTransferMoney(unittest.TestCase):
    
    @patch('transfer.get_account_balance')
    @patch('transfer.update_account_balance')
    @patch('transfer.recordTransaction')
    def test_successful_transfer(self, mock_record_transaction, mock_update_account_balance, mock_get_account_balance):
        # Mocking return values
        mock_get_account_balance.side_effect = [500, 300]  # Sender has 500, Receiver has 300
        mock_update_account_balance.side_effect = [400, 400]  # After transfer, new balances

        # Call the function
        transfer_money("sender123", "receiver456", 100)

        # Assertions
        mock_get_account_balance.assert_any_call("sender123")
        mock_get_account_balance.assert_any_call("receiver456")
        mock_update_account_balance.assert_any_call("sender123", -100)
        mock_update_account_balance.assert_any_call("receiver456", 100)
        mock_record_transaction.assert_called_once_with("sender123", "receiver456", 100, unittest.mock.ANY)

    @patch('transfer.get_account_balance', return_value=None)
    def test_sender_not_found(self, mock_get_account_balance):
        # Simulate sender account not found
        result = transfer_money("sender123", "receiver456", 100)
        
        # Check the output
        self.assertIsNone(result)
        mock_get_account_balance.assert_any_call("sender123")
        mock_get_account_balance.assert_any_call("receiver456")

    @patch('transfer.get_account_balance', side_effect=[500, None])
    def test_receiver_not_found(self, mock_get_account_balance):
        # Simulate receiver account not found
        result = transfer_money("sender123", "receiver456", 100)

        # Check the output
        self.assertIsNone(result)
        mock_get_account_balance.assert_any_call("sender123")
        mock_get_account_balance.assert_any_call("receiver456")

    @patch('transfer.get_account_balance', return_value=50)
    def test_insufficient_funds(self, mock_get_account_balance):
        # Simulate sender having insufficient funds
        result = transfer_money("sender123", "receiver456", 100)

        # Check the output
        self.assertIsNone(result)
        mock_get_account_balance.assert_any_call("sender123")
        mock_get_account_balance.assert_any_call("receiver456")

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=["sender123", "receiver456", "100"])  # Mock user inputs
    @patch('transfer.transfer_money')  # Mock transfer_money to avoid actual execution
    def test_main_successful_transfer(self, mock_transfer_money, mock_input):
        # Call the main function
        main()

        # Check that transfer_money was called with the correct arguments
        mock_transfer_money.assert_called_once_with("sender123", "receiver456", 100.0)

    @patch('builtins.input', side_effect=["sender123", "receiver456", "-100"])  # Negative amount input
    @patch('builtins.print')
    def test_main_negative_amount(self, mock_print, mock_input):
        # Call the main function
        main()
        
        # Check the output of print
        mock_print.assert_called_once()
        # Extract the argument passed to print and check its content
        args, _ = mock_print.call_args
        # Check if the output contains the expected error message
        self.assertEqual(str(args[0]), "Amount must be positive.")

    @patch('builtins.input', side_effect=["sender123", "receiver456", "invalid"])  # Invalid amount input
    @patch('builtins.print')
    def test_main_invalid_amount(self, mock_print, mock_input):
        # Call the main function
        main()

        # Check the output of print
        mock_print.assert_called_once()
        # Extract the argument passed to print and check its content
        args, _ = mock_print.call_args
        self.assertIn("could not convert string to float", str(args[0]))

if __name__ == '__main__':
    unittest.main()
