# KNN

K-Nearest-Neighbors (KNN)

Artificial Neural Networks (ANN)

Support Vector Machines (SVM)

KNN is non-parametric, instance-based and used in a supervised learning setting.

How to select k?

=> What if k is an even number?

=> What if k equals 1?
Overfitting

=> What if k equals the number of the training instances?
Underfitting training data



---

## Example

```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# https://en.wikipedia.org/wiki/Iris_flower_data_set
iris = datasets.load_iris()

print(iris.feature_names, iris.target_names)
print(iris.data[0], iris.target[0])
for i in range(len(iris.target)):
    print('Example %d: label %s, features %s' %(i, iris.target[i], iris.data[i]))

x = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.5)

# default n_neighbors=5
clf = KNeighborsClassifier(n_neighbors=1)
clf.fit(x_train, y_train)
predictions = clf.predict(x_test)

print('### prediction')
print(predictions)

print('### test')
print(y_test)

print('### accuracy')
print(accuracy_score(y_test, predictions))
```

---

## Customized Classifier

```python
import random
from scipy.spatial import distance
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


def euc(a, b):
    return distance.euclidean(a, b)


class ScrappyKNN():
    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def predict(self, x_test):
        predictions = []

        for row in x_test:
        # random value
        #     label = random.choice(self.y_train)

        # closest distance
            label = self.closest(row)
            predictions.append(label)

        return np.array(predictions)

    def closest(self, row):
        best_dist = euc(row, self.x_train[0])
        best_index = 0
        for i in range(1, len(self.x_train)):
            dist = euc(row, self.x_train[i])
            if dist < best_dist:
                best_dist = dist
                best_index = i
        return self.y_train[best_index]


iris = datasets.load_iris()

x = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.5)

clf = ScrappyKNN()
print(clf.fit(x_train, y_train))
predictions = clf.predict(x_test)

print('### prediction')
print(predictions)

print('### test')
print(y_test)

print('### accuracy')
print(accuracy_score(y_test, predictions))
```


---

## Reference

[A Complete Guide to K-Nearest-Neighbors with Applications in Python and R](https://kevinzakka.github.io/2016/07/13/k-nearest-neighbor/)

[Nearest Neighbors](http://scikit-learn.org/stable/modules/neighbors.html)