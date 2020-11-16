import pandas as pd

base_price = []


with open('prices.csv', 'r') as file:
    for row in file.readlines()[1:]:
        model, storage, price = row.replace("\n","").split(',')
        for carrier in ['Unlocked', 'Verizon', 'AT&T', 'T-Mobile', 'Sprint', 'Other']:
            for condition in ['Perfect', 'Good', 'Poor']:
                base_price.append((model, storage, carrier, condition, price))


df = pd.DataFrame(base_price)
df.columns = ['model', 'storage', 'carrier', 'condition', 'price']
print(df.head())
