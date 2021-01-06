import requests
from bs4 import BeautifulSoup
import csv
import math
import config
from tqdm import tqdm

# Declaring lists from config.py
iPhones = config.iPhones
apple_watches = config.apple_watches
samsung = config.samsung

# All prices before variations
device_prices = []

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
    pbar = tqdm(total=len(device['devices']))
    for progress, variation in enumerate(device['devices']):
        # Prints progress of program
        pbar.update(n=1)
        # Scraping
        url = f"https://swappa.com/sell/{device['web-prefix']}/{device['brand']}-{variation}?carrier=unlocked"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Finds all values in table '<td>' tag
        if device['price-tag'] == 'td':
            model_list = [value.text.strip() for value in soup.find_all('td')]
            for model, price in zip(model_list[::2], model_list[1::2]):
                device_prices.append([model, int(price[1:])])

        else:
            model = soup.find(class_='col-xs-12').find('h1').text.strip()[5:-16]
            if device['price-tag'] == 'h2':
                # Finds all values in any other tag with specified title and price tags in config.py
                price = int(soup.find(class_=device['price-class']).find_all(device['price-tag'])[device['price-index']].text.strip()[1:])
                device_prices.append([model, price])
            elif device['price-tag'] == 'span':
                price = soup.find(class_=device['price-class']).text.strip()
                device_prices.append([model, int(price)])

    print(device_prices)
scrape(iPhones)



with open("buy_prices.csv", 'w') as file:
    file.write('model,storage,price\n')
    for n, (device, price) in enumerate(device_prices, start=1):
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
