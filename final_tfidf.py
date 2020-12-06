from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from collections import defaultdict
import itertools

"""
Loading the text file and preprocessing the data
"""
with open("web_data.txt", 'r', encoding="utf8") as f:
    user_input = f.read()

# only alphabet
alpha_only = [t for t in word_tokenize(user_input.lower()) if t.isalpha()]
# lemmatize
wordnet_lemmatizer = WordNetLemmatizer()
preprocessed = [wordnet_lemmatizer.lemmatize(t) for t in alpha_only]

"""
chunk the input into a set number of portions/docs to form a corpus
"""

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


original_len = len(preprocessed)
if original_len <= 5000:
    desired_docs_num = 20
elif original_len >= 50000:
    desired_docs_num = 150
elif original_len >= 500000:
    desired_docs_num = 500
else:
    desired_docs_num = 75

corpus_docs = list(chunk(preprocessed, original_len // desired_docs_num))
number_of_docs = len(corpus_docs)

# Create a Dictionary 
dictionary = Dictionary(corpus_docs)
# Create a corpus from a bag of words
corpus = [dictionary.doc2bow(doc) for doc in corpus_docs]
# Create a defaultdict
total_word_count = defaultdict(int)
# populate the empty defaultdict with word count from the whole corpus
for word_id, word_count in itertools.chain.from_iterable(corpus):
    total_word_count[word_id] += word_count
# instantiate a tfidf model
tfidf = TfidfModel(corpus)
number_of_words_from_every_doc = 1 # you can change this to get more words out of every portion/doc
total_unique_words = {}
for i in range(len(corpus_docs)):
    # weigh a certain document against the corpus
    tfidf_weights = tfidf[corpus][i]
    # Sort the unique words
    sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
    # Print the top unique word in every portion
    for term_id, weight in sorted_tfidf_weights[:number_of_words_from_every_doc]:
        total_unique_words[dictionary.get(term_id)] = weight
"""
final result
"""
unique_words_descending_wights = sorted(total_unique_words.items(), key=lambda w: w[1], reverse=True)
unique_words = [t[0] for t in unique_words_descending_wights]
print(','.join(unique_words[0:50])) #first 50 words
