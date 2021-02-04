import glob
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from sklearn import metrics, naive_bayes, svm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

"""
expect training_data to be in data/en/
"""
train_d_path = "data/en/"
"""
expect testing_data to be in data/en_test/
"""
test_d_path = "../../data/en_test/"
""""""

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
training_div_data, testing_div_data = create_training_data_frame(train_d_path, 'truth-train.txt', 'truth-dev.txt')
print("Training Data size", len(training_div_data))
print("Testing Data size", len(testing_div_data))

"""
Preprocessing training data
"""


def listsToText(l):
    internal = [' '.join(e) for e in l]
    return ' '.join(internal)


def preprocess(data):
    corpus = []
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(data)):  # len(X)
        tweet = re.sub(r'\W', ' ', str(data[i]))  # remove non-w chars
        # tweet = str(data[i])
        tweet = tweet.lower()

        # Extra layers Lorena
        tweet = re.sub(r'https?:\/\/.\S*', 'URL', tweet)  # replace every url for a custom word
        # tweet = re.sub(r'@.\S*', 'MENTION', tweet) # replace every mention for a custom word
        # tweet = re.sub(r'#.\S*', 'HASHTAG', tweet) #replace every hashtag for a custom word
        # tweet = re.sub(r'".*"', 'QUOTE', tweet) #replace every quote for a custom word
        # tweet = re.sub(r'\W', ' ', tweet)  # remove non-w chars

        tweet = re.sub(r'\s+[a-z]\s+', ' ', tweet)  # remove single characters like i and a
        tweet = re.sub(r'^[a-z]\s+', ' ', tweet)  # remove single characters at the beginning like i and a
        tweet = re.sub(r'\s+', ' ', tweet)  # remove our extra spaces

        # lemmatize words
        tweet = word_tokenize(tweet)
        tweet = ' '.join([lemmatizer.lemmatize(w) for w in tweet])

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

# tfidf
# vectorizer = TfidfVectorizer(max_features=2000, min_df=3, max_df=0.6, stop_words=stopwords.words('english'))
# vectorized_training_div_tweets = vectorizer.fit_transform(training_div_corpus).toarray()
# vectorized_testing_div_tweets = vectorizer.transform(testing_div_corpus).toarray()

# 2 gram tfidf
# vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(2, 2), stop_words=stopwords.words('english'))
# vectorized_training_div_tweets = vectorizer.fit_transform(training_div_corpus).toarray()
# vectorized_testing_div_tweets = vectorizer.transform(testing_div_corpus).toarray()

# 3 gram tfidf
# vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(3, 3), stop_words=stopwords.words('english'))
# vectorized_training_div_tweets = vectorizer.fit_transform(training_div_corpus).toarray()
# vectorized_testing_div_tweets = vectorizer.transform(testing_div_corpus).toarray()


# 3 gram tfidf
vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,2), max_features=5000, stop_words=stopwords.words('english'))
vectorized_training_div_tweets = vectorizer.fit_transform(training_div_corpus).toarray()
vectorized_testing_div_tweets = vectorizer.transform(testing_div_corpus).toarray()




"""
MACHINE LEARNING SECTION
"""
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

LR_classifier = LogisticRegression()
LR_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred1 = LR_classifier.predict(vectorized_testing_div_tweets)
print("Logistic Regression accuracy on training_data:", metrics.accuracy_score(label_pred1, testing_div_labels))

NB_classifier = naive_bayes.MultinomialNB()
NB_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred2 = NB_classifier.predict(vectorized_testing_div_tweets)
print("Naive Bayes accuracy on training_data:", metrics.accuracy_score(label_pred2, testing_div_labels))

SVM_classifier = svm.LinearSVC()
SVM_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred3 = SVM_classifier.predict(vectorized_testing_div_tweets)
print("SVM accuracy on training_data:", metrics.accuracy_score(label_pred3, testing_div_labels))

RF_classifier = RandomForestClassifier()
RF_classifier.fit(vectorized_training_div_tweets, training_div_labels)
label_pred4 = RF_classifier.predict(vectorized_testing_div_tweets)
print("RF accuracy on training_data:", metrics.accuracy_score(label_pred4, testing_div_labels))

"""
TEST on pan test data
"""

new_test_data = create_test_data_frame(test_d_path)
test_X, test_y = new_test_data['text'], new_test_data['author']
print("Pan Testing Data size", len(new_test_data))

new_test_corpus = preprocess(test_X)
new_testing_labels = set_labels(test_y)

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_predict = LR_classifier.predict(test_tweets)
print("Logistic Regression accuracy on pan_test_data:", metrics.accuracy_score(label_predict, new_testing_labels))

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_pred_2 = NB_classifier.predict(test_tweets)
print("Naive Bayes accuracy on pan_test_data:", metrics.accuracy_score(label_pred_2, new_testing_labels))

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_pred_3 = SVM_classifier.predict(test_tweets)
print("SVM accuracy on pan_test_data:", metrics.accuracy_score(label_pred_3, new_testing_labels))

test_tweets = vectorizer.transform(new_test_corpus).toarray()
label_pred_4 = RF_classifier.predict(test_tweets)
print("RF accuracy on pan_test_data:", metrics.accuracy_score(label_pred_4, new_testing_labels))
