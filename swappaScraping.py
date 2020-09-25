import requests
from bs4 import BeautifulSoup
import xlsxwriter

workbook = xlsxwriter.Workbook('prices.xlsx')
worksheet = workbook.add_worksheet()

iphones = ['6', '6-plus', '6s', '6s-plus', '7', '7-plus', '8', '8-plus', 'x', 'xr', 'xs', 'xs-max', '11', '11-pro', '11-pro-max', 'se-2nd-gen']
carriers = ['unlocked', 'verizon', 'att', 't-mobile', 'sprint']

globalNameAndPrice = []
for phone in iphones:
    for carrier in carriers:
        url = f"https://swappa.com/sell/mobile/apple-iphone-{phone}?carrier={carrier}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        for i in soup.find_all('td'):
            phoneName = (i.get_text()[9:50]).replace("\t", "").replace("\n", "").replace("\r", "")
            price = (i.get_text()[1:6]).replace("\t", "").replace("\n", "").replace("\r", "")
            if phoneName != "":
                globalNameAndPrice.append(phoneName + ", " + carrier)
            if price != "":
                globalNameAndPrice.append(price)


name = globalNameAndPrice[::2]
price = globalNameAndPrice[1::2]

for i in range(1, len(name)+1):
    worksheet.write(f'A{i}', name[i-1])
    worksheet.write(f'B{i}', price[i-1])

workbook.close()