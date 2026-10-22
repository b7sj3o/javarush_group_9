from pathlib import Path

class Settings:
    PAGE_URL = "https://books.toscrape.com/catalogue/page-40.html"
    OUTPUT_CSV_PATH = Path("books_data.csv")
    WAIT_TIMEOUT_SECONDS = 10
    PAGE_LOAD_TIMEOUT_SECONDS = 30
    HEADLESS = False
    
    
settings = Settings()