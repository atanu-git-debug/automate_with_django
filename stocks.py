# from bs4 import BeautifulSoup
# import requests


# def scrape_stock_data(symbol):
#     url = f"https://finance.yahoo.com/quote/{symbol}"
#     headers={
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content,'html.parser')
#     current_price = soup.find('span',class_='price').text
#     print(current_price)
#     previous_close = soup.find('span',title='Previous Close').find_next_sibling('span').text

#     print(previous_close)
#     # if response.status_code == 200:

#     # print(url)

# scrape_stock_data('TMCV.NS')

import yfinance as yf

def get_stock_data(symbol):

    stock = yf.Ticker(symbol)

    current_price = stock.info['currentPrice']
    print(current_price)

    previous_close = stock.info['previousClose']
    print(previous_close)

get_stock_data('AAPL')