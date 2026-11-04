import string
import nltk
from nltk.corpus import *

nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# завантаження текстів із колекції Project Gutenberg (nltk.corpus.gutenberg)
# токенізацію тексту (word_tokenize())
file_bible = "bible-kjv.txt"

bible_words = gutenberg.words(file_bible)
clear_bible = []
for w in bible_words:
  if w not in string.punctuation and not w.isdigit():
    clear_bible.append(w)

print(f"\nIn file {file_bible} are {len(clear_bible)} words")

# визначення частоти слів (FreqDist())
freqUniqWords = nltk.FreqDist(clear_bible)
print(f"\nIn file {file_bible} frequency unique are {len(freqUniqWords)} words")

# отримання списку стоп-слів (stopwords.words())
stop_words = set(stopwords.words('english'))
without_stopwords = []
for w in clear_bible:
  if w.lower() not in stop_words:
    without_stopwords.append(w)
print(f"\nStop words are {len(stop_words)} words")
print(stop_words)

# лематизацію (WordNetLemmatizer) або стемінг (PorterStemmer)
ps = nltk.stem.PorterStemmer()
print(f"\n>>>>>  Stemming")
for w in without_stopwords[:15]:
  print(f"Word: {w} Stem: {ps.stem(w)}")

lemmatizer = nltk.stem.WordNetLemmatizer()
print(f"\n>>>>>  Lemmatizer")
for w in without_stopwords[:15]:
  print(f"Word: {w} Lemma: {lemmatizer.lemmatize(w)}")