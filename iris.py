from sklearn import datasets,tree
import numpy as np
import smote

iris = datasets.load_iris()

print smote.SMOTE(np.array(iris.data), 10, 5).shape