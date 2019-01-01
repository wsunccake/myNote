# Bayes

Gaussian Naive Bayes

Multinomial Naive Bayes

Bernoulli Naive Bayes

## Example

In theater

|         | long hair     | short hair  | total |
| ------- | ------------- | ----------- | ----- |
| man     | 2             | 48          | 50    |
| woman   | 25            | 25          | 50    |

`Probability`

P(man) = 50 / (50 + 50)

P(woman) = 50 / (50 + 50)

`Conditional Probability`

P(long|woman) = 25 / 50

P(woman|long) = 25 / (25 + 2)

P(long|man) = 2 / 50

P(man|long) = 2 / (25 + 2)

P(A|B) != P(B|A)

`Joint Probability`

P(woman,short) = 25 / (50 + 50)

= P(woman) * P(short|woman) = 50 / (50 + 50) * 25 / 50

P(A,B) = P(A) * P(B|A)

P(A,B) = P(B,A)

`Marginal Probability`

P(long) = (2 + 25) / (50 + 50)

= P(long,man) + P(long,woman) = 2 / (50 + 50) + 25 / (50 + 50)

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