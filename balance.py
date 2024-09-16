import json

def get_account_balance(account_id):
    # Load the JSON file
    with open('accounts.json', 'r') as file:
        accounts = json.load(file)
    
    # Iterate over the accounts to find the one with the given account_id
    for account in accounts:
        if account['account_id'] == account_id:
            return account['account_balance']
    
    # If account_id is not found
    return "Account not found"

# Example usage
# balance = get_account_balance('0001')
# print(f"Account balance: {balance}")


def update_account_balance(account_id, amount):
    # Load the JSON file
    with open('accounts.json', 'r') as file:
        accounts = json.load(file)
    
    # Flag to check if account was found
    account_found = False
    
    # Iterate over the accounts to find the one with the given account_id
    for account in accounts:
        if account['account_id'] == account_id:
            # Update the balance
            account['account_balance'] += amount
            account_found = True
            break
    
    # If the account_id is found, write the updated data back to the JSON file
    if account_found:
        with open('accounts.json', 'w') as file:
            json.dump(accounts, file, indent=4)
        return f"Account {account_id} updated successfully. New balance: {account['account_balance']}"
    else:
        return "Account not found"

# Example usage
# response = update_account_balance('0001', -150.0)  # Subtract 150 from account '0001'
# print(response)
