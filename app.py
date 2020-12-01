import os
import pickle
import time
from Index import Indexer
from QueryProcessor import QueryProcessor
from pathlib import Path
from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)

# Preload required pickle data for the inverted index
print('Preloading pickled data')
with open('lexicon_revised.pkl', 'rb') as f:
    lexicon = pickle.load(f)
with open('corpus.pkl', 'rb') as f:
    corpus = pickle.load(f)

print('Finished!')

# Register '/' homepage path as search.html
@app.route("/")
def search():
    return render_template('search.html')

# Register '/results' path as results.html
@app.route("/results")
def results():
    return render_template('results.html')

# Register '/api/results' for frontend/backend communication
@app.route("/api/results")
def handle_results():
    # Grab query parameters from the url
    # e.g. /results?query=machine+learning
        # returns 'machine learning'
    query = request.args.get('query')

    # Call QueryProcessor.search to perform search on index
    start_time = time.perf_counter()
    results = QueryProcessor.search(query, lexicon, corpus)
    stop_time = time.perf_counter()
    print(f'found {len(results)} in {stop_time - start_time}')

    # Initialize a list for our JSON objects, this will serve as our JSON array
    json_array = list()

    # For each url in results create a JSON object using a dictionary
        # Each object should be in the format {'url':'https://www.google.com'}
        # Append each of these objects to our JSON array
        # Formatting the results like this is necessary to use jsonify()
    for url in results[:5]:
        json_object = dict()
        json_object["url"] = str(url)
        json_array.append(json_object)

    # Turn our JSON array into an actual JSON array using jsonify()
    # You can see the output format by adding a path to the url, eg.:
        # Original query is: http://127.0.0.1:5000/results?query=machine+learning
             # Change it to: http://127.0.0.1:5000/api/results?query=machine+learning to see JSON output
    return jsonify(json_array)

if __name__ == "__main__":
    app.run(use_reloader=True)