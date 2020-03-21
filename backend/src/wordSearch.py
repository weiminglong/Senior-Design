

import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
#need to install package with command pip install sparse_dot_topn

doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father. So what is up and everyone."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle. Machine learning"

doc_complete = [doc1, doc2, doc3, doc4, doc5]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()



def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

print('All 3-grams in "McDonalds":')
ngrams('McDonalds')

def clean(doc):
    stop_free = ' '.join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join([ch for ch in stop_free if ch not in exclude])
    normalized = ' '.join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized
doc_clean = [clean(doc).split() for doc in doc_complete]

#print(doc_clean)
print()
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics = 3, id2word = dictionary, passes=50)

#print(ldamodel.print_topics(num_topics=3, num_words=6))

#print(ldamodel.print_topics(num_topics=3, num_words=6))

topics = ldamodel.print_topics(num_topics=5)

print(topics)
print(type(topics))
for topic in topics:
    print(topic)
    print('type',type(topic))

