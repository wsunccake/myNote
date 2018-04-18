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


---

## Reference

[scikit-learn](http://scikit-learn.org/stable/)

[Graphviz](https://graphviz.gitlab.io/)