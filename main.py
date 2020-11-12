import json
import os
from indexer import indexer
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from posting import Posting


# Make sure you have BeautifulSoup and NLTK installed

def main():
    docID = 0
    urlOut = open('url.txt', 'a')
    print('Starting...')

    # Set this to the path where you downloaded the developer JSON files
    rootDir = 'DEV/'

    invertedIndex = {}
    ps = PorterStemmer()

    # Traverse the directory tree starting at rootDir
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Grab JSON files
        for fname in fileList:
            # Get the path to the JSON file:
            # e.g. C:\Users\bchau\Desktop\Projects\developer.zip\DEV\aiclub_ics_uci_edu
            getPath = dirName + '/' + fname

            # Open the JSON file with above path
            with open(getPath) as f:
                # Load JSON file
                document = json.load(f)

                # Grab the HTML content from the JSON file and parse with BeautifulSoup
                soup = BeautifulSoup(document['content'], 'html.parser')

                # Tokenize the content, exclude punctuation, alphanumeric only
                tokenizer = RegexpTokenizer(r'\w+')
                output = tokenizer.tokenize(soup.get_text().lower())
                stem = [ps.stem(tk) for tk in output]

                # Output to .txt file in documents folder
                # Each .txt file is a separate webpage
                outputPath = 'documents/' + str(docID)
                if not os.path.exists('documents'):
                    os.makedirs('documents')

                with open(outputPath,'w+') as doc:
                    try:
                        # Top of the text file will have the actual URL, followed by the tokenized HTML content
                        doc.write(str(document['url']) + '\n')
                        doc.write(str(stem))
                    except:
                        print('Error @:', docID)

                freq = {}
                for x in stem:
                    # if exists, up the counter.
                    # if doesn't exist, add.
                    if x in freq:
                        freq[x] += 1
                    else:
                        freq[x] = 1

                for word in freq:
                    posting = Posting(docID, freq[word])
                    # print(posting.id)
                    if word in invertedIndex:
                        # print("1")
                        invertedIndex[word].append(posting)
                    else:
                        # print("2")
                        invertedIndex[word] = []
                        invertedIndex[word].append(posting)


                print('Tokenized: ', docID)

                # Currently limiting the output to only 200 webpages, haven't let the full program run yet
                # if(docID == 100):
                #     return
                urlOut.write(str(docID) + ' ' + document['url'] + '\n')

                docID += 1

    indexOutput = open('index.txt', 'w')
    # print invertedIndex.length
    for x in invertedIndex:
        # print(x, end=" ")
        indexOutput.write(x + ' ')
        for p in invertedIndex[x]:
            # print(str(p.id) + " " + p.url + " " + str(p.tokenCount), end=" ")
            indexOutput.write(str(p.id) + ':' + str(p.tokenCount) + ', ')

            # print("")
        indexOutput.write('\n')
    indexOutput.close()
    urlOut.close()


    print('Finished.')


main()
