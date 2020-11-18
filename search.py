import pickle
from pathlib import Path
from Index import Indexer
from nltk.stem import PorterStemmer

def search_index(inverted_index, url_list):
    # Input query, append to a list as tokens
        # input: machine learning
        # search_tokens = ['machine', 'learning']
    print('Enter a query (-1 to stop searching): ')
    search_tokens = list(map(str, input().split()))
    
    # To convert tokens from the query in stems
    stemmer = PorterStemmer()
    
    # Continue while user doesn't enter -1
    while '-1' not in search_tokens:
        # To store the docIDs that contain our search tokens
        doc_ids = list()
        
        # Grab the docIDs from the inverted_index, store in a list of sets
        for token in search_tokens:
            doc_ids.append(set(inverted_index[stemmer.stem(token).lower()].keys()))
        
        # Use the list of sets to find intersection of docIDs
        doc_intersect = set.intersection(*doc_ids)

        # Use the url_list and docIDs to grab urls and output
        for doc_id in doc_intersect:
            print(url_list[doc_id])
        
        # Ask for input again
        print('Enter a query (-1 to stop searching): ')
        search_tokens = list(map(str, input().split()))
