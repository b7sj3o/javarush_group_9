# import pandas as pd


# file_path = 'data/sales_report.xlsx'

# df = pd.read_excel(
#     file_path,
#     # usecols='A:D', # Вказуємо, які стовпці читати,
#     skiprows=2,
# )

# print(df.head(50))

# import pandas as pd
# # приклад DataFrame
# data = {'Product': ['Laptop', 'Mouse', 'Keyboard'], 'Price': [1200, 25, 75], 'Stock': [30, 150, 80]}

# df = pd.DataFrame(data)
# # --- Вибір стовпців за іменем ---
# # Вибір одного стовпця (результат - об'єкт Series)
# prices = df['Price']
# print(prices)
# # Вибір кількох стовпців (результат - новий DataFrame)
# product_info = df[['Product', 'Stock']]
# print(product_info)

# # --- Вибір рядків за числовим індексом за допомогою .iloc ---
# # Вибір другого рядка (індексація з 0)
# second_row = df.iloc[1]
# print(second_row, "\n")
# # Вибір перших двох рядків
# first_two_rows = df.iloc[0:2]
# print(first_two_rows)

# import pandas as pd
# import numpy as np # numpy потрібен для створення NaN
# # Дані з пропусками та дублікатами
# data = {'OrderID': [1, 2, 3, 4, 2],
#         'Product': ['A', 'B', 'A', 'C', 'B'],
#         'Amount': [100, 150, np.nan, 200, 150]}

# orders_df = pd.DataFrame(data)

# # Видалення повних дублікатів
# cleaned_df = orders_df.drop_duplicates()

# # Заповнення пропущених значень у стовпці 'Amount' середнім значенням
# mean_amount = cleaned_df['Amount'].mean()
# cleaned_df['Amount'] = cleaned_df['Amount'].fillna(mean_amount)

# print(cleaned_df)


# import pandas as pd

# data = {'Region': ['North', 'West', 'North', 'South', 'West'],
#         'Sales': [1000, 1500, 1200, 800, 1800]}

# sales_df = pd.DataFrame(data)

# # Групуємо дані за регіоном і рахуємо загальну суму продажів для кожного
# regional_sales = sales_df.groupby('Region')['Sales'].sum().reset_index()
# print(regional_sales)


# import pandas as pd
# # Дані про продажі за січень
# df_jan = pd.DataFrame({'Product': ['A', 'B'], 'Sales': [100, 150]})
# # Дані про продажі за лютий
# df_feb = pd.DataFrame({'Product': ['A', 'C'], 'Sales': [120, 200]})
# # Вертикально об'єднуємо два DataFrame
# total_sales = pd.concat([df_jan, df_feb], ignore_index=True)
# print(total_sales)

# import pandas as pd
# # Таблиця продажів
# sales = pd.DataFrame({'ProductID': [101, 102, 103], 'Amount': [2, 1, 5]})
# # Довідник продуктів
# products = pd.DataFrame({'ProductID': [101, 102, 104], 'Name': ['Widget', 'Gadget', 'Thingamajig']})
# # Об'єднуємо таблиці, щоб додати назви продуктів до продажів
# merged_df = pd.merge(sales, products, on='ProductID', how='left')
# print(merged_df)


import pandas as pd
data = {'Date': pd.to_datetime(['2023-01-05', '2023-01-05', '2023-01-06', '2023-01-06']),

'Region': ['North', 'South', 'North', 'South'],
'Sales': [100, 150, 120, 180]}

df = pd.DataFrame(data)
# Створюємо зведену таблицю:
# Індекс - дати, стовпці - регіони, значення - сума продажів
pivot = df.pivot_table(
    index='Date',
    columns='Region',
    values='Sales',
    aggfunc='sum'
)
print(pivot)