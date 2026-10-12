import csv
import logging
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path(__file__).parent / "output"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def fetch_html(url: str) -> bytes | None:
    """Завантажує сторінку. Повертає байти HTML або None, якщо щось пішло не так."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Таймаут: %s", url)
        return None
    except requests.exceptions.RequestException as e:
        logger.error("Помилка запиту %s: %s", url, e)
        return None
    logger.info("Отримано %s (%s байт)", url, len(response.content))
    return response.content


def parse_book(card: Tag, page_url: str) -> dict:
    """Дістає з однієї картки <article class="product_pod"> словник з даними книги."""
    link = card.select_one("h3 a")
    price_text = card.select_one(".price_color").get_text(strip=True)  # '£51.77'
    rating_word = card.select_one(".star-rating")["class"][1]  # 'Three'
    return {
        "title": link["title"],
        "price": float(price_text.replace("£", "")),
        "rating": RATINGS.get(rating_word, 0),
        "in_stock": "In stock" in card.select_one(".availability").get_text(),
        "url": urljoin(page_url, link["href"]),
    }
    
    
def parse_books(html: bytes, page_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        try:
            books.append(parse_book(card, page_url))
        except (AttributeError, KeyError, ValueError) as e:
            logger.warning("Пропускаю картку: %s", e)  # одна зламана картка не валить весь скрипт
    return books


def save_csv(books: list[dict], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
        
        
def save_excel(books: list[dict], path: Path) -> None:
    df = pd.DataFrame(books)
    df.to_excel(path, index=False)
    

def main() -> None:
    html = fetch_html(BASE_URL)
    if html is None:
        return

    books = parse_books(html, BASE_URL)
    if not books:
        logger.warning("Не знайдено жодної книги - можливо, змінилась верстка")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    save_csv(books, OUTPUT_DIR / "books.csv")
    save_excel(books, OUTPUT_DIR / "books.xlsx")
    logger.info("Збережено %s книг у %s", len(books), OUTPUT_DIR)


if __name__ == "__main__":
    main()