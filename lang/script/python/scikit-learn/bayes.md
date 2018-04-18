# Bayes

Gaussian Naive Bayes

Multinomial Naive Bayes

Bernoulli Naive Bayes

---

## GaussianNB

```python
from sklearn.datasets import load_iris
import numpy as np
from sklearn.naive_bayes import GaussianNB

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

clf = GaussianNB()
clf.fit(train_data, train_target)

print(test_target)
print(clf.predict(test_data))
```

## MultinomialNB

```python
from sklearn.datasets import load_iris
import numpy as np
from sklearn.naive_bayes import MultinomialNB

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

clf = MultinomialNB()
clf.fit(train_data, train_target)

print(test_target)
print(clf.predict(test_data))
```

---

## Reference
[Naive Bayes](http://scikit-learn.org/stable/modules/naive_bayes.html)