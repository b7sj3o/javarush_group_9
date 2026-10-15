from requests_html import HTMLSession


with HTMLSession() as session:
    response = session.get('https://quotes.toscrape.com/')

    response.html.render(scrolldown=1, sleep=1, timeout=20)

    video_titles = [el.text for el in response.html.find("span.text")]
    print(video_titles)