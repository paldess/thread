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
books = []


async def pages(links):
    # for i in links:
    response = requests.get(url+links, params=params, headers=headers)
    page = html.fromstring(response.text)
    name = page.xpath('//h1[@itemprop="name"]/text()')[0].replace('\n', '')
    prices = page.xpath('//span[@class="app-price product-sidebar-price__price"]/text()')[0].replace('\n', '').split()
    price = int(prices[0])
    currency = prices[1]
    book = {'name': name, 'price': price, 'currency': currency}
    books.append({'name': name, 'price': price, 'currency': currency})
    if len([i for i in base.find(book)]) == 0:
        base.insert_one(book)
    print(name)

async def pages1(links):
    # for i in links:
    response = requests.get(url+links, params=params, headers=headers)
    page = html.fromstring(response.text)
    name = page.xpath('//h1[@itemprop="name"]/text()')[0].replace('\n', '')
    prices = page.xpath('//span[@class="app-price product-sidebar-price__price"]/text()')[0].replace('\n', '').split()
    price = int(prices[0])
    currency = prices[1]
    book = {'name': name, 'price': price, 'currency': currency}
    # books.append({'name': name, 'price': price, 'currency': currency})
    if len([i for i in base.find(book)]) == 0:
        base.insert_one(book)
    print(name+'------')

async def main(x):

    global task
    while True:
        response = requests.get(f'{url}/search/page-{x}', params=params, headers=headers)
        print(response.url)
        if response.status_code == 200:

            dom = html.fromstring(response.text)
            links = dom.xpath('//div[@class="product-list__item"]//a[@class="product-card__image-link smartLink"]/@href')
            x += 1
            for i in range(0, len(links), 1):
                task = loop.create_task(pages(links[i]))
                task = asyncio.get_running_loop()
                futury = task.create_future()
                # task1 = loop.create_task(pages1(links[i+1]))
                # task2 = loop.create_task(pages1(links[i+2]))
                await futury

                # await task1
                # await task2
            print(time.time() - time_)

        else:
            break
        print(books)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(1))

# loop.close()






