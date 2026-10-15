from requests_html import HTMLSession

URL = "https://www.atbmarket.com/catalog/388-aktsiya-7-dniv"

with HTMLSession() as session:
    response = session.get(URL)
    
    response.html.render(sleep=10, timeout=40, scrolldown=3)  # Виконуємо рендеринг сторінки з прокруткою та затримкою
    
    print(response.html.html)  # Виводимо HTML-код сторінки для перевірки
    
    products = [{
        "title": el.html.find(".catalog-item__title a").text,
        "price": el.html.find("data.product-price__top").get("value"),
        "old_price": el.html.find("data.product-price__bottom").get("value")
        } for el in response.html.find("article.catalog-item")]
    
    print(products)
    
    for product in products:
        print(f"{product['title']} - {product['price']} (Old Price: {product['old_price']})")