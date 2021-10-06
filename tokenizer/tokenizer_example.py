#!/usr/bin/env python
import re, string

def stripWhitespace(inputString):
    return re.sub("\s+", " ", inputString.strip())

def tokenize(inputString):
    whitespaceStripped = stripWhitespace(inputString)
    punctuationRemoved = "".join([x for x in whitespaceStripped
                                  if x not in string.punctuation])
    lowercased = punctuationRemoved.lower()
    return lowercased.split()

fileName = "Asample01.txt"
words = []
with open(fileName, errors='ignore') as inputFile:
    for line in inputFile:
        words.extend(tokenize(line))
print(words)
