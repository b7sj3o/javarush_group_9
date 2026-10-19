import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 100)

# driver.get("https://formspree.io/library/application/simple-job-application-form/?tech=html")
# time.sleep(1)

# wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='preview']")))

# form = wait.until(
#     EC.visibility_of_element_located((By.CSS_SELECTOR, "form.fs-form.fs-layout__2-column"))
# )
# time.sleep(1)

# username_input = form.find_element(By.ID, "name")
# username_input.send_keys("admin")
# time.sleep(1)

# dob_input = form.find_element(By.ID, "dob")
# dob_input.send_keys("12-10-2001")
# time.sleep(1)

# email_input = form.find_element(By.ID, "email")
# email_input.send_keys("example@gmail.com")
# time.sleep(1)

# number_input = form.find_element(By.ID, "number")
# number_input.send_keys("0981234567")
# time.sleep(1)

# dates_input = Select(form.find_element(By.ID, "dates"))
# dates_input.select_by_index(1)
# time.sleep(1)

# start_date_input = form.find_element(By.ID, "start-date")
# start_date_input.send_keys("12-10-2026")
# time.sleep(1)

# form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


# username_input = driver.find_element(By.ID, "username")
# username_input.send_keys("admin")
# time.sleep(2)

# password_input = driver.find_element(By.ID, "password")
# password_input.send_keys("admin")
# time.sleep(2)

# submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'].btn.btn-primary")
# submit_btn.click()


# driver.get("https://testpages.eviltester.com/pages/forms/html-form/")

# username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
# username_input.send_keys("admin")
# time.sleep(1)

# password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
# password_input.send_keys("admin")
# time.sleep(1)

# textarea_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='comments']")
# textarea_input.send_keys("some comments...")
# time.sleep(1)

# filename_input = driver.find_element(By.CSS_SELECTOR, "input[name='filename']")
# filename_input.send_keys(r"D:\Desktop\teaching\group_9\module2\lvl7\img.avif")
# time.sleep(1)
# str(Path("upload.txt").resolve() - RELATIVE TO ABSOLUTE PATH

# checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='checkboxes[]']")
# for checkbox in checkboxes:
#     if checkbox.get_attribute("value") == "cb2" and not checkbox.is_selected:
#         checkbox.click()
# time.sleep(1)

# radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[name='radioval']")
# for radio_button in radio_buttons:
#     if radio_button.get_attribute("value") == "rd3":
#         radio_button.click()
# time.sleep(1)

# dates_input = Select(driver.find_element(By.CSS_SELECTOR, "select[name='dropdown'"))
# dates_input.select_by_value("dd5")
# time.sleep(1)

# driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
# driver.find_element(By.CSS_SELECTOR, "#start button").click()

# # 1. Без очікування
# try:
#     driver.find_element(By.ID, "finish")
# except NoSuchElementException:
#     print("Ще немає")                            # Ще немає

# # 2. Замало часу
# try:
#     WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "finish")))
# except TimeoutException:
#     print("За 2 с не з'явився")                  # За 2 с не з'явився

# # 3. Правильно
# start = time.perf_counter()
# finish = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "finish")))
# print(finish.text, f"{time.perf_counter() - start:.1f} с")       # Hello World! ~3 с (лишок від 5 с)


# driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
# driver.find_element(By.CSS_SELECTOR, "#start button").click()

# start = time.perf_counter()
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "finish")))
# print(f"presence: {time.perf_counter() - start:.2f} с, text={element.text!r}")    # presence: 0.01 с, text=''

# element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "finish")))
# print(f"visibility: {time.perf_counter() - start:.1f} с, text={element.text!r}")  # visibility: ~5 с, text='Hello World!'

# # Чекати конкретний текст
# driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
# driver.find_element(By.CSS_SELECTOR, "#start button").click()
# print(WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "finish"), "Hello")))   # True

# # Чекати, поки поле стане активним
# driver.get("https://the-internet.herokuapp.com/dynamic_controls")
# driver.find_element(By.CSS_SELECTOR, "#input-example button").click()       # кнопка Enable
# field = driver.find_element(By.CSS_SELECTOR, "#input-example input")
# print(field.is_enabled())                                                   # False
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable(field))
# print(field.is_enabled(), driver.find_element(By.ID, "message").text)       # True It's enabled!

# # Чекати список: quotes.toscrape малює цитати із затримкою (параметр delay у мілісекундах)
# driver.get("https://quotes.toscrape.com/js-delayed/?delay=3000")
# quotes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quote")))
# print(len(quotes))                     \                                     # 10, приблизно через 3 с


driver.get("https://youtube.com")

search_input = driver.find_element(By.CSS_SELECTOR, "input.ytSearchboxComponentInput.yt-searchbox-input.title")
search_input.send_keys("Python")
search_input.submit()
time.sleep(3)



for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f"Прокручування #{i+1}")

    time.sleep(3) # Тут time.sleep доречний, оскільки ми чекаємо AJAX-запит


all_posts = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
print(f"Усього знайдено {len(all_posts)} постів.")

time.sleep(100)
driver.quit()