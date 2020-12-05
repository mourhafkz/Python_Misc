
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from collections import defaultdict
import itertools
# the articles are already tokenized, lower(), no_stopwords, isalpha()
docs = [['tom', 'clancy', 'rainbow', 'six', 'siege', 'online', 'tactical', 'shooter', 'video', 'game', 'developed', 'ubisoft', 'montreal', 'published', 'ubisoft', 'released', 'worldwide', 'microsoft', 'windows', 'playstation', 'xbox', 'one', 'december', 'game', 'also', 'set', 'released', 'playstation', 'xbox', 'series', 'game', 'puts', 'heavy', 'emphasis', 'environmental', 'destruction', 'cooperation', 'players', 'player', 'assumes', 'control', 'attacker', 'defender', 'different', 'gameplay', 'modes', 'rescuing', 'hostage', 'defusing', 'bomb', 'taking', 'control', 'objective', 'within', 'room', 'title', 'campaign', 'features', 'series', 'short', 'offline', 'missions', 'called', 'situations', 'played', 'solo', 'missions', 'loose', 'narrative', 'focusing', 'recruits', 'going', 'training', 'prepare', 'future', 'encounters', 'white', 'masks', 'terrorist', 'group', 'threatens', 'safety', 'world'],
        ['rogue', 'company', 'multiplayer', 'tactical', 'shooter', 'video', 'game', 'developed', 'first', 'watch', 'games', 'published', 'studios', 'game', 'released', 'open', 'beta', 'october', 'microsoft', 'windows', 'via', 'epic', 'games', 'store', 'xbox', 'one', 'playstation', 'nintendo', 'switch', 'also', 'released', 'xbox', 'series', 'november', 'including', 'full', 'support', 'play', 'closed', 'beta', 'released', 'july', 'via', 'either', 'streamer', 'drop', 'system', 'buyable', 'founders', 'pack'],
        ['playerunknown', 'battlegrounds', 'pubg', 'online', 'multiplayer', 'battle', 'royale', 'game', 'developed', 'published', 'pubg', 'corporation', 'subsidiary', 'south', 'korean', 'video', 'game', 'company', 'bluehole', 'game', 'based', 'previous', 'mods', 'created', 'brendan', 'playerunknown', 'greene', 'games', 'inspired', 'japanese', 'film', 'battle', 'royale', 'expanded', 'standalone', 'game', 'greene', 'creative', 'direction', 'game', 'one', 'hundred', 'players', 'parachute', 'onto', 'island', 'scavenge', 'weapons', 'equipment', 'kill', 'others', 'avoiding', 'getting', 'killed', 'available', 'safe', 'area', 'game', 'map', 'decreases', 'size', 'time', 'directing', 'surviving', 'players', 'tighter', 'areas', 'force', 'encounters', 'last', 'player', 'team', 'standing', 'wins', 'round']]

# Create a Dictionary from the wiki articles
dictionary = Dictionary(docs)
# Create a corpus from a bag of words
corpus = [dictionary.doc2bow(doc) for doc in docs]
# Create a defaultdict
total_word_count = defaultdict(int)
# populate the empty defaultdict with word count from the whole corpus
for word_id, word_count in itertools.chain.from_iterable(corpus):
        total_word_count[word_id] += word_count
# instantiate a tfidf model
tfidf = TfidfModel(corpus)
# weigh a certain document against the corpus
# 0 represents the first article from the list docs or in this case rainbow six siege
tfidf_weights = tfidf[corpus][0] # change 0 to 1(rogue company) or 2(pubg)
# Sort the unique words of rainbow six when wighted against the whole docs from highest to lowest
sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
# Print the top 20 unique words to rainbow six
for term_id, weight in sorted_tfidf_weights[:20]:
    print(dictionary.get(term_id), weight)

"""
the same method applies to convs by dividing them into periods
"""
