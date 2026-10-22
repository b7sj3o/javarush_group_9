from selenium.webdriver import ChromeOptions, ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver

from src.config import settings
from src.core import logger


def create_chrome_driver(headless: bool = settings.HEADLESS) -> WebDriver:
    options = ChromeOptions()
    
    options.add_argument("--start-maximized")
    
    if headless:
        options.add_argument("--headless=new")
        
    logger.info(f"Creating chrome driver with params: headless={headless}")
        
    driver = WebDriver(options=options)
    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT_SECONDS)
    
    logger.info(f"Chrome driver created, Chrome {driver.capabilities['browserVersion']}")
    
    
    return driver