import os
import pickle
import math
import json
from collections import defaultdict, Counter
from Posting import Posting
from pathlib import Path
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from sys import getsizeof
from Tokenizer import Tokenizer


# Static class which creates the indices to be added to the index
class Indexer:

    # Generates the indices to be added to the index
    # Converts a word frequency dictionary to a dictionary of
    # tokens mapped to a dict of Postings
    # {token: {docID: Posting}}
    
    # Given: n = number of times a given token appears in a document, N = number of tokens in a document
        # tf = n/N
    # tf-idf = tf * idf
    @staticmethod
    def tokentf_to_postingtf(docID: int, token_tf: {str: int}) -> {str: {Posting}}:
        res = defaultdict(dict)
        
        for token, tf in token_tf.items():
            res[token][docID] = Posting(docID, tf)

        return res
    
    @staticmethod
    def word_freq_to_tokentf(word_freq):
        token_tf = defaultdict()
        for t, f in word_freq.items():
            token_tf[t] = f / len(word_freq)
        return token_tf

    @staticmethod
    def write_partial_to_disk(partial, partial_num):
        print(f'writing partial index {partial_num} to file ')
        filename = f'{partial_num}.txt'
        with open(filename, 'w') as out: 
            for token, postings in sorted(partial.items(), key=lambda x: x[0]):
                out.write(f'{token} {postings}\n')
        return filename

    @staticmethod
    def get_index_size(index) -> int:
        size = 0
        for token, postings in index.items():
            size += getsizeof(postings)
            for docid, posting in postings.items():
                size += getsizeof(docid)
                size += getsizeof(posting)
        return size


    # performs a multi-way merge on the created index partials
    # and converts the tfs into tf-idf in the Posting object
    @staticmethod
    def merge_partials(partials: [str], ndocs: [int]) -> None:
        # open files
        partial_files = []
        for filename in partials:
            partial_files.append(open(filename))

        # create list if (index, token, entry) tuples
        unfinished_files = set()
        ites = []
        for i,file in enumerate(partial_files):
            line = file.readline().strip()
            token, postings = line.split(maxsplit=1)
            postings = eval(postings)
            ites.append([i, token, {token: postings}])
            unfinished_files.add(i)  

        out = open('index.txt', 'w')
        out2 = open('index_revised.txt', 'w')
        nfinished = 0
        while len(unfinished_files) > 0:
            # merge into the least lexic token
            sorted_ites = sorted(ites, key=lambda x: x[1])
            least_i, least_token, least_entry = sorted_ites[0 + nfinished]
            merged_dict = {}
            for file_num in unfinished_files.copy():
                i, token, entry = ites[file_num]
                if token in least_entry:
                    for _, postings in entry.items():
                        for docid, posting in postings.items():
                            merged_dict[docid] = posting
                    line = partial_files[i].readline().strip()
                    if len(line) == 0:
                        unfinished_files.remove(i)
                        nfinished += 1
                    else:
                        token, postings = line.split(maxsplit=1)
                        postings = eval(postings)
                        ites[i] = [i, token, {token: postings}]
            if len(merged_dict) == 0:
                merged_dict = least_entry[least_token]
                line = partial_files[i].readline().strip()
                if len(line) == 0:
                    unfinished_files.remove(least_i)
                    nfinished += 1
                else:
                    token, postings = line.split(maxsplit=1)
                    postings = eval(postings)
                    ites[i] = [i, token, {token: postings}]
            
            for _, posting in merged_dict.items():
                posting.tf_idf *= math.log(ndocs / len(merged_dict))
            
            out.write(f'{least_token} {merged_dict}\n')
            out2.write(f'{least_token} ')
            for docId, posting in merged_dict.items():
                out2.write(f'{posting.docid},{posting.tf_idf} ')
            out2.write('\n')
            print('token merged:', least_token)
        # cleanup
        for file in partial_files:
            file.close()
        out.close()
        out2.close()

        
    @staticmethod
    def create_index(rootDir):
        MB_100 = 100000000
        docID = 0
        partials = []

        print('Starting...')

        # Set this to the path where you downloaded the developer JSON files
        rootDir = Path(rootDir)
        
        # partial index
        index = defaultdict(dict) 
        partial_num = 0
        curr_size = getsizeof(index)
        # Traverse the directory tree starting at rootDir
        for dirName, subdirList, fileList in os.walk(rootDir):
            # Grab JSON files
            for fname in fileList:
                # Get the path to the JSON file:
                # e.g. C:\Users\bchau\Desktop\Projects\developer.zip\DEV\aiclub_ics_uci_edu
                path = Path(dirName).joinpath(fname)
                
                # Open the JSON file with above path
                with open(path) as f:
                    # Load JSON file
                    document = json.load(f)
                    
                    stems = Tokenizer.tokenize_and_stem(document['content'])
                    
                    # stem tokens and get word frequency from the document
                    word_freq = Tokenizer.get_word_freq(stems)

                    # get term frequencies 
                    token_tf = Indexer.word_freq_to_tokentf(word_freq)

                    # Convert token_tf list to indices
                    entries = Indexer.tokentf_to_postingtf(docID, token_tf)
                    # add to index and increment size counter appropriately
                    for token, postings in entries.items():
                        for docID, posting in postings.items():
                            if token not in index:
                                curr_size += getsizeof({})
                            index[token][docID] = posting
                            curr_size += getsizeof(docID)
                            curr_size += getsizeof(posting)
                            
                    print('Indexed w/ tf: ', docID)

                    # if index grows larger than 100 MB write it to disk
                    if curr_size > MB_100:
                        # append the name of the file that we wrote to to a list
                        partials.append(Indexer.write_partial_to_disk(index, partial_num))
                        partial_num += 1
                        index.clear()
                        curr_size = getsizeof(index)

                    docID += 1

        Indexer.merge_partials(partials, get_num_docs(rootDir))
        
        for filename in partials:
            filePath = Path(filename)
            if filePath.exists():
                os.remove(filePath)

        print('Finished.')

def get_num_docs(rootDir):
    return sum(len(fileList) for _, _, fileList in os.walk(rootDir))

def load_lexicon():
    lexicon = {}
    with open('index.txt') as f:
        pos = 0
        for line in f:
            token = line.split(maxsplit=1)[0]
            lexicon[token] = pos
            pos += len(line) + 1 if os.name != 'posix' else 0
    return lexicon

def load_url_lookup(rootDir):
    lookup = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            path = Path(dirName).joinpath(fname)
            with open(path) as f:
                document = json.load(f)
                lookup.append(document['url'])
    return lookup