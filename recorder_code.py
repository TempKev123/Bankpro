import json
def recordTransaction(sender,receiver,amount,Balance,date):
    x= Balance-amount
    file = open('record.json', 'r')
    data={
    "sender": sender,
    "receiver": receiver,
    "amount": amount,
    "balance": x,
    "date": date
  }
    json_object = json.dumps(data, indent=5)
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
    bankTransfer(sender,amount)
    print(f"{date}: {sender} transfered {receiver} {amount} baht. Remaining balance: {x}")

def bankTransfer(ID,num):
    if int(ID)<15:
        g='Bank of America'
    else:
        g="Chase Bank"
    with open('bank_record.json', 'r') as f: 
        data = json.load(f) 
    data[g] = data[g]+num  # New value
    with open('bank_record.json', 'w') as f: 
        json.dump(data, f) 

#test code
if True:
    print(recordTransaction("0001","0003",float (999),float(1000),"AUG 08 2003"))
    file = open('record.json', 'r')
    print (json.load(file))

if False:
    bankTransfer('0111',900)
