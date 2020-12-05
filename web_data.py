"""
Libraries
"""
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

"""
Loading the text file and removing spaces and \n
"""
with open("web_data.txt", 'r', encoding="utf8") as f:
    web_data = f.read()

"""
Preprocessing the data
"""
colloquialisms = ['wtf', 'lol', 'ah', 'uhh', 'like', 'yea', 'know', 'haha', 'think','na', 'oh', 'get', 'one', 'idk',
                  'would', 'see', 'good', 'guess', 'even', 'mean', 'lmao', 'well', 'go', 'maybe', 'make', 'gon', 'got',
                  'im', 'right', 'want', 'say', 'could', 'dont', 'yes', 'time', 'tho', 'thing', 'look', 'feel', 'still',
                  'better', 'wan', 'bad', 'really', 'need', 'day', 'much', 'mom', 'ok', 'something', 'thats', 'shit',
                  'also', 'never', 'back', 'okay', 'people', 'sure', 'ca', 'yeah', 'said', 'nice', 'take', 'cause',
                  'tell', 'sorry', 'actually', 'trying', 'use', 'way', 'though', 'always', 'today', 'place', 'bc',
                  'thing', 'thought', 'remember', 'probably', 'anything', 'fine', 'dunno', 'sound', 'stuff', 'lot',
                  'basically', 'literally', 'home', 'already', 'fun', 'try', 'saying', 'come', 'http', 'true', 'pretty',
                  'nothing', 'hard', 'least', 'call', 'long', 'dan', 'yet', 'ta', 'night', 'going', 'tomorrow', 'find',
                  'let', 'youre', 'told', 'make', 'made',  'big', 'uh', 'done', 'kinda', 'cool', 'idea', 'last',
                  'mine', 'exactly', 'making', 'keep', 'put', 'used', 'say', 'wow', 'wrong', 'hope', 'else', 'hear',
                  'everything', 'whole', 'one', 'sense', 'looking', 'eat']
# only alphabet
alpha_only = [t for t in word_tokenize(web_data.lower()) if t.isalpha()]
# removing stopwords like pronouns and modal verbs
no_stops = [t for t in alpha_only if t not in stopwords.words('english')]
# remove colloquialisms
no_colloq = [t for t in no_stops if t not in colloquialisms]
# lemmatize
wordnet_lemmatizer = WordNetLemmatizer()
lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_colloq]
#
"""
Counting and other processes
"""
bag_of_words = Counter(lemmatized)
most_common = bag_of_words.most_common(100)
for i in most_common:
    print(f'You guys mentioned {i[0]} {i[1]} times')
