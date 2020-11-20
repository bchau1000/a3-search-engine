import pickle
from pathlib import Path
import Index
import time
from QueryProcessor import QueryProcessor


def main():
    rootDir = 'DEV'
    # if the index doesn't exist yet creat it!
    if not Path('index.txt').exists():
        Index.Indexer.create_index(rootDir)

    ##### AUXILIARY STRUCTURES #####

    # lexicon
    if not Path('lexicon.pkl').exists():
        lexicon = Index.load_lexicon()
        with open('lexicon.pkl', 'wb') as f:
            pickle.dump(lexicon, f)
    else:
        with open('lexicon.pkl', 'rb') as f:
            lexicon = pickle.load(f)

    # corpus
    if not Path('corpus.pkl').exists():
        corpus = Index.load_url_lookup(rootDir)
        with open('corpus.pkl', 'wb') as f:
            pickle.dump(corpus, f)
    else:
        with open('corpus.pkl', 'rb') as f:
            corpus = pickle.load(f)
    
    ##### DRIVER #####
    while True:
        query = input('Enter query (-1 to stop):')
        if query == '-1':
            break
        start_time = time.perf_counter()
        results = QueryProcessor.search(query, lexicon, corpus)
        stop_time = time.perf_counter()
        print(f'found {len(results)} in {stop_time - start_time}s')
        for i in range(5):
            print(results[i])

if __name__ == "__main__":
    main()
