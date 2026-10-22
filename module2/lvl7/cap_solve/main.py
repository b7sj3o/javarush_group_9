import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from browser import create_driver, installed_extensions

URL = "https://www.google.com/recaptcha/api2/demo"
CAPSOLVER = "Captcha Solver: Auto captcha solving service"

CHECKBOX_FRAME = (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
CHALLENGE_FRAME = (By.CSS_SELECTOR, "iframe[src*='api2/bframe']")
CHECKBOX = (By.ID, "recaptcha-anchor")

BLOCKED = (By.CSS_SELECTOR, ".rc-doscaptcha-header-text")


def is_checked(driver: WebDriver) -> bool:
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(*CHECKBOX_FRAME))
    checked = driver.find_element(*CHECKBOX).get_attribute("aria-checked") == "true"
    driver.switch_to.default_content()
    return checked


def captcha_state(driver: WebDriver) -> str | None:
    if is_checked(driver):
        return "solved"
    challenge = driver.find_elements(*CHALLENGE_FRAME)
    if not challenge:  # завдання ще не з'явилось
        return None
    driver.switch_to.frame(challenge[0])
    blocked = bool(driver.find_elements(*BLOCKED))
    driver.switch_to.default_content()
    return "blocked" if blocked else None


def wait_for_capsolver(driver: WebDriver, timeout: int = 120) -> bool:
    print("CapSolver розв'язує капчу...")
    try:
        result = WebDriverWait(driver, timeout, poll_frequency=2).until(captcha_state)
    except TimeoutException:
        result = "timeout"
    driver.switch_to.default_content()

    print("Результат:", result)
    if result == "blocked":
        print("Google тимчасово блокує цю IP. Спробуй за кілька годин")
    elif result == "timeout":
        print("Не встиг: перевір API-ключ і баланс у вікні розширення")
    return result == "solved"


def main() -> None:
    with create_driver() as driver:
        names = [extension["name"] for extension in installed_extensions(driver)]
        print("Розширення:", names)
        if CAPSOLVER not in names:
            print("Немає CapSolver: спершу запусти setup_profile.py")
            return

        driver.get(URL)
        if wait_for_capsolver(driver):
            driver.find_element(By.ID, "recaptcha-demo-submit").click()
            message = driver.find_element(By.CLASS_NAME, "recaptcha-success")
            print("Відповідь сайту:", message.text)
        
        input("Enter, щоб закрити браузер... ")


if __name__ == "__main__":
    main()
