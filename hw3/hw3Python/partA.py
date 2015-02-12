import os
import sys
import math


FILE_TRAIN = "9Cat-Train.labeled"
FILE_DEV = "9Cat-Dev.labeled"
FILE_TEST = sys.argv[1]

PARTA4 = "PARTA4.txt"

def creatInstanceList(dataset):
	ret = []
	file = open(dataset, "r")
	setStr = file.read()
	file.close()
	instanceList = setStr.split("\n")
	instanceList = filter(None, instanceList)
	for instance in instanceList:
		features = []
		tmp = instance.split("	")
		for feature in tmp:
			features.append((feature.split(" "))[1].replace("\r", ""))
		ret.append(features)	
	return ret

def findSAlgo(trainSet, noFeature):
	hypophesis = []
	count = 0; 
	file = open(PARTA4, "w")
	
	for i in xrange(0,noFeature):
		hypophesis.append("null")
		#print i
	for instance in trainSet:
		#features = instance.split("	")
		count += 1		
		if (count % 30 == 0):
			for i in xrange(0,noFeature):
			#for concept in hypophesis:
				file.write(hypophesis[i])
				if (i<noFeature-1):
					file.write("	")
				else:
					file.write("\n")
		if (instance[noFeature] == "low"):
			continue; 
		else: 
			for i in xrange(0,noFeature):
				#print i
				#print hypophesis[i] + " vs " + instance[i]
				if (hypophesis[i] == "null"):
					hypophesis[i] = instance[i]
				elif (hypophesis[i] != instance[i] and hypophesis!="?"):
					hypophesis[i] = "?"
	file.close()
	return hypophesis

def compareGold(myClass, gold, featureNo):
	fractionRate = 0.0
	misCount = 0

	if (len(myClass) != len(gold)):
		return 0.0

	i = 0; 
	for instance in gold:
		#features = instance.split("	")

		if (instance[featureNo] != myClass[i]):
			misCount += 1; 
		i += 1

	fractionRate = float(misCount)/len(myClass)
		
	return fractionRate

def classify(testSet, hypophesis):
	classification = []
	isHigh = True
	for instance in testSet:
		#features = instance.split("	")
		for i in xrange(0, len(hypophesis)-1):
			if (hypophesis[i] != "?" and hypophesis[i] != instance[i]):
				isHigh = False
		if (isHigh):
			classification.append("high")
		else:
			classification.append("low")
			isHigh = True
			
	return classification		



def _main():
	trainSet = creatInstanceList(FILE_TRAIN)
	devSet = creatInstanceList(FILE_DEV)
	testSet = creatInstanceList(FILE_TEST)

	instanceNo = len(trainSet)
	featureNo = len(trainSet[0]) - 1
	#print featureNo
	
	#print "inst:"+str(instanceNo)
	#print trainSet[0]
	#print "feature:"+str(featureNo)

	instanceSpaceSize = int(math.pow(2, featureNo))
	conceptNo = int(math.pow(2, instanceSpaceSize))
	hypoSpaceSize = int(math.pow(3, featureNo))+1

	#train the model
	hypo = findSAlgo(trainSet, featureNo)

	#test with dev_set and calculate fractionRate
	classify_dev = classify(devSet, hypo)
	fractionRate = compareGold(classify_dev, devSet, featureNo)

	sys.stdout.write(str(instanceSpaceSize)+ "\n")
	sys.stdout.write(str(len(str(conceptNo)) )+ "\n")
	sys.stdout.write(str(hypoSpaceSize)+ "\n")
	sys.stdout.write(str(fractionRate)+ "\n")

	#test with test set
	classify_test = classify(testSet, hypo)
	for ret in classify_test:
		sys.stdout.write(ret + "\n" )



_main()





