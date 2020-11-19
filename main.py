import pickle
from pathlib import Path
from Index import Indexer
import time
from QueryProcessor import QueryProcessor
import os


def main():
    rootDir = 'DEV'
    if not Path('index.pickle').exists():
        inverted_index = Indexer.create_index(rootDir)
    else:
        # Unpickle the inverted index here for testing purposes
        print('Unpickling index...')
        inverted_index = pickle.load(open('index.pickle', 'rb'))
        print('Index unpickled')   
    
    corpus = [fname for dirName, subdirList, fileList in os.walk(rootDir) for fname in fileList]

    while True:
        query = input('Enter query (-1 to stop):')
        if query == '-1':
            break
        start_time = time.perf_counter()
        results = QueryProcessor.search(query, inverted_index, corpus)
        stop_time = time.perf_counter()
        print(f'found {len(results)} in {stop_time - start_time}s')
        for i in range(5):
            print(results[i])

if __name__ == "__main__":
    main()
