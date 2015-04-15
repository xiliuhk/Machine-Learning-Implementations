import os
import math
import sys
import operator
from collections import defaultdict


POS = ["yes", "A"]
NEG = ["no", "notA"]

TRAIN = ""
TEST = ""


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.splitFeature = None
        self.infoGain = 0.0
        self.label = None
        self.countYes = 0
        self.countNo = 0
        self.instances = []


def createInstance(dataFile):
    file = open(dataFile, "r")
    setStr = file.read()
    file.close()

    setStr = setStr.replace("\r", "")
    instanceList = setStr.split("\n")
    instanceList = filter(None, instanceList)

    if len(instanceList) < 1:
        return None

    features = instanceList[0].split(",")
    instances = []

    for i in xrange(1, len(instanceList)):
        tmp = instanceList[i].split(",")
        instance = {}
        for j in xrange(0, len(tmp)):
            value = tmp[j]
            feature = features[j]
            instance[feature] = value
        instances.append(instance)
    return features, instances


def countLabels(instances, feature):
    labelCnt = defaultdict(int)

    for instance in instances:
        labelCnt[instance[feature]] += 1

    return labelCnt


def voteForMajority(instances, target):
    labelCnt = countLabels(instances, target)
    maxCnt = 0
    majority = ""

    for key in labelCnt.keys():
        if labelCnt[key] > maxCnt:
            maxCnt = labelCnt[key]
            majority = key

    return majority


def computeEntropy(instances, feature):
    if len(instances) <= 1:
        return 0

    valueCnt = countLabels(instances, feature)

    if len(valueCnt) < 1:
        return 0

    N = len(instances)

    entropy = 0.0

    for value in valueCnt.keys():
        p = 1.0*valueCnt[value] / N
        entropy -= p * math.log(p, 2)

    return entropy


def computeInfoGain(instances, feature, target):
    curEntropy = computeEntropy(instances, target)

    children = defaultdict(list)

    for instance in instances:
        children[instance[feature]].append(instance)

    nextEntropy = 0.0

    N = len(instances)

    for childLabel in children.keys():
        p = len(children[childLabel]) / float(N)
        nextEntropy += p * computeEntropy(children[childLabel], target)

    infoGain = curEntropy - nextEntropy

    return infoGain


def selectSplitFeature(instances, candidateFeatures, target):
    maxGain = 0.0
    splitFeature = ""

    for candidate in candidateFeatures:
        curGain = computeInfoGain(instances, candidate, target)
        if curGain > maxGain:
            maxGain = curGain
            splitFeature = candidate

    return splitFeature


def splitDataset(instances, splitFeature):
    children = defaultdict(list)
    for instance in instances:
        #print instance[splitFeature]
        children[instance[splitFeature]].append(instance)
    return children


def buildDTree(root, instances, candidateFeatures, target, height):

    # count for each label
    cntMap = countLabels(instances, target)
    for label in cntMap.keys():
        if label in POS:
            root.countYes = cntMap[label]
        else:
            root.countNo = cntMap[label]

    if len(instances) == 0:
        return root

    if height > 2:
        return root
    # all same target label
    if len(cntMap) == 1:
        root.label = instances[0][target]
        return root
    # no candidate left    
    if len(candidateFeatures)==0 :
        root.label = voteForMajority(instances, target)
        return root

    # split dataset by max info gain    
    splitFeature = selectSplitFeature(instances, candidateFeatures, target)

    root.infoGain = computeInfoGain(instances, splitFeature, target)
    if root.infoGain < 0.1:
        return root

    childrenMap = splitDataset(instances, splitFeature)
    root.splitFeature = splitFeature
    candidateFeatures.remove(splitFeature)

    for childLabel in childrenMap.keys():
        child = Node(root)
        child.instances = childrenMap[childLabel]
        child.label = childLabel
        child = buildDTree(child, child.instances, candidateFeatures, target, height+1)
        root.children.append(child)

    return root


def outputDTree(root):
    print("[" + str(root.countYes) + "+/" + str(root.countNo) + "-]")
    bfsPrint(root, 0)

def bfsPrint(root, layer):
    if len(root.children) == 0:
        return
    for i in xrange(0, layer):
        sys.stdout.write("| ")

    sys.stdout.write(str(root.splitFeature) + " = " + str(root.children[0].label) + ": [" + str(root.children[0].countYes) + "+/" + str(root.children[0].countNo) + "-]\n")
    if len(root.children[0].children) != 0:
        bfsPrint(root.children[0], layer+1)

    for i in xrange(0, layer):
        sys.stdout.write("| ")

    sys.stdout.write(str(root.splitFeature) + " = " + str(root.children[1].label) + ": [" + str(root.children[1].countYes) + "+/" + str(root.children[1].countNo) + "-]\n")
    if len(root.children[1].children) != 0:
        bfsPrint(root.children[1], layer+1)
    return

def classify(root, instances, features, target):
    cntMap = countLabels(instances, target)
    for label in cntMap.keys():
        if label in POS:
            root.countYes = cntMap[label]
        else:
            root.countNo = cntMap[label]
    if len(root.children) == 0:
        return root

    childrenMap = splitDataset(instances, root.splitFeature)
    features.remove(root.splitFeature)
    for child in root.children:
        child.instances = childrenMap[child.label]
        #if len(child.children) > 0:
        child = classify(child, child.instances, features, target)
    return root

def countMis(root):
    mis = 0
    for child in root.children:
        if len(child.instances) == 0:
            continue
        if len(child.children) == 0:
            if child.label in POS:
                mis += child.countNo
            else:
                mis += child.countYes
        else:
            mis += countMis(child )

    return mis

########################################################
#main func
def main():
    TRAIN = sys.argv[1]
    TEST = sys.argv[2]

    trainFeatures, trainSet = createInstance(TRAIN)
    testFeatures, testSet = createInstance(TEST)

    if len(trainSet) < 1 or trainSet == None:
        print "empty!"
        return None

    target = trainFeatures[len(trainFeatures) - 1]

    trainFeatures.remove(target)
    testFeatures.remove(target)

    root = Node()
    root = buildDTree(root, trainSet, trainFeatures, target, 1)
    outputDTree(root)

    trainError = float(countMis(root))/len(trainSet)
    sys.stdout.write("error(train): "+ "{:.2f}".format(trainError)+"\n")

    testDT = classify(root, testSet, testFeatures, target)
    #outputDTree(testDT)
    testError = float(countMis(testDT))/len(testSet)
    sys.stdout.write("error(test): "+ "{:.2f}".format(testError)+"\n")

    return

#print "error(train): " + str(trainErr)

#testErr = classify(decisionTree, testSet, testFeatures, target)
#print "error(train): " + str(testErr)

main()

    