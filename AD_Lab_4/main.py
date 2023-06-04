import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

data = pd.read_excel('Dataset.xlsx')

# Удаление всех транзакций, которые были сделаны в кредит
data['InvoiceNo'] = data['InvoiceNo'].astype('str')
data = data[~data['InvoiceNo'].str.contains('C')]

basket = (data.groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))

# Определение функции кодирования, чтобы сделать данные подходящими
# для соответствующих библиотек
def hot_encode(x):
    if (x <= 0): return 0
    if (x >= 1): return 1

# Кодирование набора данных
basket_encoded = basket.applymap(hot_encode)
basket = basket_encoded

# Построение модели
frq_items = apriori(basket, min_support=0.1, use_colnames=True)

# Сбор предполагаемых правил в кадре данных
rules = association_rules(frq_items, metric="lift", min_threshold=1)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
rules = rules.drop(['antecedent support', 'consequent support', 'leverage'], axis=1)
print(rules.head())
rules.to_excel('./Rules.xlsx')