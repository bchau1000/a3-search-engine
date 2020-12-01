from Posting import Posting
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from pathlib import Path
from QueryProcessor import QueryProcessor
import pickle, time, Index

def main():
    lexicon = Index.load_lexicon_revised()
    
    if not Path('lexicon_revised.pkl').exists():
        lexicon = Index.load_lexicon()
        with open('lexicon_revised.pkl', 'wb') as f:
            pickle.dump(lexicon, f)
    else:
        with open('lexicon_revised.pkl', 'rb') as f:
            lexicon = pickle.load(f)
        
        with open('index_revised.txt') as index:
            index.seek(lexicon['mach'])
            posting_list = index.readline().split()[1:]
            
            for val in posting_list:
                pair = val.split(',')
                posting = Posting(val[0], val[1])
                print(pair)
    

main()