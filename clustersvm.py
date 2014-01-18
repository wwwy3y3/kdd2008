from sklearn import svm
from sklearn import datasets
import numpy as np
import smote
import pandas as pd
from itertools import izip
import TomekLink as Tomeklink

def printSvm(predict, rightAns):
	acc= 0
	tp= 0
	fp= 0
	tn= 0
	fn= 0
	for ans,right in izip(predict,rightAns):
		if ans == right:
			acc += 1
		if ans > 0 and right > 0:
			tp += 1
		if ans < 0 and right > 0:
			fp += 1
		if ans < 0 and right < 0:
			tn += 1
		if ans > 0 and right < 0:
			fn += 1
	tpr= 0
	fpr= 0
	string= 'right= {0}, all= {1}, tp= {2}, fp= {3}, tn= {4}, fn= {5}, tpr= {6}, fpr= {7}'
	print string.format(acc, len(rightAns), tp, fp, tn, fn, tpr, fpr)

#test- Features-test & test
#real- Features-merge & test_Features_merge
# after-pr.csv
path= 'data/training/after-pr.csv'
path2= 'data/testing/test_Features_merge.txt'
#f = open(path, 'r')

features= {'a': [],'b': [],'c': [],'d': []}
value= {'a': [],'b': [],'c': [],'d': []}
alls= {'a': [],'b': []}
data= pd.read_csv(path, header=None)
for index, row in data.iterrows():
	mali= int(row[1])
	pid= int(row[0])
	if pid<=19500:
		#features['a'].append(row[2:].tolist())
		#value['a'].append(mali)
		alls['a'].append(row[1:].tolist())
	elif pid<= 438000:
		#features['b'].append(row[2:].tolist())
		#value['b'].append(mali)
		alls['b'].append(row[1:].tolist())
	elif pid<= 4330000:
		features['c'].append(row[2:].tolist())
		value['c'].append(mali)
	elif pid<= 6210000:
		features['d'].append(row[2:].tolist())
		value['d'].append(mali)

#smote
for ch in ['a','b']:
	sick= [item for item in alls[ch] if item[0]>0]
	healthy= [item for item in alls[ch] if item[0]<0]
	oversample= smote.SMOTE(np.array(sick), 2000, 5)
	whole= healthy+oversample.tolist()
	features[ch]= [row[1:] for row in whole]
	value[ch]= [row[0] for row in whole]

# svm
clfs= {}
for ch in ['a','b','c','d']:
	clf= svm.SVC()
	clf.fit(features[ch], value[ch])
	clfs[ch]= clf

# predict
test = []
data= pd.read_table(path2, header=None)
for row in data.iterrows():
	test.append(row[1].tolist())

features= {'a': [],'b': [],'c': [],'d': []}
value= {'a': [],'b': [],'c': [],'d': []}
for row in test:
	mali= int(row[1])
	pid= int(row[0])
	if pid<=19500:
		features['a'].append(row[2:])
		value['a'].append(mali)
	elif pid<= 438000:
		features['b'].append(row[2:])
		value['b'].append(mali)
	elif pid<= 4330000:
		features['c'].append(row[2:])
		value['c'].append(mali)
	else:
		features['d'].append(row[2:])
		value['d'].append(mali)

for ch in ['a','b','c','d']:
	if not len(features[ch]) == 0:
		print 'at: '
		print ch
		predict= clfs[ch].predict(features[ch])
		printSvm(predict, value[ch])
	