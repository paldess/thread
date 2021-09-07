import asyncio
import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
import time

time_ = time.time()

bd = MongoClient('localhost', 27017)
base = bd.new_books['book24-психология']

url = 'https://book24.ru'
params = {'q': 'психология'}
headers = {'user_ahent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
# books = []



async def pages(dom):
    response = requests.get(url+dom, params=params, headers=headers)
    page = html.fromstring(response.text)
    name = page.xpath('//h1[@itemprop="name"]/text()')[0].replace('\n', '')
    prices = page.xpath('//span[@class="app-price product-sidebar-price__price"]/text()')[0].replace('\n', '').split()
    price = int(prices[0])
    currency = prices[1]
    book = {'name': name, 'price': price, 'currency': currency}
    # books.append({'name': name, 'price': price, 'currency': currency})
    base.insert_one(book)
    print(name)


x = 1
while True:

    response = requests.get(f'{url}/search/page-{x}', params=params, headers=headers)
    if response.status_code != 200:
        break
    dom = html.fromstring(response.text)
    links = dom.xpath('//div[@class="product-list__item"]//a[@class="product-card__image-link smartLink"]/@href')
    x += 1

    for i in range(len(links)):
        loop = asyncio.get_event_loop()
        task = loop.run_until_complete(pages(links[i]))

    print(time.time()-time_)






