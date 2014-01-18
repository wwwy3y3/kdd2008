from sklearn import svm
from sklearn import datasets
import numpy as np
import smote
import pandas as pd
from itertools import izip
import TomekLink as Tomeklink
#test- Features-test & test
#real- Features-merge & test_Features_merge
# after-pr.csv
path= 'data/training/after-pr.csv'
path2= 'data/testing/test_Features_merge.txt'
#f = open(path, 'r')

l = []
data= pd.read_csv(path, header=None)
for row in data.iterrows():
	l.append(row[1].tolist())


unhealthyMatrix= data[data[0] > 0].as_matrix()
healthyMatrix= data[data[0] < 0].as_matrix()
oversample= smote.SMOTE(np.array(unhealthyMatrix), 1000, 5)

# final= healthy + unhealthyMatrix oversampling
final=  np.concatenate((healthyMatrix, oversample), axis=0)

# svm
X= [sub[1:] for sub in final]
Y= []
for sub in final:
	Y.append(sub[0])

# Detect the TomekLinks in the data
tomeklinks = Tomeklink.detectTomekLinks(X,Y)

# Remove the TomekLinks from the data
X,Y = Tomeklink.removeTomekLinks(tomeklinks,X,Y)

clf = svm.SVC()
clf.fit(X, Y)

# predict
test = []
data= pd.read_table(path2, header=None)
for row in data.iterrows():
	test.append(row[1].tolist())

X_test= [sub[1:] for sub in test]
rightAns= []
for sub in test:
	rightAns.append(sub[0])

predict= clf.predict(X_test)
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
tpr= float(tp)/(float(tp)+float(fn))
fpr= float(fp)/(float(fp)+float(tn))
string= 'right= {0}, all= {1}, tp= {2}, fp= {3}, tn= {4}, fn= {5}, tpr= {6}, fpr= {7}'
print string.format(acc, len(rightAns), tp, fp, tn, fn, tpr, fpr)