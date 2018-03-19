import urllib3
import csv
import datetime

from bs4 import BeautifulSoup

quote_page = 'http://www.bloomberg.com/quote/SPX:IND'

http = urllib3.PoolManager()

page = http.request('GET', quote_page)

soup = BeautifulSoup(page.data, 'html.parser')

name_box = soup.find('h1', attrs={'class': 'name'}) # prints <h1 class="name"> S&amp;P 500 Index </h1>

# After getting the tag, we can get the data by getting its text.
text = name_box.text.strip() # prints S&P 500 Index

# getting the index price
price = soup.find('div', attrs={'class': 'price'}).text

# Import data to a csv
with open('index_price.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([text, price, datetime.datetime.now().strftime("%Y-%m-%d")
])
