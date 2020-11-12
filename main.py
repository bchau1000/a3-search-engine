import json
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer 


# Make sure you have BeautifulSoup and NLTK installed
        
def getHTMLContent(rootDir):
    docID = 0
    
    # Traverse the directory tree starting at rootDir
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Grab JSON files
        for fname in fileList:
            # Get the path to the JSON file:
            # e.g. C:\Users\bchau\Desktop\Projects\developer.zip\DEV\aiclub_ics_uci_edu
            getPath = dirName + '\\' + fname
            
            # Open the JSON file with above path
            with open(getPath) as f:
                # Load JSON file
                document = json.load(f)
                
                # Grab the HTML content from the JSON file and parse with BeautifulSoup
                soup = BeautifulSoup(document['content'], 'html.parser')
                
                # Tokenize the content, exclude punctuation, alphanumeric only
                tokenizer = RegexpTokenizer(r'\w+')
                output = tokenizer.tokenize(soup.get_text().lower())
                
                with open('urlMap.txt','a+', encoding="utf-8") as urlMap:
                    urlMap.write(str(document['url']) + ' ' + str(docID) + '\n')
                
                # Output to .txt file in documents folder
                # Each .txt file is a separate webpage
                outputPath = 'documents/' + str(docID) + '.txt'
                if not os.path.exists('documents'):
                    os.makedirs('documents')
                    
                with open(outputPath,'a+', encoding="utf-8") as doc:
                    try:
                        tokens = " ".join(output)
                        doc.write(str(tokens))
                    except Exception as e:
                        with open('errors.txt','a+') as errors:
                            errors.write(str(docID) + ': ' + str(e) + '\n')
                            
                docID += 1

def invertedIndex(tokenDir):
    invertedIndex = dict()
    
    for dirName, subdirList, fileList in os.walk(tokenDir):
        for fname in fileList:
            getPath = dirName + '\\' + fname
            with open(getPath, 'r', encoding="utf-8") as f:
                tokenList = list()
                for line in f:
                    tokenList.extend(line.split())
                
                ps = PorterStemmer()
                
                for token in tokenList:
                    docID = fname.replace('.txt', ' ')
                    
                    tokenStem = str(ps.stem(token))
                    if tokenStem not in invertedIndex:
                        invertedIndex[tokenStem] = list()
                        invertedIndex[tokenStem].append(docID)
                    else:
                        invertedIndex[tokenStem].append(docID)
                
    return invertedIndex
                    
                

def main():
    print('Starting...')
    
    rootDir = 'C:\\Users\\bchau\\Desktop\\Projects\\developer\\DEV'
    getHTMLContent(rootDir)
    
    tokenDir = 'C:\\Users\\bchau\\Desktop\\Projects\\a3-indexer\\documents'
    indexedTokens = invertedIndex(tokenDir)
    
    with open('index.txt', '+a', encoding="utf-8") as f:
        for key, value in indexedTokens.items():
            f.write(str(key) + ': ' + str(value) + '\n\n')
    
    print('Finished.')

main()