from balance import get_account_balance, update_account_balance
from recorder_code import recordTransaction
import datetime

#MAIN DRIVER CODE HERE#
def transfer_money(sender_id, receiver_id, amount):
    sender_balance = get_account_balance(sender_id)
    receiver_balance = get_account_balance(receiver_id)

    if sender_balance is None:
        print(f"Sender account {sender_id} not found.")
        return None

    if receiver_balance is None:
        print(f"Receiver account {receiver_id} not found.")
        return None

    if sender_balance < amount:
        print(f"Sender has insufficient funds to transfer {amount}.")
        return None

    new_sender_balance = update_account_balance(sender_id, -amount)
    new_receiver_balance = update_account_balance(receiver_id, amount)

    print(f"Transfer of {amount}")
    print(f"Account {sender_id} updated successfully. New balance: {new_sender_balance}")
    print(f"Account {receiver_id} updated successfully. New balance: {new_receiver_balance}")
    
    recordTransaction(sender_id,receiver_id,amount,str(datetime.datetime.now()))


def main():
    sender_id = input("Enter sender's account ID: ")
    receiver_id = input("Enter receiver's account ID: ")
    try:
        amount = float(input("Enter the amount to transfer: "))
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError as e:
        print(e)
        return
    
    transfer_money(sender_id, receiver_id, amount)

if __name__ == "__main__":
    main()
