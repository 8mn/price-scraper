from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import Updater

import config

import requests
from requests.api import get
from bs4 import BeautifulSoup

URLS = ['https://www.pcstudio.in/product/adata-xpg-gammix-d30-8gb-8gbx1-ddr4-3200mhz-red/',
        'https://www.amazon.in/gp/product/B085HSGQ1Y',
        'https://www.vedantcomputers.com/adata-xpg-gammix-d30-red-8gb-8gbx1-ddr4-3200mhz?search=AX4U320038G16A-SR30',
        'https://mdcomputers.in/adata-xpg-gammix-d30-8gb-ddr4-3200mhz-red-ax4u320038g16a-sr30.html',
        'https://www.primeabgb.com/online-price-reviews-india/adata-xpg-gammix-d30-series-8gb-8gbx1-ddr4-3200mhz-memory-ax4u320038g16a-sr30/']

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    
}


fetchedItems = {}

def printInfo(title,price,retailer):
    fetchedItems[retailer] ={}
    fetchedItems[retailer]["itemName"] = title
    fetchedItems[retailer]["itemPrice"] = price
    


def getInfo(url):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    if 'pcstudio' in url:
        title = soup.find(class_='product_title entry-title').get_text()
        price = soup.find(class_='price').get_text()
        printInfo(title,price,"pcstudio.in")
    elif 'amazon' in url:
        title = soup.find(id='title').get_text().strip()
        price = soup.find(class_='a-size-medium a-color-price priceBlockBuyingPriceString').get_text().strip()
        printInfo(title,price,"amazon.in")
    elif 'vedantcomputers' in url:
        title = soup.find(class_='title page-title').get_text()
        price = soup.find(class_='product-price').get_text()
        printInfo(title,price,"vedantcomputers.com")
    elif 'mdcomputers' in url:
        title = soup.find(class_='title-product').get_text().strip()
        price = soup.find(class_='price-new').get_text().strip()
        # availability = soup.find(class_='stock').get_text()
        # print(availability)
        printInfo(title,price,"mdcomputers.com")
    elif 'primeabgb' in url:
        title = soup.find(class_='product_title entry-title').get_text()
        price = soup.find(class_='price pewc-main-price').get_text()
        price = price[-6:]
        printInfo(title,price,"primeabgb.com")
        

    
# print(fetchedItems)  
fetchedItemsMsg = ""

def makeFetchItemsMsg():
    print("making fetched messages ...")
    global fetchedItemsMsg
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

# print(fetchedItemsMsg)

updater = Updater(token=config.ACCESS_TOKEN, use_context=True)
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

# 'amazon.in': 
#       {'itemName': 'XPG ADATA GAMMIX D30 DDR4 8GB (1x8GB) 3200MHz U-DIMM Desktop Memory -AX4U320038G16A-SR30', 
#       'itemPrice': '₹\xa04,598.00'}, 

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