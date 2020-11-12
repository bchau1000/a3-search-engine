import json
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from pathlib import Path
from collections import Counter
from Index import Index, Indexer
from sys import getsizeof
import pickle

# Make sure you have BeautifulSoup and NLTK installed

def main():
    docID = 0
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
                output = tokenizer.tokenize(soup.get_text().lower())

                # get word frequency from the document
                word_freq = Counter(output)

                # Convert word_freq list to indices 
                indices = Indexer.to_indices(docID, word_freq)
                index.add_indices(indices)
                print('Indexed: ', docID)
                
                # Currently limiting the output to only 200 webpages, haven't let the full program run yet
                # if(docID == 200): 
                #     broke = True
                #     break
                docID += 1
        # if broke: break

    with open('index.pickle','wb') as pkl_out:
        print('Pickling index...')
        pickle.dump(index, pkl_out)
    
    print('Finished.')
        


if __name__ == "__main__":           
    main()