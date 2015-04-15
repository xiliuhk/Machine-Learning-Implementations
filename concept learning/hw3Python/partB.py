import os
import sys
import math


FILE_TRAIN = "4Cat-Train.labeled"
FILE_DEV = "4Cat-Dev.labeled"
FILE_TEST = sys.argv[1]
gender = ["Male", "Female"]
age = ["Young", "Old"]
student = ["Yes", "No"]
pDeclined = ["Yes", "No"]
risk = ["low", "high"]
	
#PARTA4 = "PARTB5.txt"

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


def vote(testSet, versionSpace):
	
	for instance in testSet:
		#print instance
		high = 0
		low = 0
		for concept in versionSpace:
			i = 0
			
			#print(concept)
			
			while(i<4 and concept[i] == instance[i]):
				i+=1
			
			if (i == 4): 
				if (concept[4] == "high"):
					high +=2*len(versionSpace)
				elif (concept[4] == "low"): 
					low += 2*len(versionSpace)
				else:
					low += len(versionSpace)
					high += len(versionSpace)
			
			
		sys.stdout.write(str(high)+" "+str(low)+"\n")
	return	

def listThenEliminate(conceptSpace, trainSet):
	versionSpaceHD = []
	for hp in conceptSpace:
		hp.append("unknown")
		for instance in trainSet:				
			i = 0
			while(i<4 and hp[i] == instance[i]):
				i+=1
			if (i== 4):
				hp[i] = instance[i]
			else: 
				continue
		versionSpaceHD.append(hp)
	return versionSpaceHD


def buildEntireConceptSpace(featureDict):	
	
	conceptSpace = []
	
	for x in xrange(0,16):	
		concept = []
		binaryStr = '{0:04b}'.format(x)
		for d in xrange(0, 4): 
			i = int(binaryStr[d])
			concept.append(featureDict[d][i])
		conceptSpace.append(concept)
	return conceptSpace


def _main():
	trainSet = creatInstanceList(FILE_TRAIN)
	devSet = creatInstanceList(FILE_DEV)
	testSet = creatInstanceList(FILE_TEST)

	instanceNo = len(trainSet)
	featureNo = len(trainSet[0]) - 1
	
	instanceSpaceSize = int(math.pow(2, featureNo))
	conceptNo = int(math.pow(2, instanceSpaceSize))

	sys.stdout.write(str(instanceSpaceSize)+ "\n")
	sys.stdout.write(str(conceptNo)+ "\n")

	featureDict = [gender, age, student, pDeclined]
	conceptSpace = buildEntireConceptSpace(featureDict)
	
	#print trainSet
	#train the model
	versionSpace = listThenEliminate(conceptSpace, trainSet)
	sys.stdout.write(str(len(versionSpace)*2)+ "\n")
	#sys.stdout.write(str(len(versionSpace))+"\n")

	#test with dev_set and calculate fractionRate
	vote(testSet, versionSpace)


_main()






