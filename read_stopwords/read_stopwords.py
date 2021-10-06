import re

def populateStopWords():
    stopWords = []
    with open('stopwords.txt') as inputFile:
        for line in inputFile:
            if(line != '\n'):
                stopWords.append(line.rstrip())
    return stopWords

stopWords = populateStopWords()
for i in range(0,len(stopWords)):
    print(stopWords[i])
