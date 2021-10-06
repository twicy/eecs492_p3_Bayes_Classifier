import sys
import os
import numpy as np
import re, string
import operator

def computeConfusionMatrix(predicted, groundTruth, nAuthors):
	confusionMatrix = [[0 for i in range(nAuthors+1)] for j in range(nAuthors+1)]

	for i in range(len(groundTruth)):
		confusionMatrix[predicted[i]][groundTruth[i]] += 1

	return confusionMatrix


def outputConfusionMatrix(confusionMatrix):
	columnWidth = 4

	print(str(' ').center(columnWidth),end=' ')
	for i in range(1,len(confusionMatrix)):
		print(str(i).center(columnWidth),end=' ')

	print()

	for i in range(1,len(confusionMatrix)):
		print(str(i).center(columnWidth),end=' ')
		for j in range(1,len(confusionMatrix)):
			print(str(confusionMatrix[j][i]).center(columnWidth),end=' ')
		print()


def populateStopWords():
	stopWords = []
	with open('stopwords.txt') as inputFile:
		for line in inputFile:
			if (line != '\n'):
				stopWords.append(line.rstrip())
	return stopWords


def stripWhitespace(inputString):
	return re.sub("\s+", " ", inputString.strip())


def tokenize(inputString):
	whitespaceStripped = stripWhitespace(inputString)
	punctuationRemoved = "".join([x for x in whitespaceStripped
								  if x not in string.punctuation])
	lowercased = punctuationRemoved.lower()
	return lowercased.split()


def train(pathname, stopwords):
	nc = {}
	nci = {}
	for filename in os.listdir(pathname):
		with open(os.path.join(pathname, filename), "r", encoding="UTF-8", errors="ignore") as file:
			words = []
			for line in file:
				words.extend(tokenize(line))
			if "train" in filename:
				authorid = filename[filename.index("train") + 5: filename.index("train") + 7]
				if authorid not in nc.keys():
					nc[authorid] = 1
				else:
					nc[authorid] = nc[authorid] + 1

				for stopword in stopwords:
					temp_tuple = (authorid, stopword)
					if temp_tuple not in nci.keys():
						nci[temp_tuple] = 0

				for stopword in stopwords:
					temp_tuple = (authorid, stopword)
					if stopword in words:
						nci[temp_tuple] = nci[temp_tuple] + 1
	return nc, nci


def test(pathname, nc, nci, stopwords):
	total_file_number = 0
	list_of_prediction = {}
	for value in nc.values():
		total_file_number += value
	for filename in os.listdir(pathname):
		with open(os.path.join(pathname, filename), "r", encoding="UTF-8", errors="ignore") as file:
			appearance = {}
			if "train" not in filename:
				words = []
				for line in file:
					words.extend(tokenize(line))
				for stopword in stopwords:
					if stopword not in appearance.keys():
						appearance[stopword] = False

				for stopword in stopwords:
					if stopword in words:
						appearance[stopword] = True

				probability = []
				for authors in sorted(nc.keys()):
					pfic = 1.0
					for key in sorted(appearance.keys()):
						temp_tuple = (authors, key)
						if appearance[key]:
							pfic = pfic * (nci[temp_tuple] + 1)/(nc[authors] + 2)
						else:
							pfic = pfic * (1 - (nci[temp_tuple] + 1) / (nc[authors] + 2))
					probability.append(np.log2(nc[authors]/total_file_number) + np.log2(pfic))
					list_of_prediction[filename] = probability.index(max(probability))
	return list_of_prediction


def calculate_accuracy(predictedAuthorIdNum, groundTruthAuthorIdNum, nAuthors):
	outputConfusionMatrix(computeConfusionMatrix(predictedAuthorIdNum, groundTruthAuthorIdNum, nAuthors))


def calculate_entropy(nc, nci, stopwords):
	total_file_number = 0
	cce_list = {}
	for value in nc.values():
		total_file_number += value
	cce = 0.0
	for stopword in sorted(stopwords):
		for author in sorted(nc.keys()):
			tpl = (author, stopword)
			cce += (nc[author]/total_file_number) * (nci[tpl] + 1)/(nc[author] + 2) * np.log2((nci[tpl] + 1)/(nc[author] + 2))
		cce_list[stopword] = -cce
	return cce_list


def main(pathname):
	stopwords = populateStopWords()
	stopwords = list(set(stopwords))
	nc = {}
	nci = {}
	nc, nci = train(pathname, stopwords)
	list_of_prediction = test(pathname, nc, nci, stopwords)
	cce_list = calculate_entropy(nc, nci, stopwords)
	print(dict(sorted(cce_list.items(), key=operator.itemgetter(1), reverse=True)))
	result = {}
	for curr_file in list_of_prediction.keys():
		# Suppose you get result 0-index result, corresponding to author 1
		temp_str = str(list_of_prediction[curr_file] + 1)
		if len(temp_str) == 1:
			temp_str = '0' + temp_str
		result[pathname[14:] + curr_file] = 'Author' + temp_str
	# Key: Filename; Value: Author. Example: “problemA/Asample01.txt”: “Author03”
	groundTruthAuthorIdNum = []
	with open("test_ground_truth.txt", "r", encoding="UTF-8", errors="ignore") as file:
		for line in file:
			if pathname[-9:-1] in line:
				groundTruthAuthorIdNum.append(int(line[29:31]))
	calculate_accuracy([value + 1 for value in list_of_prediction.values()], groundTruthAuthorIdNum, len(nc))
	return result


if __name__ == "__main__":
	print(main(sys.argv[1]))
