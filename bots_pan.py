import glob
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from sklearn import metrics, naive_bayes
from nltk.corpus import stopwords

"""
expect training_data to be in /data/en/
expect testing_data to be in /data/en_test/
"""

"""
Loading the data   --- these functions are taken from ashraf2019
"""
def iter_docs(author):
    author_attr = author.attrib
    doc_dict = author_attr.copy()
    #    print(doc_dict)
    doc_dict['text'] = [' '.join([doc.text for doc in author.iter('document')])]
    return doc_dict


def create_data_frame(input_folder):
    os.chdir(input_folder)
    all_xml_files = glob.glob("*.xml")
    truth_data = pd.read_csv('truth.txt', sep=':::', names=['author_id', 'author', 'gender'], engine="python")
    temp_list_of_DataFrames = []
    text_Data = pd.DataFrame()
    for file in all_xml_files:
        etree = ET.parse(file)  # create an ElementTree object
        doc_df = pd.DataFrame(iter_docs(etree.getroot()))
        doc_df['author_id'] = file[:-4]
        temp_list_of_DataFrames.append(doc_df)
    text_Data = pd.concat(temp_list_of_DataFrames, axis=0)

    data = text_Data.merge(truth_data, on='author_id')
    return data


# loading training data
training_data = create_data_frame('data/en/')
X, y = training_data['text'], training_data['author']
# loading testing data
testing_data = create_data_frame('../../data/en_test/')
test_X, test_y = testing_data['text'], testing_data['author']


"""
Preprocessing training data
"""
training_corpus = []
for i in range(0, len(X)):  # len(X)
    tweet = re.sub(r'\W', ' ', str(X[i]))  # remove non-w chars
    # tweet = X[i].lower()
    tweet = tweet.lower()
    tweet = re.sub(r'\s+[a-z]\s+', ' ', tweet)  # remove single characters like i and a
    tweet = re.sub(r'^[a-z]\s+', ' ', tweet)  # remove single characters at the beginning like i and a
    tweet = re.sub(r'\s+', ' ', tweet)  # remove the extra spaces created
    training_corpus.append(tweet)

#changing human to 1 and bot to 0
test_human_bot_y = []
for j in range(0, len(y)):
    if y[j] == "human":
        clas = 1
    else:
        clas = 0
    test_human_bot_y.append(clas)
y = test_human_bot_y

"""
Preprocessing testing data
"""
testing_corpus = []
for i in range(0, len(test_X)):  # len(X)
    tweet = re.sub(r'\W', ' ', str(test_X[i]))  # remove non-w chars
    tweet = tweet.lower()
    tweet = re.sub(r'\s+[a-z]\s+', ' ', tweet)  # remove single characters like i and a
    tweet = re.sub(r'^[a-z]\s+', ' ', tweet)  # remove single characters at the beginning like i and a
    tweet = re.sub(r'\s+', ' ', tweet)  # remove the extra spaces created
    testing_corpus.append(tweet)


#changing human to 1 and bot to 0
training_human_bot_y = []
for j in range(0, len(test_y)):
    if test_y[j] == "human":
        human = 1
    else:
        human = 0
    training_human_bot_y.append(human)
new_y = training_human_bot_y


"""
TFIDF vectorizer
"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=2000, min_df=3, max_df=0.6, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(training_corpus).toarray()


"""
splitting the training data to get the accuracy
"""
from sklearn.model_selection import train_test_split
td_tweet_train, td_tweet_test, td_author_train, td_author_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""
--------------------Machine Learning-----------------------------------
"""

"""
Logistic Regression on tfidf
"""
from sklearn.linear_model import LogisticRegression

LR_classifier = LogisticRegression()
LR_classifier.fit(td_tweet_train, td_author_train)
label_pred = LR_classifier.predict(td_tweet_test)
print("Logistic Regression accuracy on training_data:", metrics.accuracy_score(label_pred, td_author_test))


test_tweets = vectorizer.transform(testing_corpus).toarray()
label_pred_2 = LR_classifier.predict(test_tweets)
print("Logistic Regression accuracy on test_data:", metrics.accuracy_score(label_pred_2, new_y))


"""
Naive Bayes on tfidf
"""


NB_classifier = naive_bayes.MultinomialNB()
NB_classifier.fit(td_tweet_train, td_author_train)
label_pred = NB_classifier.predict(td_tweet_test)
print("Naive Bayes accuracy on training_data:", metrics.accuracy_score(label_pred, td_author_test))


test_tweets = vectorizer.transform(testing_corpus).toarray()
label_pred_2 = NB_classifier.predict(test_tweets)
print("Naive Bayes accuracy on test_data:", metrics.accuracy_score(label_pred_2, new_y))

"""
output:
Logistic Regression accuracy on training_data: 0.9648058252427184
Logistic Regression accuracy on test_data: 0.9068181818181819
Naive Bayes accuracy on training_data: 0.8907766990291263
Naive Bayes accuracy on test_data: 0.825
"""
