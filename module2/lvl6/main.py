import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# response = requests.get("https://httpbin.org/headers", headers=headers)
# print(response.json())

# with requests.Session() as session:
#     response = session.get("https://httpbin.org/cookies/set?lang=uk&theme=dark", headers=headers)
#     print(session.cookies.get_dict())
#     print(session.get("https://httpbin.org/cookies", timeout=10).json())

#     print(requests.get("https://httpbin.org/cookies", timeout=10).json()) 