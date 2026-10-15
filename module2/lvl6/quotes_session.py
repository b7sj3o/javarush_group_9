import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"
LOGIN_URL = "https://quotes.toscrape.com/login"

session = requests.Session()

response = session.get(LOGIN_URL)
soup = BeautifulSoup(response.content, "html.parser")
token = soup.select_one("input[name='csrf_token']").get("value")



response = session.post(
    LOGIN_URL,
    data={
        "csrf_token": token,
        "username": "testuser",
        "password": "12345"
    }
)

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

print(soup.select_one("a[href='/login']"))
print(soup.select_one("a[href='/logout']"))
