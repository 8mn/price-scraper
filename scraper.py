import requests
from requests.api import get
from bs4 import BeautifulSoup

URLS = ['https://www.pcstudio.in/product/adata-xpg-gammix-d30-8gb-8gbx1-ddr4-3200mhz-red/','https://www.amazon.in/gp/product/B085HSGQ1Y']

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
        

# getInfo('https://www.amazon.in/gp/product/B085HSGQ1Y')

for u in URLS:
    getInfo(u)