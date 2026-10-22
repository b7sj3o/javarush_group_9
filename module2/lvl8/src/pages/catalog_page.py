from urllib.parse import urljoin

from selenium.common import NoSuchElementException

from src.models import Book
from src.pages import BasePage
from src.locators import CatalogLocators
from src.utils import word_to_number
from src.core import logger

class CatalogPage(BasePage):
    
    def extract_all_books_from_page(self) -> list[Book]:
        books: list[Book] = []
        book_cards = self.wait_for_all_elements(CatalogLocators.BOOK_CARD)
        
        for card in book_cards:
            
            img_path = card.find_element(*CatalogLocators.BOOK_IMG).get_attribute("src")
            html_path = card.find_element(*CatalogLocators.BOOK_DETAILED_PAGE).get_attribute("href")
            
            
            books.append(
                Book(
                    title=card.find_element(*CatalogLocators.BOOK_TITLE).get_attribute("title").strip(),
                    rating=word_to_number(card.find_element(*CatalogLocators.BOOK_RATING).get_attribute("class")),
                    price=float(card.find_element(*CatalogLocators.BOOK_PRICE).text[1:]),
                    in_stock=bool(card.find_elements(*CatalogLocators.BOOK_IN_STOCK)),
                    img_path=urljoin(self.driver.current_url, img_path),
                    html_path=urljoin(self.driver.current_url, html_path)
                )
            )
        
        return books
    
    def get_next_page_url(self) -> str | None:
        try:
            next_page_button = self.driver.find_element(*CatalogLocators.NEXT_BUTTON)
        except NoSuchElementException:
            logger.warning("There is no next page url")
            return None
        
        return urljoin(self.driver.current_url, next_page_button.get_attribute("href"))
    