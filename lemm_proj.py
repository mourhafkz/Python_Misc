from nltk import word_tokenize
import enchant

standard_dict = enchant.Dict("en_US")
lemmas_dict = [['not', 'nt', 'nott', 'n0t', 'nawt', 'nottt', 'nto', 'notttt', 'noot', 'nooot', 'not-', 'noooot', 'nottttt', '_not_', 'naht', "n't", 'nnot', 'nooooot', 'notttttt', '-not-', 'noit', '/not/', 'noooooot', 'nottttttt', 'noht'],
               ['been', 'beeen', 'beeeen', 'beenn', 'beeeeen', 'beeeeeen', 'b33n'], 
               ['just', 'jus', 'juss', 'jst', 'juz', 'jsut', 'jux', 'justt', 'jut', 'just', 'jz', 'jusst', 'jusss', 'jss', '#just', 'jusz', 'juat', 'juust', 'jusy', 'juts', 'juuust', 'jusr', 'justed', 'juzt', 'justtt', 'jjust', 'juuuust', 'juhs', 'juzz', 'jzt', 'juxx', 'jusx', 'jussst', 'justs', 'jhuss', 'jussss', 'jhus', 'kust', 'juuuuust', 'jsst', 'juus', 'ju$t', 'jusssst', 'justttt', 'jyst'],
               ["ain't", 'ain', 'anit', 'ain’t', 'iaint', 'aiint', 'aintt', 'ainn', 'ain`t', 'aine', "an't", 'iant', 'ainnt', 'aynt',  'ainy', 'aitn', "a'int", 'ain´t', 'aint', "ain\\'t"],
               ['only', 'onli', 'onlyy', 'ony', 'onlii', '0nly', '-only', 'olny', 'onlyyy', 'onlt', 'onlly', 'onyl', 'onlu', 'onlee', 'onle', 'inly'],
               ['really', 'rly', 'realy', 'rllllly', 'rlly', 'reallly', 'realllly', 'reallyy', 'rele', 'realli', 'relly', 'reallllly', 'reli', 'reali', 'sholl', 'rily', 'reallyyy', 'reeeeally', 'realllllly', 'reaally', 'reeeally', 'rili', 'reaaally', 'reaaaally', 'reallyyyy', 'rilly', 'reallllllly', 'reeeeeally', 'reeally', 'realllyyy', 'reely', 'relle', 'reaaaaally', 'really2', 'reallyyyyy', '_really_', 'realllllllly', 'reaaly', 'realllyy', 'reallii', 'reallt', 'relli', 'realllyyyy', 'reeeeeeally', 'weally', 'reaaallly', 'reallllyyy']]

def TweetLemmatizer(word):
    if not standard_dict.check(word):
        for index, row in enumerate(lemmas_dict):
            for j_index, col in enumerate(row):
                if col == word:
                    return row[0]
        return word
    else:
        return word


tweet_input = "I rllllly aint home"
alpha_only = [t for t in word_tokenize(tweet_input.lower()) if t.isalpha()]
lemmatized = [TweetLemmatizer(i) for i in alpha_only]
print(lemmatized)
# output : ['i', 'really', "ain't", 'home']

"""
Ways to improve this:
1- handcraft a lemmas dictionary similar to the yesterday's link or wordnet
2- maybe sort and binary search to minimize search iterations
"""
