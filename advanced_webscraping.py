import urllib3
import csv
import datetime as dt

from bs4 import BeautifulSoup

http = urllib3.PoolManager()

US_list_of_indices = ['SPX:IND', 'INDU:IND', 'CCMP:IND', 'NYA:IND', 'SPTSX:IND']
UE_list_of_indices = ['SX5E:IND', 'UKX:IND', 'DAX:IND', 'CAC:IND', 'IBEX:IND']
ASIA_list_of_indices = ['NKY:IND', 'TPX:IND', 'HSI:IND', 'SHSZ300:IND', 'AS51:IND', 'MXAP:IND']


US_urls = ['http://www.bloomberg.com/quote/{}'.format(indices) for indices in US_list_of_indices]


def getIndexPrice(urls):
    data = []
    for url in urls:
        page = http.request('GET', url)
        parse_page = BeautifulSoup(page.data, 'html.parser')

        name_box = parse_page.find('h1', attrs={'class': 'name'})
        text = name_box.text.strip()
        price = parse_page.find('div', attrs={'class': 'price'}).text

        data.append([text, price, dt.datetime.now()])

    return data


if __name__ == '__main__':
    data = getIndexPrice(US_urls)
    with open('index_price_all.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)