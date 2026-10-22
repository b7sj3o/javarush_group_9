from src.core import create_chrome_driver, logger
from src.scrapers import BookScraper
from src.services import CSVExporter
from src.config import settings


def main():
    logger.info("Scraper started")
    driver = create_chrome_driver()
    
    try:
        book_scraper = BookScraper(driver)
        csv_exporter = CSVExporter()

        books = book_scraper.collect_books()
        csv_exporter.export_books(books, settings.OUTPUT_CSV_PATH)
    except Exception as e:
        logger.error(f"Error while scraping books: {e}")
        raise
    finally:
        logger.info("Closing browser")
        driver.quit()
        logger.info("Browser closed")
    
    
if __name__ == "__main__":
    try:
        main()
    except OSError:
        logger.warning("Closing driver from Keyboard")