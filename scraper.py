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


def printInfo(title,price):
    print(f"Product: {title}")
    print(f"Price: {price}")
    print('########################')
    


def getInfo(url):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    if 'pcstudio' in url:
        title = soup.find(class_='product_title entry-title').get_text()
        price = soup.find(class_='price').get_text()
        print('pcstudio.in')
        printInfo(title,price)
    elif 'amazon' in url:
        title = soup.find(id='title').get_text().strip()
        price = soup.find(class_='a-size-medium a-color-price priceBlockBuyingPriceString').get_text().strip()
        print("amazon.in")
        printInfo(title,price)
    elif 'vedantcomputers' in url:
        title = soup.find(class_='title page-title').get_text()
        price = soup.find(class_='product-price').get_text()
        print("vedantcomputers.com")
        printInfo(title,price)
    elif 'mdcomputers' in url:
        title = soup.find(class_='title-product').get_text().strip()
        price = soup.find(class_='price-new').get_text().strip()
        availability = soup.find(class_='stock').get_text()
        print("mdcomputers.com")
        print(availability)
        printInfo(title,price)
    elif 'primeabgb' in url:
        title = soup.find(class_='product_title entry-title').get_text()
        price = soup.find(class_='price pewc-main-price').get_text()
        price = price[-6:]
        print("primeabgb.com")
        printInfo(title,price)
        

# getInfo('https://www.amazon.in/gp/product/B085HSGQ1Y')

for u in URLS:
    getInfo(u)