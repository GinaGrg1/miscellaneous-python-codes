import bz2
import xml.etree.ElementTree as xml

import pandas as pd

# Data conversions
conversion = [
    ('vendor', int),
    ('people', int),
    ('tip', float),
    ('price', float),
    ('pickup', pd.to_datetime),
    ('dropoff', pd.to_datetime),
    ('distance', float),
]


def iter_rides(file_name):
    with bz2.open(file_name, 'rt') as fp:
        tree = xml.parse(fp)
    
    rides = tree.getroot()
    for elem in rides:
        record = {}
        for tag, func in conversion:   # [('vendor', int), ('people', int), ..., ('distance', float)]
            text = elem.find(tag).text # text = elem.find('vendor').text == 2
            record[tag] = func(text)   # record['vendor'] = int(2)
        yield record


def load_xml(file_name):
    records = iter_rides(file_name)
    return pd.DataFrame.from_records(records)


# Example
if __name__ == '__main__':
    df = load_xml('./data/taxi.xml.bz2')
    print(df.dtypes)
    print(df.head())
