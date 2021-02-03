import glob
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from sklearn import metrics, naive_bayes
from sklearn.feature_extraction.text import TfidfVectorizer
import ktrain
import numpy as np
import tensorflow as tf
from ktrain import text

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

(x_train, y_train), (x_test, y_test), preproc = text.texts_from_array(list(training_div_data['text']),list(training_div_data['author']),list(testing_div_data['text']),list(testing_div_data['author']),
                                                                      max_features=500,preprocess_mode='bert')

model = text.text_classifier(name='bert', train_data=(x_train, y_train), preproc=preproc)

learner = ktrain.get_learner(model=model, train_data=(x_train, y_train), val_data=(x_test, y_test), batch_size=6)

learner.fit_onecycle(lr=2e-5, epochs=1)
