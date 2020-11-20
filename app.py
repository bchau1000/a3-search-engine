import os
import pickle
import time
from Index import Indexer
from QueryProcessor import QueryProcessor
from pathlib import Path
from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)

# Comment this out if you're just testing for front-end changes
print('Preloading pickled data')
with open('lexicon.pkl', 'rb') as f:
    lexicon = pickle.load(f)
with open('corpus.pkl', 'rb') as f:
    corpus = pickle.load(f)

print('Finished!')

@app.route("/")
def search():
    return render_template('search.html')

@app.route("/results")
def results():
    return render_template('results.html')

@app.route("/api/results")
def handle_results():
    query = request.args.get('query')

    start_time = time.perf_counter()
    results = QueryProcessor.search(query, lexicon, corpus)
    stop_time = time.perf_counter()
    print(f'found {len(results)} in {stop_time - start_time}')

    json_results = list()

    for url in results[:5]:
        json_object = dict()
        json_object["url"] = str(url)
        json_results.append(json_object)
    
    return jsonify(json_results)

if __name__ == "__main__":
    app.run(use_reloader=False)