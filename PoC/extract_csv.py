import csv

#load csv file

def list_nicely():
    with open('data/chesterfield_25-08-2021_09-00-00.csv', 'r') as file:
        reader = csv.reader(file)
        chest_orders = []
        count = 0
        for record in reader:
            if count < 10:
                chest_orders.append(record)
                count += 1
            else: 
                break
        for record in chest_orders:
            print(f'{record}\n')
    
list_nicely()