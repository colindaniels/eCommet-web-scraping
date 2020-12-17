import requests
from bs4 import BeautifulSoup
import config
iPhones = config.models

phone_prices = []
for phone in iPhones:
    url = f"https://swappa.com/sell/mobile/apple-iphone-{phone}?carrier=unlocked"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tds = [td.text.replace("\t","").replace("\n","") for td in soup.find_all('td')]     # clean out all the junk
    pps = [[f"{phone}", price] for phone, price in zip(tds[::2], tds[1::2])] # zip two alternating tds together: [phone, price]
    phone_prices = phone_prices + pps

with open("prices.csv", 'w') as file:
    file.write('model,storage,price\n')
    for n, (phone, price) in enumerate(phone_prices, start=1):
        price = int(price[1:])
        print(price)
        file.write(phone.replace(" ","") + ',' + str(price) + '\n')
    file.close()
