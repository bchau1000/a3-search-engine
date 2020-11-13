from collections import defaultdict
from Posting import Posting

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
    def to_indices(docID: int, word_count: float, idf_dict: dict, word_freq: {str: int}) -> {str: {Posting}}:
        res = defaultdict(dict)
        
        for token, count in word_freq.items():
            tf_idf = (count/word_count) * idf_dict.get(token)
            
            res[token][docID] = Posting(docID, tf_idf)

        return res

# Inherits from defaultdict for convenience in adding new entries
# This class is essentially a dict of dicts of id:Postings pairs
# {token: {docID: Posting}}
class Index(defaultdict):
    def __init__(self, _=None, **kwargs):
        super().__init__(dict, **kwargs)

    # add the indices created from Indexer.to_indices() into this index
    def add_indices(self, indices: {str: Posting}) -> None:
        for token, postings in indices.items():
            for docID, posting in postings.items():
                self[token][docID] = posting

    # FOR DEBUGGING PURPOSES
    # overrode __str__ to esaily print/write the index to console/file
    # returns a str representation of the index '{token: {docID: Posting}, ...}'
    def __str__(self):
        res = '{'
        for token, postings in self.items():
            postings_str = '{'
            for docID, posting in postings.items():
                postings_str += f'{docID}: {str(posting)},'
            res += f'\'{token}\': {postings_str},'

        return res + '}'