import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# options = Options()
# options.add_argument(r"--user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data")
# options.add_argument(r"--profile-directory=Default")
# options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 100)

URL = "https://www.linkedin.com/jobs/search-results?keywords={q}"

driver.get(URL.format(q="python middle dev"))

time.sleep(100)
driver.quit()