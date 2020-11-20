from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from collections import Counter

class Tokenizer:
    @staticmethod
    def tokenize_and_stem(content):
        # Grab the HTML content from the JSON file and parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Tokenize the content, exclude punctuation, alphanumeric only
        tokenizer = RegexpTokenizer(r'[A-Za-z0-9]+')
        tokens = tokenizer.tokenize(soup.get_text().lower())
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]

    @staticmethod
    def get_word_freq(words: [str]):
        return Counter(words)