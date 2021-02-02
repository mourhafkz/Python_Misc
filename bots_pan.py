import glob
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from sklearn import metrics, naive_bayes
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

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
    doc_dict['text'] = [' '.join([doc.text for doc in author.iter('document')])]
    return doc_dict


def create_test_data_frame(input_folder):
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



def create_training_data_frame(input_folder, taining_div, testing_div):
    os.chdir(input_folder)
    all_xml_files = glob.glob("*.xml")
    train_truth_div_data = pd.read_csv(taining_div, sep=':::', names=['author_id', 'author', 'gender'], engine="python")
    test_truth_div_data = pd.read_csv(testing_div, sep=':::', names=['author_id', 'author', 'gender'], engine="python")
    temp_list_of_DataFrames = []
    text_Data = pd.DataFrame()
    for file in all_xml_files:
        etree = ET.parse(file)  # create an ElementTree object
        doc_df = pd.DataFrame(iter_docs(etree.getroot()))
        doc_df['author_id'] = file[:-4]
        temp_list_of_DataFrames.append(doc_df)
    text_Data = pd.concat(temp_list_of_DataFrames, axis=0)
    training_data = text_Data.merge(train_truth_div_data, on='author_id')
    testing_data = text_Data.merge(test_truth_div_data, on='author_id')
    return training_data, testing_data


# loading training data
training_div_data, testing_div_data = create_training_data_frame('data/en/', 'truth-train.txt', 'truth-dev.txt')
print("Training Data size", len(training_div_data))
print("Testing Data size", len(testing_div_data))


"""
Preprocessing training data
"""

def preprocess(data):
    corpus = []
    for i in range(0, len(data)):  # len(X)
        tweet = re.sub(r'\W', ' ', str(data[i]))  # remove non-w chars
        # tweet = X[i].lower()
        tweet = tweet.lower()
        tweet = re.sub(r'\s+[a-z]\s+', ' ', tweet)  # remove single characters like i and a
        tweet = re.sub(r'^[a-z]\s+', ' ', tweet)  # remove single characters at the beginning like i and a
        tweet = re.sub(r'\s+', ' ', tweet)  # remove our extra spaces
        corpus.append(tweet)
    return corpus


def set_labels(data):
    labels = []
    for j in range(0, len(data)):
        if data[j] == "human":
            clas = 1
        else:
            clas = 0
        labels.append(clas)
    return labels


training_div_corpus = preprocess(training_div_data['text'])
training_div_labels = set_labels(training_div_data['author'])

testing_div_corpus = preprocess(testing_div_data['text'])
testing_div_labels = set_labels(testing_div_data['author'])


vectorizer = TfidfVectorizer(max_features=2000, min_df=3, max_df=0.6, stop_words=stopwords.words('english'))
vectorized_training_div_tweets = vectorizer.fit_transform(training_div_corpus).toarray()
vectorized_testing_div_tweets = vectorizer.transform(testing_div_corpus).toarray()

"""
Logistic Regression on tfidf
"""
from sklearn.linear_model import LogisticRegression

LR_classifier = LogisticRegression()
LR_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred1 = LR_classifier.predict(vectorized_testing_div_tweets)
print("Logistic Regression accuracy on training_data:", metrics.accuracy_score(label_pred1, testing_div_labels))

NB_classifier = naive_bayes.MultinomialNB()
NB_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred2 = NB_classifier.predict(vectorized_testing_div_tweets)
print("Naive Bayes accuracy on training_data:", metrics.accuracy_score(label_pred2, testing_div_labels))



"""
TEST on separate data
"""

new_test_data = create_test_data_frame('../../data/en_test/')
test_X, test_y = new_test_data['text'], new_test_data['author']
print("New Testing Data size", len(new_test_data))


new_test_corpus = preprocess(test_X)
new_testing_labels = set_labels(test_y)

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_predict = LR_classifier.predict(test_tweets)
print("Logistic Regression accuracy on new_test_data:", metrics.accuracy_score(label_predict, new_testing_labels))

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_pred_2 = NB_classifier.predict(test_tweets)
print("Naive Bayes accuracy on new_test_data:", metrics.accuracy_score(label_pred_2, new_testing_labels))



"""
Output on my machine:
------------------------------------------------------------------
Training Data size 2880
Testing Data size 1240
Logistic Regression accuracy on training_data: 0.9016129032258065
Naive Bayes accuracy on training_data: 0.7741935483870968
New Testing Data size 2640
Logistic Regression accuracy on new_test_data: 0.9030303030303031
Naive Bayes accuracy on new_test_data: 0.8223484848484849
-------------------------------------------------------------------
"""
