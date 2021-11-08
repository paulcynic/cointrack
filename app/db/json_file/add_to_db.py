import json
import csv


#with open("currencies.json", "r") as db:
#    currencies = json.load(db)
#    with open("currencies.csv", "w", encoding="utf-8") as f:
#        writer = csv.writer(f)
#        for i in range(len(currencies)):
#            writer.writerow([i + 1, currencies[i], 'null'])
#print("All right!")



with open("coin.json", "r") as db:
    coins = json.load(db)
    with open("coins.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        count = 1
        for i in coins:
            writer.writerow([count, i['symbol'], i['name']])
            count += 1
print("All right!")
