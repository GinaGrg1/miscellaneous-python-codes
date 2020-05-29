import csv
from collections import Counter, defaultdict
from itertools import islice
import random

# Very inefficient way of opening a file.
# Converts into a list of dictionary. Each row is a OrderedDict
food = list(csv.DictReader(open('./data/Food_Inspections.csv')))

result_type = { row['Results'] for row in food }
failed = [row for row in food if row['Results'] == 'Fail']
worst_restaurants = Counter(row['DBA Name'] for row in failed)
top_5_worst_places = worst_restaurants.most_common(5)

# Take the dictionary rows from failed **row and merging new keys into it [ replacing values with the apostrophes in 'DBA Name' with blank]
failed_cleanup = [ { **row, 'DBA Name': row['DBA Name'].replace("'",'').upper()} for row in failed ]
cleaned_worst_restaurants = Counter(row['DBA Name'] for row in failed_cleanup)

worst_location = Counter(row['Address'] for row in failed_cleanup)
top_5_worst_location = worst_location.most_common(5)

# Find the worst place by year
by_year = defaultdict(Counter)
for row in failed_cleanup:
    by_year[row['Inspection Date'][-4:]][row['Address']] += 1

worst_location_2016 = by_year['2016'].most_common(5)
 
# by_year
# defaultdict(<class 'collections.Counter'>, {'2020': Counter({'1334 W DIVISION ST ': 1})})

any_5 = list(islice(by_year['2016'].items()), 5)

# All failed businesses in ohare
ohare = [row for row in failed_cleanup if row['Address'].startswith('11601 W TOUHY')]
failed_businesses_in_ohare = { row['DBA Name']for row in ohare }

which_terminal = Counter(row['AKA Name'] for row in ohare)
which_terminal.most_common(5)

# {row['Address']for row in ohare}
# {'11601 W TOUHY AVE ', '11601 W TOUHY AVE T2 F12'}

inspections = defaultdict(list)
for row in ohare:
    inspections[row['License #']].append(row)

# To see all the license no. --> inspections.keys()

# Randomly choose a license # and fine its Inspection Date
inspection_date = [row['Inspection Date'] for row in inspections[random.choice(list(inspections))]]

# Get the type of violations for the 3rd entry. This is only an example
violations = ohare[2]['Violations'].split('|')
vtypes = [v[:v.find('- Comments:')].strip() for v in violations]  # find() returns the index

all_violations = [ row['Violations'].split('|') for row in ohare ]
v_counter = Counter()
for violations in all_violations:
    for v in violations:
        v_counter[v[:v.find('- Comments')].strip()] += 1

v_counter.most_common(5)
