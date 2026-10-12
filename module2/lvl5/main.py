import re
import csv
import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup


# if response.status_code == 200:
#     html_content = response.text
#     print("Page downloaded successfully!")
#     print(html_content[:500]) # Виводимо перші 500 символів для перевірки
# else:
#     print(f"Failed to download page. Status code: {response.status_code}")


# print(response.headers["Content-Type"])
# print(response.status_code)
# print(response.encoding)
# print(len(response.content))


# print(soup.title.string.strip())

# print(soup.find("p", class_="price_color").text.strip())
# print(soup.select_one("p.price_color").text.strip())

# print(soup.find_all("p", class_="price_color"))
# prices = soup.select("p.price_color")

# suma = 0

# for price in prices:
#     suma += float(price.text.strip()[1:])
    
# print(suma)

base_url = 'https://books.toscrape.com'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        if response.headers.get("Content-Type") != "text/html":
            logging.error("Повернута сторінка не є HTML")
            raise
        if not len(response.content):
            logging.error("Повернуто пусту HTML сторінку")
            raise
    except TimeoutError:
        logging.error(f"Не вдалось з'єднатись з сторінкою: {url}")
        raise
        
    except requests.exceptions.RequestException as e:
        logging.exception(f"Failed to download page")
        raise
        
    else:
        logging.info(f"Успішно завантажено сторінку '{url}'")
        return BeautifulSoup(response.content, "html.parser")
        


soup = get_soup(base_url)

links = [link.get("href") for link in soup.select("article.product_pod div a")]

fieldnames = ("title", "price", "stock", "suma")
scraped_data = []

for link in links[:5]:
    soup = get_soup(f"{base_url}/{link}")
    
    title = soup.select_one(".product_main h1").text.strip()
    price = float(soup.select_one("p.price_color").text.strip()[1:])
    stock = soup.select_one("p.instock.availability").text.strip()
    stock_number = int(re.findall(r'\d+', stock)[0])
    
    scraped_data.append({
        "title": title,
        "price": price,
        "stock": stock_number,
        "suma": round(price * stock_number, 2)
    })
    
    logging.info(f"'{title}' має {stock_number}шт, ціна/шт: £{price}")
    
    
with open("./data.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scraped_data)
    
    
df = pd.DataFrame(scraped_data)
df.to_excel('./books.xlsx', index=False)
    

    