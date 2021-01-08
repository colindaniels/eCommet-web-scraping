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

# Appends prices to empty list to be put in buy_prices.csv
def calculate_buy(data):
    data.append((model, storage, carrier, condition, (round(reliable_price(float(price)) *
                                                                         float(price)*config.carrier_depreciation[carrier] *
                                                                         config.condition_depreciation[condition], 2))))

# Calculates sell prices
def calculate_sell(price):
    return round(price-((price * config.ebay_fee) + (price * config.sales_tax) + (price * config.company_percentage)) - config.buying_shipping, 2)

def write_csv(file_name, prices_list):
    with open(file_name, 'w') as file:
        file.write('model,storage,carrier,condition,price\n')
        writer = csv.writer(file, delimiter=',')
        for row in prices_list:
            writer.writerow(row)
        file.close()

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
                device_and_model = model.split(', ')
                device_and_model.append(int(price[1:]))
                device_prices.append(device_and_model)

        else:
            model = soup.find(class_='col-xs-12').find('h1').text.strip()[5:-16]
            if device['price-tag'] == 'h2':
                # Finds all values in any other tag with specified title and price tags in config.py
                price = int(soup.find(class_=device['price-class']).find_all(device['price-tag'])[device['price-index']].text.strip()[1:])
                device_prices.append([model, price])
            elif device['price-tag'] == 'span':
                price = soup.find(class_=device['price-class']).text.strip()
                device_prices.append([model, int(price)])

scrape(iPhones)


# Get starting prices


for element in device_prices:
    model, storage, price = element
    for carrier in config.carrier_depreciation:
        for condition in config.condition_depreciation:
            calculate_buy(buy_prices)

for model, storage, carrier, condition, price in buy_prices:
    price = calculate_sell(price)
    sell_prices.append((model, storage, carrier, condition, price))


write_csv('buy_prices.csv', buy_prices)
write_csv('sell_prices.csv', sell_prices)