#!/usr/bin/env python


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

# Auhhor's id are from test_ground_truth = [1,2,...]
predictedAuthorIdNum = [1, 3, 2, 4]
groundTruthAuthorIdNum = [1, 3, 2, 4]
nAuthors = 4
outputConfusionMatrix(computeConfusionMatrix(predictedAuthorIdNum, groundTruthAuthorIdNum, nAuthors))
