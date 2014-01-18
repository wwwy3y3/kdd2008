import pandas as pd
from itertools import izip
from collections import Counter
import numpy as np

#test- Features-test & test
#real- Features-merge & test_Features_merge
path= 'data/training/Features-merge.txt'

data= pd.read_table(path, header=None)
q1= data.quantile(q=0.25).tolist()[1:]
q3= data.quantile(q=0.75).tolist()[1:]

#
# iqr
iqr= []
for x,y in izip(q1,q3):
	iqr.append(y-x)

# max, min
maxi= []
mini= []

# max= q3 + 3*iqr
for x,y in izip(q3,iqr):
	maxi.append(x+3*y)

# min= q1 - 3*iqr
for x,y in izip(q1,iqr):
	mini.append(x-3*y)

# ranges
ranges= [ (x,y) for x,y in izip(mini,maxi) ]

# detect ouliers
ouliers= []
for row in data.iterrows():
	for idx,val in enumerate(np.nditer(row)):
		col= val[1]
		if idx > 0: # skip first one
		# if out of range
			minval= ranges[idx-1][0]
			maxval= ranges[idx-1][1]
			# larger than max
			if col>maxval:
				ouliers.append((row[0],idx-1,maxval))
			# smaller than min
			if col<minval:
				ouliers.append((row[0],idx-1,minval))


# overide
counts= Counter()
for item in ouliers:
	row= item[0]
	counts[row] += 1
	col= item[1]
	overide= item[2]
	data[col][row]= overide

print counts.most_common(10)

#write to file
#data.to_csv('test.csv', header= False, index= False)

				

