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
    return (f"{date}: {sender} transfered {receiver} {amount} baht. Remaining balance: {x}")
    
#test code
if False:
    print(recordTransaction("kim","joe",float (999.30),float(1000.80),"AUG 08 2003"))
    file = open('record.json', 'r')
    print (json.load(file))
