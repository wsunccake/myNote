# scikit-learn

## Install


```bash
# for linux
centos:~ # yum -y install gcc gcc-c++ python-devel
centos:~ # pip install numpy scipy scikit-learn

# other option
centos:~ # pip install --user --install-option="--prefix=" -U scikit-learn

# for macos
macos:~ # pip install numpy scipy scikit-learn
```

---

## Simple Case

```python
from sklearn import tree

# feature: [weight, skin]
# skin: smooth -> 1, bumpy -> 0
features = [[140, 1], [130, 1], [150, 0], [170, 0]]

# label: apple -> 0, orange -> 1
labels = [0, 0, 1, 1]

# choose algorithm
clf = tree.DecisionTreeClassifier()

# learn
clf = clf.fit(features, labels)

# predict
print(clf.predict([[150, 0], [160, 1]]))
```

---

## Decision Tree Visualization

```bash
centos:~ # yum install graphviz
centos:~ # pip install graphviz
```

```python
from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np

iris = load_iris()
print(iris.feature_names, iris.target_names)
print(iris.data[0], iris.target[0])

# for i in range(len(iris.target)):
#     print('Example %d: label %s, features %s' %(i, iris.target[i], iris.data[i]))

test_idx = [0, 50, 100]

# training data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# test data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)

print(test_target)
print(clf.predict(test_data))

# visualized code
import graphviz

#dot_data = tree.export_graphviz(clf, out_file=None)
dot_data = tree.export_graphviz(clf,
                                out_file=None,
                                feature_names=iris.feature_names,
                                class_names=iris.target_names,
                                filled=True,
                                rounded=True,
                                special_characters=True)  
graph = graphviz.Source(dot_data)
graph.render('iris')

print(test_data[0], test_target[0])
```


---

## Customized Classifier

`original code`

```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()

x = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.5)

my_classifier = KNeighborsClassifier()
my_classifier.fit(x_train, y_train)
predictions = my_classifier.predict(x_test)

print(accuracy_score(y_test, predictions))
```

`modified code`

```python
import random
from scipy.spatial import distance
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def euc(a, b):
    return distance.euclidean(a ,b)

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

        return predictions

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

my_classifier = ScrappyKNN()
my_classifier.fit(x_train, y_train)
predictions = my_classifier.predict(x_test)

print(accuracy_score(y_test, predictions))
```

## Reference

[scikit-learn](http://scikit-learn.org/stable/)

[Graphviz](https://graphviz.gitlab.io/)