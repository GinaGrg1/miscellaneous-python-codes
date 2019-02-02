import os
import pdftables_api


client = pdftables_api.Client('14tn2liiiei7')

for num, file in enumerate(os.listdir()):
	if file.endswith('pdf'):
		client.csv(file, 'fromsas_{}'.format(num))
	else:
		raise("There are no pdf files.")
