import os

def indexer():
    #open all documents in documents/
    for root, dir, file in os.walk("documents/"):
        for fname in file:
            print("filename: " + fname)
            # with open(fname,'r') as doc:
                # try:
