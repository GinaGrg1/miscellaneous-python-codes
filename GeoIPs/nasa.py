"""Add geo information to IPs
This code opens the NASA log file, looks for the IP address and match that with the geoip+country name
which comes from the GeoLite2Country.csv file.
GeoLite2Country is available on http://localhost:8988/geoip

Run geoip.py and start the server and then run this file.
"""
import gzip
from ipaddress import IPv4Address
from functools import lru_cache

import requests

headers = {
    'X-GEOIP-TOKEN': 'l3tm3in',
}
base_url = 'http://localhost:8988/geoip'  # 


@lru_cache(1024)   # no of calls to save. When the no of unique calls exceed 1024, LRU cache will remove the least recently used calls.
def country_of(ip):   # country_of('133.43.96.45')
    params = {
        'ip': ip,
    }
    resp = requests.get(base_url, params=params, headers=headers)
    if not resp.ok:
        return ''
    reply = resp.json()
    if not reply['found']:
        return ''

    return reply['name']


def is_ip(host):
    try:
        IPv4Address(host)
        return True
    except ValueError:
        return False


def iter_ips(file_name, limit):
    count = 0
    for line in gzip.open(file_name, 'rt'):  # line = '133.43.96.45 - - [01/Aug/1995:00:00:16 -0400] "GET /shuttle/missions/sts-69/mission-sts-69.html HTTP/1.0" 200 10566'
        if count >= limit:
            break
        i = line.find('-')
        if i == -1:  # not found
            continue
        host = line[:i].strip()  # host = '133.43.96.45'
        if not is_ip(host):      # is_ip(host) --> True
            continue
        yield host
        count += 1


if __name__ == '__main__':
    from collections import Counter

    countries = Counter()
    ips = iter_ips('NASA_access_log_Aug95.gz', 1000)
    for ip in ips:
        country = country_of(ip)
        if not country:
            country = '<Unknown>'
        countries[country] += 1

    total = sum(countries.values())
    for country, count in countries.most_common(10):
        percent = count / total * 100
        print(f'{country:<20} {percent:.2f}%')
