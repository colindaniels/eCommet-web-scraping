import pandas as pd
from matplotlib import pyplot as plt

prices = pd.read_csv('prices.csv')


x_axis = prices['Model']
y_axis = prices['Avg_Sale_Price']

plt.bar(x_axis, y_axis)
plt.xticks(rotation='vertical')
plt.show()
