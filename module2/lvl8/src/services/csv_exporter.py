import csv

from src.core import logger
from src.models import Book

class CSVExporter:
    HEADERS = ("title", "price", "rating", "in_stock", "img_path", "html_path")

    def export_books(self, books: list[Book], output_path: str) -> None:
        logger.info(f"Exporting {len(books)} books to '{output_path}'.")

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADERS)

            for book in books:
                writer.writerow((book.title, book.price, book.rating, book.in_stock, book.img_path, book.html_path))

        logger.info("CSV export completed.")