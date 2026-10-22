from selenium.webdriver.chrome.webdriver import WebDriver

from src.config import settings
from src.core import logger
from src.pages import CatalogPage
from src.models import Book

class BookScraper:
    def __init__(self, driver: WebDriver):
        self.catalog_page = CatalogPage(driver)
        
    def collect_books(self) -> list[Book]:
        books: list[Book] = []
        next_page_url: str = settings.PAGE_URL
        page_number = 1
        
        while next_page_url:
            logger.info(f"Processing page {page_number}: {next_page_url}")
            self.catalog_page.open(next_page_url)
            
            collected_books = self.catalog_page.extract_all_books_from_page()
            books.extend(collected_books)
            logger.info(f"Collected {len(collected_books)} from page {page_number}")
            
            next_page_url = self.catalog_page.get_next_page_url()
            page_number += 1
            
        logger.info(f"Pagination completed. "
                    f"Total books collected: {len(books)}."
                    f" Total pages: {page_number}"
        )
        
        return books