# NLP

## nltk

### bag of words

```python
import nltk
import random
from nltk.corpus import movie_reviews

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

# raw data
# print(documents[0])
# print(documents[0][0])  # data, word set: [str]
# print(documents[0][1])  # category: 'neg', 'pos'


all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())
all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
# print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)

classifier.show_most_informative_features(15)
```


---

## scikit

### tf-idf

```python
from pprint import pprint

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

newgroups_train = fetch_20newsgroups(subset='train')
# pprint(list(newgroups_train.target_names))

categories = ['alt.atheism', 'comp.graphics', 'sci.space', 'soc.religion.christian', ]
twenty_train = fetch_20newsgroups(subset='train', categories=categories)

# raw data
# twenty_train.data    # sentence set: [str]
# twenty_train.target  # category set: [int]
# twenty_train.data[0]    # sentence: str
# twenty_train.target[0]  # category: int

count_vector = CountVectorizer()
X_train_counts = count_vector.fit_transform(twenty_train.data)
# print(count_vector.get_feature_names())
# print(count_vector.vocabulary_)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


# rocchio
def rocchio(train, target):
    from sklearn.neighbors import NearestCentroid
    classifier = NearestCentroid().fit(train, target)
    return classifier


# naive bayes
def naive_bayes(train, target):
    from sklearn.naive_bayes import MultinomialNB
    classifier = MultinomialNB().fit(train, target)
    return classifier


# k mean
def k_mean(train, target):
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(10).fit(train, target)
    return classifier


# svm
def svm(train, target):
    from sklearn import svm
    classifier = svm.SVC(kernel='linear').fit(train, target)
    return classifier


# clf = rocchio(X_train_tfidf, twenty_train.target)
# clf = naive_bayes(X_train_tfidf, twenty_train.target)
# clf = k_mean(X_train_tfidf, twenty_train.target)
clf = svm(X_train_tfidf, twenty_train.target)

docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vector.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('{} => {}'.format(doc, twenty_train.target_names[category]))
```
