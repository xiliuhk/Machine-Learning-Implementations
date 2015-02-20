import math
import sys
import os
import collections

TRAIN_FILE = ""
TEST_FILE = ""
OUTPUT_FILE = ""

class Node:
	def _init_(self, parent = None):
		self.parent = parent
		self.children = []
		self.splitFeature = None
		self.selfValue = None
		self.label = None

def createInstance(dataFile):
	file = open(dataFile, "r")
	setStr = file.read()
	file.close()
	instanceList = setStr.split("\n")
	instanceList = filter(None, instanceList)
	
	if len(instanceList) < 1:
		return  None

	instances = []
	features = instanceList[0].split(",")
	features = filter(None, features)

	for i in xrange(1, len(instanceList)):
		for (feature, value) in (features, filter(None, instanceList[i].split(",")):
			instance = {}
			instance[feature] = value
		instances.append(instance)

	return features, instances


def computeEntropy(instances, feature):

	if len(instances)<=1:
		return 0

	valueCnt = defaultdict(int)

	for instance in instances: 
		valueCnt[instance[feature]]+=1
	if len(valueCnt) <=1:
		return 0

	N = len(instances)
	V = len(valueCnt)
	entropy = 0.0
	for value in valueCnt:
		p = valueCnt[value]/N
		entropy -= p*math.log(p, V)

	return entropy 

def computeInfoGain(instances, feature, target):
	
	currentEntropy = computeEntropy(instances, feature)
	childList = defaultdict(list)
	
	for instance in instances:
		childList[instance[feature]].append(instance)
	
	nextEntropy = 0.0
	N = len(instances)
	for child in childList:
		p = len(childList[child[feature]])/N
		nextEntropy += p*entropy(childList[child[feature]], feature) 
	
	infoGain = currentEntropy - nextEntropy
	
	return infoGain

def majorityVote(instances, feature):
	valueCnt = defaultdict(int)
	maxCnt = 0
	majority = None
	for instance in instances: 
		valueCnt[instance[feature]]+=1
		if (valueCnt[instance[feature]>maxCnt]):
			maxCnt = valueCnt[instance[feature]]
			majority = instance[feature]
	return majority

def split(instances, feature):		
	children = defaultdict(list)
	for instance in instances:
		children[instances[feature]].append(instance)
	return children

def computeSplit(instances, features, target):
	maxGain = 0.0
	splitFeature = ""
	for feature in features:
		tmpGain = computeInfoGain(instances, feature, target)
		if (tmpGain>maxGain):
			maxGain = tmpGain
			splitFeature = feature
	return splitFeature

def buildDecisionTree(instances, candidates, target):

	root = Node()

	# contains same lables
	labelCnt = defaultdict(int)
	for instance in instances:
		 labelCnt[instance[target]] +=1
	if len(labelCnt)<=1:
		root.label = instances[1][target]
		return root
	#no split features left	
	if len(candidates) == 0:
		root.label = majorityVote(instances, target)
		return root
	#find the split feature with max info gain	
	splitFeature = computeSplit(instances, candidates, target)

	#no more info gained, finish
	if computeInfoGain(instances, candidates, target) == 0:
		root.label = majorityVote(instances, target)
		return root

	#split by chosen split feature	
	root.splitFeature = splitFeature
	root.children = split(instance, splitFeature)


	reuturn DT

def classify(tree, instances, features, target):


def ouputDTree(tree):
	
	return



def _main():
	TRAIN_FILE = sys.argv[0]
	TEST_FILE = sys.argv[1]

	trainFeature, trainSet = createInstance(TRAIN_FILE)
	testFeature, testSet = createInstance(TEST_FILE)

	#trainset and testset not match
	if len(trainFeature) != len(testFeature):
		return None
	#empty trainset
	if len(trainSet) < 1:
		return None;
	
	target = trainFeature[len(trainFeature)-1]
	decisionTree = buildDecisionTree(trainSet, trainFeature, target)

	ouputDTree(decisionTree)

	trainErr = classify(decisionTree, trainSet, trainFeature, target)
	print trainErr
	
	testErr = classify(decisionTree, testSet, testFeature, target)
	print testErr

	
main()


	