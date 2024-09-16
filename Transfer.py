from balance import get_account_balance, update_account_balance
from recorder_code import recordTransaction
import datetime
#MAIN DRIVER CODE HERE#
def transfer_money(sender_id, receiver_id, amount):
    sender_balance = get_account_balance(sender_id)
    receiver_balance = get_account_balance(receiver_id)

    if sender_balance is None:
        print(f"Sender account {sender_id} not found.")
        return

    if receiver_balance is None:
        print(f"Receiver account {receiver_id} not found.")
        return

    if sender_balance < amount:
        print(f"Sender has insufficient funds to transfer {amount}.")
        return

    new_sender_balance = update_account_balance(sender_id, -amount)
    new_receiver_balance = update_account_balance(receiver_id, amount)

    print(f"Transfer of {amount}")
    print(new_sender_balance)
    print(new_receiver_balance)

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
    recordTransaction(sender_id,receiver_id,amount,get_account_balance(sender_id),str(datetime.datetime.now()))

if __name__ == "__main__":
    main()
