import json
import os
import math
import pickle
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from pathlib import Path
from collections import defaultdict
from collections import Counter
from Index import Index, Indexer
from sys import getsizeof

# Make sure you have BeautifulSoup and NLTK installed

def create_index():
    docID = 0
    
    # Unpickle idf_dict that we pickled earlier
    print('Loading in IDF...')
    idf_dict = pickle.load(open('idf.pickle', 'rb'))
    
    print('Starting...')

    # THE INDEX
    index = Index()
    
    # Set this to the path where you downloaded the developer JSON files
    rootDir = Path('DEV')
    
    # Traverse the directory tree starting at rootDir
    for dirName, subdirList, fileList in os.walk(rootDir):
        broke = False
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
                
                # get word frequency from the document
                word_freq = Counter(tokens)

                # Convert word_freq list to indices
                # Pass number of tokens in document to calculate tf
                    # Pass as float to avoid integer division
                # Pass idf_dict to calculate tf-idf of each token in the document
                indices = Indexer.to_indices(docID, float(len(tokens)), idf_dict, word_freq)
                index.add_indices(indices)
                print('Indexed: ', docID)
                
                # Currently limiting the output to only 200 webpages, haven't let the full program run yet
                #if(docID == 200): 
                #    broke = True
                #    break
                docID += 1
        #if broke: break

    # Output number of documents for the report
    with open('info.txt', '+a') as info_file:
        info_file.write('Number of documents: ' + str(docID) + '\n')

    # Pickle the inverted_index for future use
    with open('index.pickle','wb') as pkl_out:
        print('Pickling index...')
        pickle.dump(index, pkl_out)
        
    print('Finished.')

# Create a dictionary formatted as token:idf
def calc_idf():
    idf_dict = dict()
    token_freq = defaultdict(int)
    doc_count = 55393.0
    docID = 0
    
    rootDir = Path('DEV')
    
    # Traverse the directory tree starting at rootDir
    for dirName, subdirList, fileList in os.walk(rootDir):
        broke = False
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
                
                # We only need to check if the document has at least 1 occurence of a token, so use a set
                tokens = set(tokenizer.tokenize(soup.get_text().lower()))
                
                # Increment the count of the tokens that occur in the document
                for token in tokens:
                    token_freq[token] += 1
                
                print('Tokenized: ', docID)
                
                docID += 1
    
    # Pickle token frequencies for debugging purposes
    with open('token_freq.pickle','wb') as pkl_out:
        print('Pickling token frequency...')
        pickle.dump(token_freq, pkl_out)
    
    # Create a dictionary in the format -> token:idf
    # Given: N = size of corpus, df = number of documents a given token appears in
    # idf = log(N/df)
    print('Populating idf_dict...')
    for token, freq in token_freq.items():
        idf = math.log(doc_count/(freq))
        idf_dict[token] = idf
    
    # Pickle idf for use in creating an inverted index
    with open('idf.pickle','wb') as pkl_out:
        print('Pickling idf...')
        pickle.dump(idf_dict, pkl_out)

def main():
    calc_idf()
    create_index()
    
    # Unpickle the inverted index here for testing purposes
    print('Unpickling index...')
    inverted_index = pickle.load(open('index.pickle', 'rb'))
    
    # Output the number of unique tokens for the report
    with open('info.txt', '+a') as info_file:
        info_file.write('Number of tokens: ' + str(len(inverted_index)))


if __name__ == "__main__":
    main()