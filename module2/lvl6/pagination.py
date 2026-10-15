from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
books = []
page = 0
max_pages = 5       # на парі обмежуємо, щоб не чекати всі 50

while url:
    page += 1
    soup = BeautifulSoup(requests.get(url, timeout=10).content, "html.parser")
    for card in soup.select("article.product_pod"):
        books.append(card.select_one("h3 a")["title"])
    print(f"Сторінка {page}: усього {len(books)}")

    if page >= max_pages:
        break
    next_link = soup.select_one("li.next a")
    url = urljoin(url, next_link["href"]) if next_link else None

print(len(books))
