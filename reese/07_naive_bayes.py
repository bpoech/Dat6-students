'''
CLASS: Naive Bayes SMS spam classifier using sklearn
Data source: https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
'''

## READING IN THE DATA

# read tab-separated file using pandas
import pandas as pd
df = pd.read_table('https://raw.githubusercontent.com/justmarkham/DAT4/master/data/sms.tsv',
                   sep='\t', header=None, names=['label', 'msg'])

# examine the data
df.head(30)
df.label.value_counts()
df.msg.describe()

# convert label to a binary variable
df['label'] = df.label.map({'ham':0, 'spam':1})
df.head()

# split into training and testing sets
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.msg, df.label, random_state=1)
X_train.shape
X_test.shape


## COUNTVECTORIZER: 'convert text into a matrix of token counts'
## http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

from sklearn.feature_extraction.text import CountVectorizer

# start with a simple example
train_simple = ['call you tonight',
                'Call me a cab',
                'please call me... PLEASE 44!']

# learn the 'vocabulary' of the training data
vect = CountVectorizer()
vect.fit(train_simple)
vect.get_feature_names()

# transform training data into a 'document-term matrix'
train_simple_dtm = vect.transform(train_simple)
train_simple_dtm
train_simple_dtm.toarray()

# examine the vocabulary and document-term matrix together
pd.DataFrame(train_simple_dtm.toarray(), columns=vect.get_feature_names())

# transform testing data into a document-term matrix (using existing vocabulary)
test_simple = ["please don't call me"]
test_simple_dtm = vect.transform(test_simple)
test_simple_dtm.toarray()
pd.DataFrame(test_simple_dtm.toarray(), columns=vect.get_feature_names())


## REPEAT PATTERN WITH SMS DATA

# instantiate the vectorizer
vect = CountVectorizer()

# learn vocabulary and create document-term matrix in a single step
# fit_transofmr accomplishses both the "fit" and "transform" funciton in one line
train_dtm = vect.fit_transform(X_train)
train_dtm

# transform testing data into a document-term matrix
test_dtm = vect.transform(X_test)
test_dtm

# store feature names and examine them
train_features = vect.get_feature_names()
len(train_features)
train_features[:50]
train_features[-50:]

# convert train_dtm to a regular array
train_arr = train_dtm.toarray()
train_arr


## SIMPLE SUMMARIES OF THE TRAINING DATA

# refresher on numpy
import numpy as np
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
arr[0, 0]
arr[1, 3]
arr[0, 1:3]
arr[:, 0]
np.sum(arr)
np.sum(arr, axis=0)
np.sum(arr, axis=1)

# exercise: calculate the number of tokens in the 0th message in train_arr
train_arr[0,:].sum()
# exercise: count how many times the 0th token appears across ALL messages in train_arr
train_arr[:,0].sum()
# exercise: count how many times EACH token appears across ALL messages in train_arr
np.sum(train_arr, axis = 0)
# exercise: create a DataFrame of tokens with their counts
token_counts = pd.DataFrame({'token' : train_features, 'count' : np.sum(train_arr, axis = 0)})
## MODEL BUILDING WITH NAIVE BAYES
## http://scikit-learn.org/stable/modules/naive_bayes.html

# train a Naive Bayes model using train_dtm
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(train_dtm, y_train)

# make predictions on test data using test_dtm
preds = nb.predict(test_dtm)
preds

# compare predictions to true labels
from sklearn import metrics
print metrics.accuracy_score(y_test, preds)
print metrics.confusion_matrix(y_test, preds)

# predict (poorly calibrated) probabilities and calculate AUC
probs = nb.predict_proba(test_dtm)[:, 1]
probs
print metrics.roc_auc_score(y_test, probs)

# exercise: show the message text for the false positives
X_test[y_test < preds]

# exercise: show the message text for the false negatives
X_test[y_test > preds]

## COMPARE NAIVE BAYES AND LOGISTIC REGRESSION
## USING ALL DATA AND CROSS-VALIDATION

# create a document-term matrix using all data
all_dtm = vect.fit_transform(df.msg)

# instantiate logistic regression
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()

# compare AUC using cross-validation
# note: this is slightly improper cross-validation... can you figure out why?
from sklearn.cross_validation import cross_val_score
cross_val_score(nb, all_dtm, df.label, cv=10, scoring='roc_auc').mean()
cross_val_score(logreg, all_dtm, df.label, cv=10, scoring='roc_auc').mean()


## EXERCISE: CALCULATE THE 'SPAMMINESS' OF EACH TOKEN

# create separate DataFrames for ham and spam
spam_df = pd.DataFrame(df[df.label == 1])
ham_df = pd.DataFrame(df[df.label == 0])

# learn the vocabulary of ALL messages and save it
from textblob import TextBlob, Word
import nltk
import re

tokens = []
for token in df.msg:
    for text_token in nltk.word_tokenize(token):
        tokens.append(text_token)

# create document-term matrix of ham, then convert to a regular array

# create document-term matrix of spam, then convert to a regular array

# count how many times EACH token appears across ALL messages in ham_arr

# count how many times EACH token appears across ALL messages in spam_arr

# create a DataFrame of tokens with their separate ham and spam counts

# add one to ham counts and spam counts so that ratio calculations (below) make more sense

# calculate ratio of spam-to-ham for each token
