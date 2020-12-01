from Posting import Posting
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

class QueryProcessor:
    @staticmethod
    def boolean_retrieval(query: {str}, lexicon: {str: int}) -> ([int], {str: {int: Posting}}):
        # get all posting ids associated with tokens in query
        postings_ids = []
        full_entries = {}
        
        
        with open('index_revised.txt') as index:
            for word in query:
                index.seek(lexicon[word])
                
                parsed_posting = index.readline().split()[1:]
                postings = dict()
                id_set = set()
            
                for val in parsed_posting:
                    pair = val.split(',')
                    postings[int(pair[0])] = Posting(int(pair[0]), float(pair[1]))
                    id_set.add(int(pair[0]))

                postings_ids.append(set(id_set))
                full_entries[word] = postings
        
        # merge: intersection of all sets of ids
        res = postings_ids.pop()
        for posting in postings_ids:
            res = res.intersection(posting)

        return res, full_entries


    # use doc ids to get urls 
    @staticmethod
    def get_urls(ids: [int], corpus: [str]) -> [str]:
        res = []
        for doc_id in ids:
            res.append(corpus[int(doc_id)])

        return res


    # uses helper methods above to perform the full search process
    # do the boolean retrieval -> rank urls -> return urls 
    @staticmethod
    def search(query: str, lexicon: {str: int}, corpus: [str]):
        # parse query and stem
        tokenizer = RegexpTokenizer(r'[A-Za-z0-9]+')
        tokens = tokenizer.tokenize(query)
        stemmer = PorterStemmer()
        stemmed_tokens = []
        for token in tokens:
            stemmed = stemmer.stem(token)
            if stemmed in lexicon:
                stemmed_tokens.append(stemmed)
        stemmed_tokens = set(stemmed_tokens)
        ids, partial = QueryProcessor.boolean_retrieval(stemmed_tokens, lexicon)

        # accumulate tf_idf totals for each doc_id
        ids_total_tfidf = [(doc_id, sum(partial[token][doc_id].tf_idf for token in stemmed_tokens)) for doc_id in ids]
        ## rank by descending tf_idf
        ids = [doc_id for doc_id, tf_idf in sorted(ids_total_tfidf, key=lambda id_tfidf: -id_tfidf[1])]
        return QueryProcessor.get_urls(ids, corpus)
