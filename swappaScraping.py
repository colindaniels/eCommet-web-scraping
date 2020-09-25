import requests
from bs4 import BeautifulSoup
import xlsxwriter

iphones = ['6', '6-plus', '6s', '6s-plus', '7', '7-plus', '8', '8-plus', 'x', 'xr', 'xs', 'xs-max', '11', '11-pro', '11-pro-max', 'se-2nd-gen']
carriers = ['unlocked', 'verizon', 'att', 't-mobile', 'sprint']

phone_prices = []
for phone in iphones:
    for carrier in carriers:
        url = f"https://swappa.com/sell/mobile/apple-iphone-{phone}?carrier={carrier}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        tds = [td.text.replace("\t","").replace("\n","") for td in soup.find_all('td')]     # clean out all the junk
        pps = [[f"{phone}, {carrier}", price] for phone, price in zip(tds[::2], tds[1::2])] # zip two alternating tds together: [phone, price]
        phone_prices = phone_prices + pps

workbook = xlsxwriter.Workbook('prices.xlsx')
worksheet = workbook.add_worksheet()

for n, (phone,price)  in enumerate(phone_prices,start=1):  # enumerate adds a counter when going through a list
    print(n,phone,price) 
    worksheet.write(f'A{n}', phone)
    worksheet.write(f'B{n}', price)
workbook.close()

