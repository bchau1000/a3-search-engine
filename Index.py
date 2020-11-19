import os
import pickle
import math
import json
from collections import defaultdict, Counter, OrderedDict
from Posting import Posting
from pathlib import Path
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer


# Static class which creates the indices to be added to the index
class Indexer:

    @staticmethod
    def get_num_docs(rootDir):
        return sum(len(fileList) for _, _, fileList in os.walk(rootDir))

    # Generates the indices to be added to the index
    # Converts a word frequency dictionary to a dictionary of
    # tokens mapped to a dict of Postings
    # {token: {docID: Posting}}
    
    # Given: n = number of times a given token appears in a document, N = number of tokens in a document
        # tf = n/N
    # tf-idf = tf * idf
    @staticmethod
    def to_indices_posting_tf(docID: int, token_tf: {str: int}) -> {str: {Posting}}:
        res = defaultdict(dict)
        
        for token, tf in token_tf.items():
            res[token][docID] = Posting(docID, tf)

        return res

    @staticmethod
    def create_index(rootDir):
        docID = 0

        print('Starting...')

        # THE INDEX
        index = defaultdict(OrderedDict) # Index()
        url_list = list()
        
        # Set this to the path where you downloaded the developer JSON files
        rootDir = Path(rootDir)
        
        stemmer = PorterStemmer()
        # Traverse the directory tree starting at rootDir
        for dirName, subdirList, fileList in os.walk(rootDir):
            # broke = False
            # Grab JSON files
            for fname in fileList:
                # Get the path to the JSON file:
                # e.g. C:\Users\bchau\Desktop\Projects\developer.zip\DEV\aiclub_ics_uci_edu
                getPath = Path(dirName).joinpath(fname)
                
                # Open the JSON file with above path
                with open(getPath) as f:
                    # Load JSON file
                    document = json.load(f)
                    
                    # Grab the HTML content from the JSON file and parse with BeautifulSoup
                    soup = BeautifulSoup(document['content'], 'html.parser')
                    
                    # Tokenize the content, exclude punctuation, alphanumeric only
                    tokenizer = RegexpTokenizer(r'\w+')
                    tokens = tokenizer.tokenize(soup.get_text().lower())
                    
                    # stem tokens and get word frequency from the document
                    word_freq = Counter([stemmer.stem(token) for token in tokens])
                    # get term frequencies 
                    token_tf = defaultdict(float)
                    for t, f in word_freq.items():
                        token_tf[t] = f / len(word_freq)

                    url_list.append(document['url'])
                    
                    # Convert token_tf list to indices
                    # Pass idf_dict to calculate tf-idf of each token in the document
                    indices = Indexer.to_indices_posting_tf(docID, token_tf)
                    # index.add_indices_posting_tf(indices)
                    for token, postings in indices.items():
                        for docID, posting in postings.items():
                            index[token][docID] = posting
                    print('Indexed w/ tf: ', docID)

                    # Currently limiting the output to only 200 webpages, haven't let the full program run yet
                    #if(docID == 200): 
                    #    broke = True
                    #    break
                    docID += 1
            #if broke: break
        
        # multiply each postings tf by idf
        # to convert the tfs  to tf-idf
        print('Converting tf to tf-idf...')
        ndocs = Indexer.get_num_docs(rootDir)
        for token, postings in index.items():
            for docID, posting  in postings.items():
                posting.tf_idf *= math.log(ndocs / len(postings))

        with open('index.pickle', 'wb') as f:
            print("Pickling index...")
            pickle.dump(index, f)
            
        with open('urls.pickle', 'wb') as f:
            print("Pickling urls...")
            pickle.dump(url_list, f)
            
        print('Finished.')

        return index

