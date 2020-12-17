import config
import csv
import math

def reliablePrice(x):
    return 1-(1/(math.sqrt(x)+1)*3)

prices = []




# Get starting prices
with open('prices.csv', 'r') as file:
    for row in file.readlines()[1:]:
        model, storage, price = row.replace("\n","").split(',')
        for carrier in config.carrier_depreciation:
            for condition in config.condition_depreciation:
                prices.append((model, storage, carrier, condition, round(reliablePrice(float(price)) *
                                                                         float(price)*config.carrier_depreciation[carrier] *
                                                                         config.condition_depreciation[condition], 2)))


print(prices)



with open('all_prices.csv', 'w') as file:
    file.write('model,storage,carrier,condition,price\n')
    writer = csv.writer(file, delimiter=',')
    for row in prices:
        writer.writerow(row)
    file.close()

