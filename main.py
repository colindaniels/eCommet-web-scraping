import requests
from bs4 import BeautifulSoup
import csv
import math
import config

# exponential function that accounts for a price I will be garunteed to sell at and profit margins when buy prices are low or high
def reliable_price(price):
    return 1-(1/(math.sqrt(price)+1)*3)

def calculate_buy(data):
    data.append((model, storage, carrier, condition, (round(reliable_price(float(price)) *
                                                                         float(price)*config.carrier_depreciation[carrier] *
                                                                         config.condition_depreciation[condition], 2))))

iPhones = config.models
phone_prices = [] #all prices before variations
buy_prices = [] #all price variations
sell_prices = []

for progress, phone in enumerate(iPhones):
    url = f"https://swappa.com/sell/mobile/apple-iphone-{phone}?carrier=unlocked"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tds = [td.text.replace("\t","").replace("\n","") for td in soup.find_all('td')]     # clean out all the junk
    pps = [[f"{phone}", price] for phone, price in zip(tds[::2], tds[1::2])] # zip two alternating tds together: [phone, price]
    phone_prices = phone_prices + pps
    print(f'{round(progress/len(iPhones)*100, 1)}% Complete')
print('100% Complete')
with open("buy_prices.csv", 'w') as file:
    file.write('model,storage,price\n')
    for n, (phone, price) in enumerate(phone_prices, start=1):
        price = int(price[1:])
        file.write(phone.replace(" ","") + ',' + str(price) + '\n')
    file.close()

# Get starting prices
with open('buy_prices.csv', 'r') as file:
    for row in file.readlines()[1:]:
        model, storage, price = row.replace("\n","").split(',')
        for carrier in config.carrier_depreciation:
            for condition in config.condition_depreciation:
                calculate_buy(buy_prices)



with open('buy_prices.csv', 'w') as file:
    file.write('model,storage,carrier,condition,price\n')
    writer = csv.writer(file, delimiter=',')
    for row in buy_prices:
        writer.writerow(row)
    file.close()

def calc_sell_price(row):
    model, storage, carrier, condition, price = row
    price = float(price)           # str -> float
    price = 1.2 * price            # calculation
    price = str(round(price,2) )   # float -> str
    return [model, storage, carrier, condition, price]

with open('sell_prices.csv', 'w') as sell_file:
    sell_file.write('model,storage,carrier,condition,price\n')
    with open('buy_prices.csv', 'r') as buy_file:
        reader = csv.reader(buy_file, delimiter=',')
        reader.__next__() # get rid of the header
        for row in reader:
            row = calc_sell_price(row) # update price
            sell_file.write(','.join(row)+'\n')
        buy_file.close()
    sell_file.close()

# original colde
# with open('sell_prices.csv', 'w') as file:
#     file.write('model,storage,carrier,condition,price\n')
#     writer = csv.writer(file, delimiter=',')
#     for row in sell_prices:
#         writer.writerow(row)
#     file.close()
