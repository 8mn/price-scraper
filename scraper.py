from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import Updater
# import config
import requests
from requests.api import get
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import os


load_dotenv()

# access_token = os.environ.get('ACCESS_TOKEN')


URLS = ['https://www.pcstudio.in/product/adata-xpg-gammix-d30-8gb-8gbx1-ddr4-3200mhz-red/',
        'https://www.vedantcomputers.com/adata-xpg-gammix-d30-8gb-8gbx1-ddr4-3000mhz-memory-ax4u3000w8g16a-sr30?search=ram',
        'https://mdcomputers.in/adata-xpg-gammix-d30-8gb-ddr4-3200mhz-red-ax4u320038g16a-sr30.html',
        'https://www.primeabgb.com/online-price-reviews-india/adata-xpg-gammix-d30-series-8gb-8gbx1-ddr4-3200mhz-ram-ax4u32008g16a-sr30/']

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'

           }


fetchedItems = {}


def printInfo(title, price, retailer, link):
    fetchedItems[retailer] = {}
    fetchedItems[retailer]["Name"] = title
    fetchedItems[retailer]["Price"] = price
    fetchedItems[retailer]["Buy here"] = link


def getInfo(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        if 'pcstudio' in url:
            title = soup.find(
                class_='product_title entry-title elementor-heading-title elementor-size-default').get_text()
            price = soup.find(
                class_='woocommerce-Price-amount amount').get_text()
            printInfo(title, price, "PC studio", url)
        elif 'vedantcomputers' in url:
            title = soup.find(class_='title page-title').get_text()
            price = soup.find(class_='product-price').get_text()
            printInfo(title, price, "Vedant Computers", url)
        elif 'mdcomputers' in url:
            title = soup.find(class_='title-product').get_text().strip()
            price = soup.find(class_='price-new').get_text().strip()
            # availability = soup.find(class_='stock').get_text()
            # print(availability)
            printInfo(title, price, "MD computers", url)
        elif 'primeabgb' in url:
            title = soup.find(class_='product_title entry-title').get_text()
            price = soup.find(class_='price pewc-main-price').get_text()
            price = price[-6:]
            printInfo(title, price, "Primeabgb", url)
    except AttributeError:
        print(f"Error could not scrape price!")


# print(fetchedItems)
fetchedItemsMsg = ""


def makeFetchItemsMsg():
    print("making fetched messages ...")
    global fetchedItemsMsg
    fetchedItemsMsg += "Here are the updated prices for the RAM\n"
    for i in fetchedItems:
        fetchedItemsMsg += "---------------------------------\n"
        fetchedItemsMsg += f"{i}\n"
        for j, k in fetchedItems[i].items():
            fetchedItemsMsg += f"{j} : {k}\n"
    print("message sent successfully...")


def scrapeItems():
    print("start scraping...")
    for u in URLS:
        getInfo(u)
    print("price scraped successfully...")
    makeFetchItemsMsg()
    print(fetchedItemsMsg)


token = os.getenv('ACCESS_TOKEN_NEW')

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def fetch(update, context):
    scrapeItems()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=fetchedItemsMsg)


start_handler = CommandHandler('fetch', fetch)
dispatcher.add_handler(start_handler)
updater.start_polling()
print("listening for command..")





# json =
# {'pcstudio.in':
#       {'itemName': 'Adata XPG Gammix D30 8GB (8GBX1) DDR4 3200MHz Red        (AX4U320038G16A-SR30)',
#       'itemPrice': '₹4,800.00'},

# 'vedantcomputers.com':
#       {'itemName': 'ADATA XPG GAMMIX D30 RED 8GB (8GBX1) DDR4 3200MHz',
#       'itemPrice': '₹4,300'}, '

# mdcomputers.com':
#       {'itemName':
# 'Adata XPG Gammix D30 8GB (8GBX1) DDR4 3200MHz Red',
#       'itemPrice': '₹3,200'},

# 'primeabgb.com':
#       {'itemName': 'ADATA XPG Gammix D30 Series 8GB (8GBX1) DDR4 3200MHz Memory AX4U320038G16A-SR30',
#       'itemPrice': '₹4,050'}
# }
