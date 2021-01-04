import requests
from bs4 import BeautifulSoup
import csv
import math
import config

# Declaring lists from config.py
iPhones = config.iPhones
apple_watches = config.apple_watches

# All prices before variations
phone_prices = []

# Buy prices using the calculate_buy function
buy_prices = []

# Sell Prices using the calc_sell_price function
sell_prices = []

# Exponential function that accounts for a price that will be guaranteed to sell at and profit margins when buy prices are low or high
def reliable_price(price):
    return 1-(1/(math.sqrt(price)+1)*3)

# Changes price values to be put in buy_prices.csv
def calculate_buy(data):
    data.append((model, storage, carrier, condition, (round(reliable_price(float(price)) *
                                                                         float(price)*config.carrier_depreciation[carrier] *
                                                                         config.condition_depreciation[condition], 2))))

# Calculates new prices from buy_prices to sell_prices
def calc_sell_price(row):
    model, storage, carrier, condition, price = row
    price = float(price)
    price = price-((price * config.ebay_fee) + (price * config.sales_tax) + (price * config.company_percentage)) - config.buying_shipping          # calculation
    price = str(round(price,2) )
    return [model, storage, carrier, condition, price]

#scrapes models and prices from swappa.com
def scrape(device):
    for progress, variation in enumerate(device['devices']):
        url = f"https://swappa.com/sell/{device['web-prefix']}/apple-{variation}?carrier=unlocked"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # If the prices are found in a <td> tag
        if device['type'] == '<td>':
            model = soup.find('td').text.strip()
            price = soup.find_all('td')[1].text.strip()
            phone_prices.append([model, price])
        # If the prices are found in a <h2> tag
        elif device['type'] == '<h2>':
            # Finds title of product and removes the "Get more green." string after name.
            model = soup.find('h1').text.strip()[:-16]
            # Finds price of product at the 3rd index of <h2>
            price = soup.find_all('h2')[3].text.strip()
            phone_prices.append([model, price])
            print(model, price)
        print(f"{round(progress/len(iPhones['devices'])*100, 1)}% Complete")
    print('100% Complete')

scrape(iPhones)

with open("buy_prices.csv", 'w') as file:
    file.write('model,storage,price\n')
    for n, (device, price) in enumerate(phone_prices, start=1):
        price = int(price[1:])
        file.write(device.replace(" ","") + ',' + str(price) + '\n')
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
