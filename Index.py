from collections import defaultdict
from Posting import Posting

# Static class which creates the indices to be added to the index
class Indexer:
    # Generates the indices to be added to the index
    # Converts a word frequency dictionary to a dictionary of
    # tokens mapped to a set of Postings
    # token -> {Posting}
    @staticmethod
    def to_indices(docID: int, url: str, word_freq: {str: int}) -> {str: {Posting}}:
        res = defaultdict(set)
        for token, count in word_freq.items():
            res[token].add(Posting(docID, url, count))

        return res

# Inherits from defaultdict for convenience in adding new entries
# This class is essentially a defaultdict of token -> set(Posting)
class Index(defaultdict):
    def __init__(self, **kwargs):
        super().__init__(set, **kwargs)

    # add the indices created from Indexer.to_indices() into this index
    def add_indices(self, indices: {str: Posting}) -> None:
        for token, postings in indices.items():
            for posting in postings:
                self[token].add(posting)

    # FOR DEBUGGING PURPOSES
    # overrode __str__ to esaily print/write the index to console/file
    # NOTICE: URLs are not printed since it just clutters up the already massive index
    # returns a str representation of the index '{token: set(posting), ...}'
    def __str__(self):
        res = '{'
        for token, postings in self.items():
            postings_str = '{'
            for posting in postings:
                postings_str += f'{str(posting)},'
            postings_str += '}'
            res += f'\'{token}\': {postings_str},'

        return res + '}'