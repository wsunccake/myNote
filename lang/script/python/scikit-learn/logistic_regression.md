# Logistic Regression

```python
from sklearn.datasets import load_iris
import numpy as np
from sklearn import linear_model
from sklearn.metrics import accuracy_score

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

clf = linear_model.LogisticRegression(C=1e5)
clf.fit(train_data, train_target)
predictions = clf.predict(test_data)

print('### prediction')
print(predictions)

print('### test')
print(test_target)

print('### accuracy')
print(accuracy_score(test_target, predictions))

print('### intercept')
print(clf.intercept_)

print('### coefficient')
print(clf.coef_)
```