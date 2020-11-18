import pickle
from pathlib import Path
from Index import Indexer


def main():
    if not Path('index.pickle').exists():
        inverted_index = Indexer.create_index('DEV')
    else:
        # Unpickle the inverted index here for testing purposes
        print('Unpickling index...')
        inverted_index = pickle.load(open('index.pickle', 'rb'))
        print('Index unpickled')   


if __name__ == "__main__":
    main()
