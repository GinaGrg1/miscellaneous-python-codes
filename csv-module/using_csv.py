import bz2
import csv
from collections import namedtuple
from datetime import datetime

Column = namedtuple('Column', 'src dest convert')


def parse_timestamp(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')


columns = [
    Column('VendorID', 'vendor_id', int),
    Column('passenger_count', 'num_passengers', int),
    Column('tip_amount', 'tip', float),
    Column('total_amount', 'price', float),
    Column('tpep_dropoff_datetime', 'dropoff_time', parse_timestamp),
    Column('tpep_pickup_datetime', 'pickup_time', parse_timestamp),
    Column('trip_distance', 'distance', float),
]


def iter_records(file_name):
    """
    csv.DictReader converts into an OrderedDict. First row looks like this:
    csv_record = OrderedDict([('VendorID', '2'), ('tpep_pickup_datetime', '2018-10-31 07:10:55'), ('tpep_dropoff_datetime', '2018-11-01 06:43:24'), 
                ('passenger_count', '1'), ('trip_distance', '2.57'), ('RatecodeID', '1'), ('store_and_fwd_flag', 'N'), ('PULocationID', '211'), 
                ('DOLocationID', '48'), ('payment_type', '1'), ('fare_amount', '14.5'), ('extra', '0.5'), ('mta_tax', '0.5'), ('tip_amount', '4.74'),
                ('tolls_amount', '0.0'), ('improvement_surcharge', '0.3'), ('total_amount', '20.54')])

    The columns looks like:
        [Column(src='VendorID', dest='vendor_id', convert=<class 'int'>),
        Column(src='passenger_count', dest='num_passengers', convert=<class 'int'>),
        Column(src='tip_amount', dest='tip', convert=<class 'float'>),
        Column(src='total_amount', dest='price', convert=<class 'float'>),
        Column(src='tpep_dropoff_datetime', dest='dropoff_time', convert=<function parse_timestamp at 0x102759a70>),
        Column(src='tpep_pickup_datetime', dest='pickup_time', convert=<function parse_timestamp at 0x102759a70>),
        Column(src='trip_distance', dest='distance', convert=<class 'float'>)]
    """
    with bz2.open(file_name, 'rt') as fp:
        reader = csv.DictReader(fp) 
        for csv_record in reader:
            record = {}
            for col in columns:
                value = csv_record[col.src]  # value = csv_record['VendorID'] == 2
                record[col.dest] = col.convert(value)  # record['vendor_id'] = int(2)
            yield record


def example():
    from pprint import pprint

    for i, record in enumerate(iter_records('./data/taxi.csv.bz2')):
        if i >= 10:
            break
        pprint(record)


example()
