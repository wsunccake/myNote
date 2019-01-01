# linear regression


`example1`

```python
from sklearn.datasets import load_iris
from sklearn import linear_model
from sklearn.metrics import accuracy_score

import numpy as np


iris = load_iris()
# print('feature: {}'.format(iris.feature_names))
# print('target: {}'.format(iris.target_names))

# print(iris.data[0], iris.target[0])
# for i in range(len(iris.target)):
#     print('Example %d: label %s, features %s' %(i, iris.target[i], iris.data[i]))

test_idx = [0, 50, 100]

# training data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# test data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = linear_model.LinearRegression()
clf.fit(train_data, train_target)
predictions = clf.predict(test_data)

print('### prediction')
print(predictions)

print('### test')
print(test_target)

# print('### accuracy')
# print(accuracy_score(test_target, predictions))

print('### intercept')
print(clf.intercept_)

print('### coefficient')
print(clf.coef_)
```

`example2`

```python
from sklearn.datasets import load_iris
from sklearn import linear_model
from sklearn.metrics import accuracy_score

import numpy as np


iris = load_iris()
# print('feature: {}'.format(iris.feature_names))
# print('target: {}'.format(iris.target_names))
#
# print(iris.data[0], iris.target[0])
# for i in range(len(iris.target)):
#     print('Example %d: label %s, features %s' %(i, iris.target[i], iris.data[i]))

setosa_data = iris.data[0:49]
versicolor_data = iris.data[50:99]
virginica_data = iris.data[99:149]

sepal_lengths = iris.data[:, 0]
sepal_widths = iris.data[:, 1]
petal_lengths = iris.data[:, 2]
petal_widths = iris.data[:, 3]

X = sepal_lengths
y = sepal_widths

test_idx = [0, 50, 100]

# training data
train_target = np.delete(sepal_lengths, test_idx)
train_data = np.delete(sepal_widths, test_idx, axis=0)

# test data
test_target = sepal_lengths[test_idx]
test_data = sepal_widths[test_idx]

clf = linear_model.LinearRegression()
clf.fit(train_data[:, np.newaxis], train_target)
predictions = clf.predict(test_data[:, np.newaxis])

print('### prediction')
print(predictions)

print('### test')
print(test_target)

# print('### accuracy')
# print(accuracy_score(test_target, predictions))

print('### intercept')
print(clf.intercept_)

print('### coefficient')
print(clf.coef_)
```