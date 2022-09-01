import requests
from bs4 import BeautifulSoup
import fake_useragent


def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')    
    pages_ul = soup.find('div', class_="page-pagination page-pagination--center").find('ul')
    last_page = pages_ul.find_all('li')[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)


def get_product_info(product_url):
    html = get_html(product_url)
    soup = BeautifulSoup(html, 'lxml')
    img = soup.find("img",class_="product__gallery-photo--big").get("src")
    title = soup.find("h1").text
    price = soup.find("span", class_="price__inner--new product__price-new js-price-new").text.strip()
    if price[0] == "0":
        price = soup.find("span", class_="product__price-main js-price-old").text.strip()
    return {"title":title, "price":price, "img":img}
    

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_="js__products")
    products = product_list.find_all('div', class_="js__product")
    
    products_data = []

    for product in products:
        product_data = get_product_info(product.find("a").get("href"))
        products_data.append(product_data)

    return products_data

def main():
    import json
    machine_url = 'https://www.gulliver.ru/catalog/igrushki/roboty-i-transformery'
    pages = '?page={}'
    last_page = get_total_pages(get_html(machine_url))

    products = []
    for page in range(1, last_page+1): # last_page+1
        print(page)
        data = get_page_data(get_html(machine_url + pages.format(page)))
        products += data

    with open("parsed_data.json", "w") as f:
        f.write(json.dumps(products))

main()