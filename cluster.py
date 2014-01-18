import pandas as pd
from itertools import izip
from collections import Counter
import numpy as np

#test- Features-test & test
#real- Features-merge & test_Features_merge
path= 'data/mini.csv'

sick= Counter()
allc= Counter()
data= pd.read_csv(path)
for index, row in data.iterrows():
	mali= int(row['mali'])
	pid= int(row['id'])
	if pid<=19500:
		allc['a'] += 1
		if mali >0:
			sick['a'] += 1
	elif pid<= 438000:
		allc['b'] += 1
		if mali >0:
			sick['b'] += 1
	elif pid<= 4330000:
		allc['c'] += 1
		if mali >0:
			sick['c'] += 1
	elif pid<= 6210000:
		allc['d'] += 1
		if mali >0:
			sick['d'] += 1

print sick
print allc
for ch in ['a','b','c','d']:
	print float(sick[ch])/float(allc[ch])