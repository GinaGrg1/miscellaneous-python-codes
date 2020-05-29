import json
from datetime import datetime, timedelta


def parse_time(ts):
    """
    parse_time('2018-10-31T07:10:55.000Z') --> datetime.datetime(2018, 10, 31, 7, 10, 55)
    """
    # [:-1] trims Z suffix
    return datetime.fromisoformat(ts[:-1])


def fix_pair(pair):
    key, value = pair   # ('vendor',2), ('pickup', '2018-10-31T07:10:55.000Z'), ('dropoff', '2018-11-01T06:43:24.000Z'), ('distance', 2.57)
    if key not in ('pickup', 'dropoff'):
        return pair     # ('vendor',2), ('distance', 2.57)
    return key, parse_time(value)


def pairs_hook(pairs):
    # pairs = [('vendor', 2), ('pickup', '2018-10-31T07:10:55.000Z'), ('dropoff', '2018-11-01T06:43:24.000Z'), ('distance', 2.57), ('tip', 4.74), ('total', 20.54)]
    return dict(fix_pair(pair) for pair in pairs)


durations = []
with open('./data/taxi.jl') as fp:
    for line in fp:
        obj = json.loads(line, object_pairs_hook=pairs_hook)  # {'vendor': 2, 'pickup': datetime.datetime(2018, 10, 31, 7, 10, 55), 'dropoff': datetime.datetime(2018, 11, 1, 6, 43, 24), 'distance': 2.57, 'tip': 4.74, 'total': 20.54}
        duration = obj['dropoff'] - obj['pickup']
        durations.append(duration)

avg_duration = sum(durations, timedelta()) / len(durations)
print(f'average ride duration: {avg_duration}')


# object_pairs_hook converts the dict into a list of tuples
# {"var1": val1, "var2": val2}  --> [('var1', val1), ('var2', val2)]
