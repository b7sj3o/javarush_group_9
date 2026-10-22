from pathlib import Path

from selenium import webdriver

PROFILE_DIR = Path(__file__).resolve().parent / "chrome_profile"


def create_driver(headless: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()

    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--window-size=1366,900")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


def installed_extensions(driver: webdriver.Chrome) -> list[dict]:
    driver.get("chrome://extensions-internals")
    data = driver.execute_script("return JSON.parse(document.body.innerText)")
    return [
        {
            "name": item["name"],
            "id": item["id"],
            "enabled": not item.get("disable_reasons"),
        }
        for item in data
        if item["location"] != "COMPONENT"
    ]
