# PLA

Perceptron Learning Algorithm (PLA)

[Standard Score](https://en.wikipedia.org/wiki/Standard_score)

mean = sum(Xi)

standard deviation = variance ^ 2

variance = sum(Xi - X) / N


---

## Example

```python
from sklearn import preprocessing
import numpy as np

x = np.array([[0, 0],
              [1, 1],
              [-1, 2]])

ss = preprocessing.StandardScaler().fit(x)

print('x array:')
print(x)

print('mean:')
print(ss.mean_)

print('variance:')
print(ss.var_)

print('standard x:')
print(ss.transform(x))
```

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

import numpy as np

iris = load_iris()
print('feature: {}'.format(iris.feature_names))
print('target: {}'.format(iris.target_names))

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

ss = StandardScaler()
ss.fit(train_data)
ss_x_train = ss.transform(train_data)
ss_x_test = ss.transform(test_data)

clf = Perceptron(n_iter=100, eta0=0.01, shuffle=True)
clf.fit(ss_x_train, train_target)
# clf.fit(train_data, train_target)

predictions = clf.predict(ss_x_test)
# predictions = clf.predict(test_data)

print('### prediction')
print(predictions)

print('### test')
print(test_target)

print('### accuracy')
print(accuracy_score(test_target, predictions))
```