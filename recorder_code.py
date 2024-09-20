import json
def recordTransaction(sender,receiver,amount,date):
    data= {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "date": date
    }

    with open('record.json', 'r+') as file:
    # Load the current data into a list
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = []  # If file is empty, start with an empty list
    
    # Append the new data (now stored in `data`) to the list
        existing_data.append(data)
    
    # Move the file pointer to the beginning of the file
        file.seek(0)
    
    # Write the updated list back to the file
        json.dump(existing_data, file, indent=4)

    # Truncate any leftover data (in case the new data is shorter than the original)
        file.truncate()
    
    bankTransfer(sender,receiver,amount)
    print(f"{date}: {sender} transfered {receiver} {amount} baht.")

def bankTransfer(sender, receiver, amount):
    sender_bank = get_bank(sender)
    receiver_bank = get_bank(receiver)
    with open('bank_record.json', 'r') as f: 
        data = json.load(f) 
    
    data[sender_bank] -= amount
    data[receiver_bank] += amount
    
    with open('bank_record.json', 'w') as f: 
        json.dump(data, f) 

def get_bank(ID):
    if int(ID)<15:
        return "Bank of America"
    else:
        return "Chase Bank"

#test code
if False:
    print(recordTransaction("0001","0003",float (999),"AUG 08 2003"))
    file = open('record.json', 'r')
    print (json.load(file))

if False:
    bankTransfer('0111',900)
