"""Пошук на YouTube: збирає відео з результатів пошуку в CSV (рівень 7).

Чому тут не підійде requests: у HTML, який віддає сервер, немає жодної картки відео.
Їх малює JavaScript у браузері, а дані підтягуються під час прокрутки.

Що робить скрипт:
- відкриває youtube.com і вводить запит у поле пошуку, як людина;
- чекає на перші результати (WebDriverWait);
- прокручує сторінку, поки не набере потрібну кількість відео або вони не скінчаться;
- з кожної картки бере назву, канал, перегляди, давність, тривалість і посилання;
- зберігає все в CSV і показує топ-5 за переглядами.

Запуск: python scrape_youtube.py "python tutorial"
"""

import csv
import logging
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_QUERY = "python tutorial"
MAX_VIDEOS = 50
OUTPUT = Path("output/youtube.csv")
HEADLESS = False  # True - браузер без вікна

SEARCH_BOX = (By.NAME, "search_query")
VIDEO = (By.CSS_SELECTOR, "ytd-video-renderer")

# "1,8 млн" -> 1_800_000; мову інтерфейсу фіксуємо через --lang=uk
MULTIPLIERS = {"тис.": 1_000, "млн": 1_000_000, "млрд": 1_000_000_000}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_driver(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    # Без цього формат переглядів залежить від мови системи ("1.8M views" замість "1,8 млн")
    options.add_argument("--lang=uk")
    return webdriver.Chrome(options=options)


def search(driver: webdriver.Chrome, query: str) -> None:
    driver.get("https://www.youtube.com/")
    box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SEARCH_BOX))
    box.clear()
    box.send_keys(query, Keys.ENTER)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located(VIDEO))


def count_videos(driver: webdriver.Chrome) -> int:
    return len(driver.find_elements(*VIDEO))


def more_videos_than(count: int):
    """Своя умова для WebDriverWait: карток стало більше, ніж count."""
    return lambda driver: count_videos(driver) > count


def scroll_results(driver: webdriver.Chrome, max_videos: int) -> int:
    """Прокручує, поки не набереться max_videos або поки не перестануть з'являтися нові."""
    wait = WebDriverWait(driver, 8)
    count = count_videos(driver)

    while count < max_videos:
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )
        try:
            wait.until(more_videos_than(count))
        except TimeoutException:
            logger.info("Нових відео немає, зупиняємось")
            break
        count = count_videos(driver)
        logger.info("Після прокрутки: %d відео", count)

    return count


def parse_views(text: str) -> int:
    """'1,8 млн' -> 1800000, '950 тис.' -> 950000, '734' -> 734."""
    match = re.match(r"([\d\s,]+)\s*(тис\.|млн|млрд)?", text.replace("\xa0", " "))
    if not match:
        return 0
    number = float(match.group(1).replace(" ", "").replace(",", "."))
    return int(number * MULTIPLIERS.get(match.group(2), 1))


def clean_url(href: str) -> str:
    """Прибирає службові параметри (&pp=..., &t=...).

    Звичайне відео -> https://www.youtube.com/watch?v=ID, Shorts -> https://www.youtube.com/shorts/ID.
    """
    parsed = urlparse(href)
    video_id = parse_qs(parsed.query).get("v", [""])[0]
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    return f"https://www.youtube.com{parsed.path}"


def text_or_empty(parent, selector: str) -> str:
    """Текст з DOM (textContent), а не видимий .text.

    Частина елементів на YouTube прихована або ще не домальована (ім'я каналу в спільних відео,
    тривалість на мініатюрі), і для них .text повертає ''.
    """
    try:
        element = parent.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return ""
    return element.get_attribute("textContent").strip().split("\n")[0].strip()


def parse_video(card) -> dict:
    link = card.find_element(By.CSS_SELECTOR, "a#video-title")
    meta = [
        item.text
        for item in card.find_elements(
            By.CSS_SELECTOR, "#metadata-line span.inline-metadata-item"
        )
    ]
    views_text = meta[0] if meta else ""

    return {
        "title": link.get_attribute("title"),
        "channel": text_or_empty(card, "#channel-info ytd-channel-name"),
        "views": parse_views(views_text),
        "views_text": views_text,
        "age": meta[1] if len(meta) > 1 else "",
        "duration": text_or_empty(card, "ytd-thumbnail-overlay-time-status-renderer"),
        "url": clean_url(link.get_attribute("href")),
    }


def save_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Збережено %d відео у %s", len(rows), path)


def main() -> None:
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY

    with create_driver(HEADLESS) as driver:
        logger.info("Шукаю: %s", query)
        search(driver, query)
        scroll_results(driver, MAX_VIDEOS)
        videos = []
        for card in driver.find_elements(*VIDEO)[:MAX_VIDEOS]:
            # YouTube може перемалювати картку, поки ми її читаємо: таку пропускаємо
            try:
                videos.append(parse_video(card))
            except (NoSuchElementException, StaleElementReferenceException) as error:
                logger.warning("Пропускаю картку: %s", type(error).__name__)

    if not videos:
        logger.error("Не знайдено жодного відео")
        return

    save_csv(videos, OUTPUT)
    print("\nТоп-5 за переглядами:")
    for video in sorted(videos, key=lambda v: v["views"], reverse=True)[:5]:
        print(f"{video['views_text']:>10}  {video['title'][:60]}  ({video['channel']})")


if __name__ == "__main__":
    main()
