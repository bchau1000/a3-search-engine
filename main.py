import pickle
from search import search_index
from pathlib import Path
from Index import Indexer
from nltk.stem import PorterStemmer



def main():
    if not Path('index.pickle').exists():
        inverted_index = Indexer.create_index('DEV')
    else:
        # Unpickle the inverted index here for testing purposes
        print('Unpickling index...')
        inverted_index = pickle.load(open('index.pickle', 'rb'))
        print('Index unpickled')
        
        print('Unpickling url list...')
        url_list = pickle.load(open('urls.pickle', 'rb'))
        print('Url list unpickled')
        
        search_index(inverted_index, url_list)

if __name__ == "__main__":
    main()
