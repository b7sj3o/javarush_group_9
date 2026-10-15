import csv
import logging
import random
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
import requests_cache
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

START_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("output")
TIMEOUT = (5, 15)  # (підключення, читання) у секундах
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_session() -> requests.Session:
    """Сесія з кешем, заголовками браузера і повторами при збоях."""
    session = requests_cache.CachedSession("books_cache", expire_after=3600)
    session.headers.update(HEADERS)

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_soup(session: requests.Session, url: str) -> BeautifulSoup:
    """Завантажує сторінку і повертає soup. Пауза лише для справжніх запитів."""
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    if not getattr(response, "from_cache", False):
        time.sleep(random.uniform(1, 3))

    return BeautifulSoup(response.content, "html.parser")


def parse_book(card, page_url: str) -> dict:
    """Одна картка книги -> словник."""
    link = card.select_one("h3 a")
    rating_class = card.select_one("p.star-rating")["class"][1]

    return {
        "title": link["title"],
        "price": float(card.select_one(".price_color").get_text(strip=True)[1:]),
        "rating": RATINGS.get(rating_class, 0),
        "in_stock": "In stock" in card.select_one(".availability").get_text(),
        "url": urljoin(page_url, link["href"]),
    }


def scrape_all(
    session: requests.Session, start_url: str, max_pages: int | None = None
) -> list[dict]:
    """Іде по сторінках, поки є кнопка next (або поки не досягне max_pages)."""
    books = []
    url = start_url
    page = 0

    while url:
        page += 1
        try:
            soup = fetch_soup(session, url)
        except requests.exceptions.RequestException as error:
            logger.error("Не вдалося завантажити %s: %s", url, error)
            break

        cards = soup.select("article.product_pod")
        books.extend(parse_book(card, url) for card in cards)
        logger.info("Сторінка %d: %d книг (усього %d)", page, len(cards), len(books))

        if max_pages and page >= max_pages:
            break

        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None

    return books


def save_csv(books: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
    logger.info("Збережено %d книг у %s", len(books), path)


def main() -> None:
    session = create_session()
    started = time.perf_counter()

    books = scrape_all(session, START_URL)
    if not books:
        logger.error("Не знайдено жодної книги")
        return

    save_csv(books, OUTPUT_DIR / "all_books.csv")
    logger.info("Готово за %.1f с", time.perf_counter() - started)


if __name__ == "__main__":
    main()