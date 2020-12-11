from Posting import Posting
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import nltk
from nltk.corpus import stopwords


class QueryProcessor:
    @staticmethod
    def boolean_retrieval(query: [str], lexicon: {str: int}) -> ([int], {str: {int: Posting}}):
        # get all posting ids associated with tokens in query
        postings_ids = []
        full_entries = {}

        
        with open('index.txt') as index:
            for word in query:
                index.seek(lexicon[word])
                
                # Tokenize the line containing our token/word using split(), skip the first entry with [1:] since we don't need the token/word itself
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
        res = postings_ids[0]
        for posting in postings_ids:
            res = res.intersection(posting)

        # if we have too few results we can compute the intersections on fewer of the tokens
        # we iteratively consider n-1/n, n-2/n... n-(n-1)/n until we have a satisfactory amount of results
        # we consider those with lower document frequencies first as those rarer terms will 
        # typically have more relevance to the query
        postings_ids = sorted(postings_ids, key=lambda x: len(x))
        iteration = 1
        while len(res) < 10 and iteration < len(postings_ids):
            sub_query = postings_ids[0]
            for i in range(1, len(postings_ids) - iteration):
                sub_query = sub_query.intersection(postings_ids[i])
            res = res.union(sub_query)
            iteration += 1
        return res, full_entries


    # use doc ids to get urls 
    @staticmethod
    def get_urls(ids: [int], corpus: [str]) -> [str]:
        res = []
        for doc_id in ids:
            if '#' not in corpus[int(doc_id)]:
                res.append(corpus[int(doc_id)])
        return res

    @staticmethod
    def check_stopwords(stemmed_tokens:{set}) -> [str]:
        stop_words = set(stopwords.words('english'))
        word_count = 0
        
        # Check the set difference between query and stop_words
            # eg. query = {'my', 'name', 'is', 'John'}
                # query - stop_words = {'name', 'John'}
        difference = stemmed_tokens - stop_words
        
        # If there are at least 3 non-stopwords, return only the non-stopwords
        if len(difference) >= 3:
            return difference

        # Otherwise return the full query
        return stemmed_tokens


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
        
        # remove stopd words if we can
        considered_tokens_set = QueryProcessor.check_stopwords(set(stemmed_tokens))
        # remove tokens that are not considered
        i = 0
        while i < len(stemmed_tokens):
            if stemmed_tokens[i] not in considered_tokens_set:
                stemmed_tokens.pop(i)
                i -= 1
            i += 1
        ids, partial = QueryProcessor.boolean_retrieval(stemmed_tokens, lexicon)

        # accumulate tf_idf totals for each doc_id
        ids_total_tfidf = [(doc_id, sum(partial[token][doc_id].tf_idf for token in stemmed_tokens if doc_id in partial[token])) for doc_id in ids]
        ## rank by descending tf_idf
        ids = [doc_id for doc_id, tf_idf in sorted(ids_total_tfidf, key=lambda id_tfidf: -id_tfidf[1])]
        return QueryProcessor.get_urls(ids, corpus)
