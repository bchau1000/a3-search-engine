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
        
        if len(tokens) < 50:
            return []
        
        if len(tokens) or len(soup.find_all()):
            low_info_ratio = float(len(soup.find_all()))/(float(len(tokens)) + float(len(soup.find_all())))
            if(low_info_ratio > 0.7):
                return []
        
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]

    @staticmethod
    def get_word_freq(words: [str]):
        return Counter(words)