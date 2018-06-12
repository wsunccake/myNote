# PCA


---

## Example

```python
from sklearn.datasets import load_iris
import numpy as np
from sklearn.decomposition import PCA

iris = load_iris()
print('feature: {}'.format(iris.feature_names))
print('target: {}'.format(iris.target_names))

print(iris.data[0], iris.target[0])
for i in range(len(iris.target)):
    print('Example %d: label %s, features %s' %(i, iris.target[i], iris.data[i]))

test_idx = [0, 50, 100]

# training data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# test data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = PCA(n_components=2)
new_train_data = clf.fit(train_data).transform(train_data)
print(clf.explained_variance_ratio_)
print(clf.explained_variance_)

clf = PCA(n_components=0.9)
new_train_data = clf.fit(train_data).transform(train_data)
print(clf.explained_variance_ratio_)
print(clf.explained_variance_)

clf = PCA(n_components='mle')
new_train_data = clf.fit(train_data).transform(train_data)
print(clf.explained_variance_ratio_)
print(clf.explained_variance_)

# print(train_data)
# print(new_train_data)
```
