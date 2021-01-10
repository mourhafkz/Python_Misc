from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

with open("chat.txt", 'r', encoding="utf8") as f:
    text = f.readlines()


def line_split(line):
    last_seen_month = 0
    last_seen_year = 0
    if ' - ' in line:
        date_time, full_message = line.split(' - ', 1)
        date, time = date_time.split(' ', 1)
        day, month, year = date.split('/', 2)
        author, message = full_message.split(': ', 1)
        last_seen_month = month
        last_seen_year = year
        return month, year, message
    else:
        message = line
        return last_seen_month, last_seen_year, message


# Create a list with the relevant information of each line, for each line
extracted_date_text = [line_split(l) for l in text]
colloquialisms = ['wtf', 'lol', 'ah', 'uhh', 'like', 'yea', 'know', 'haha', 'think', 'na', 'oh', 'get', 'one', 'idk',
                  'would', 'see', 'good', 'guess', 'even', 'mean', 'lmao', 'well', 'go', 'maybe', 'make', 'gon', 'got',
                  'im', 'right', 'want', 'say', 'could', 'dont', 'yes', 'time', 'tho', 'thing', 'look', 'feel', 'still',
                  'better', 'wan', 'bad', 'really', 'need', 'day', 'much', 'mom', 'ok', 'something', 'thats', 'shit',
                  'also', 'never', 'back', 'okay', 'people', 'sure', 'ca', 'yeah', 'said', 'nice', 'take', 'cause',
                  'tell', 'sorry', 'actually', 'trying', 'use', 'way', 'though', 'always', 'today', 'place', 'bc',
                  'thing', 'thought', 'remember', 'probably', 'anything', 'fine', 'dunno', 'sound', 'stuff', 'lot',
                  'basically', 'literally', 'home', 'already', 'fun', 'try', 'saying', 'come', 'http', 'true', 'pretty',
                  'nothing', 'hard', 'least', 'call', 'long', 'dan', 'yet', 'ta', 'night', 'going', 'tomorrow', 'find',
                  'let', 'youre', 'told', 'make', 'made', 'big', 'uh', 'done', 'kinda', 'cool', 'idea', 'last',
                  'mine', 'exactly', 'making', 'keep', 'put', 'used', 'say', 'wow', 'wrong', 'hope', 'else', 'hear',
                  'everything', 'whole', 'one', 'sense', 'looking', 'eat', 'ur', 'hi']
# Add list to a dictionary
categorized = {}
for i in range(0, len(extracted_date_text), 1):
    month = extracted_date_text[i][0]
    year = extracted_date_text[i][1]
    # preprocess text
    alpha_only = [t for t in word_tokenize(extracted_date_text[i][2].lower()) if t.isalpha()]
    no_stops = [t for t in alpha_only if t not in stopwords.words('english')]
    no_colloq = [t for t in no_stops if t not in colloquialisms]
    wordnet_lemmatizer = WordNetLemmatizer()
    message = [wordnet_lemmatizer.lemmatize(t) for t in no_colloq]

    if message:
        if (month, year) in categorized:
            categorized[(month, year)] += message
        else:
            categorized[(month, year)] = message

"""
Counting and printing the most common words per month
"""
months = {'01': 'Jan', '02': 'Feb', '03': 'March', '04': 'April',
          '05': 'May', '06': 'June', '07': 'July', '08': 'Aug',
          '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
how_many_words_do_you_want = 5
for date_time_item in categorized:
    bag_of_words = Counter(categorized[date_time_item])
    most_common = bag_of_words.most_common(how_many_words_do_you_want)
    print(f'In {months[date_time_item[0]]} - {date_time_item[1]} the most common words were:')
    for i in most_common:
        print(f' {i[0]}, {i[1]} time(s)')
