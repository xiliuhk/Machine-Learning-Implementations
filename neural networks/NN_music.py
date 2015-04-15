from numpy import *
import random
import sys
import math
import time

def sigmoid(x):
    return 1.0/(1+math.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x)*(1-sigmoid(x))

def makeMatrix(m, n, init = 0.0):
    ret = []
    tmp = [init]*m
    for i in xrange(0, n):
        ret.append(tmp)
    return ret

class ANN_1HL:

    def __init__(self, hiddenLayerSize = 25, inputSize = 1):

        self.hiddenLayerSize = hiddenLayerSize
        self.inputSize = inputSize

        self.inputs = [1.0]*(inputSize+1)
        self.hiddenValues = [1.0]*hiddenLayerSize
        self.output = 1.0

        self.inWeights = makeMatrix(inputSize+1, hiddenLayerSize, 1.0)
        for i in xrange(0, hiddenLayerSize):
            for j in xrange(1, inputSize+1):
                self.inWeights[i][j] = random.uniform(-0.05, 0.05)

        self.outWeights = []
        for i in xrange(0, hiddenLayerSize):
            self.outWeights.append(random.uniform(-0.05, 0.05))

        self.inWeightsPrev = makeMatrix(inputSize+1, hiddenLayerSize)

        self.outWeightsPrev = []
        for i in xrange(0, hiddenLayerSize):
            self.outWeightsPrev.append(1.0)

    def feedForward(self, inputs):
        for i in xrange(1, self.inputSize+1):
            self.inputs[i] = inputs[i-1]

        for i in xrange(0, self.hiddenLayerSize):
            sum = 0.0
            for j in xrange(0, self.inputSize+1):
                sum += self.inWeights[i][j]*self.inputs[j]
            self.hiddenValues[i] = sigmoid(sum)

        osum = 0.0
        for i in xrange(0, self.hiddenLayerSize):
            osum += self.hiddenValues[i]*self.outWeights[i]
        self.output = sigmoid(osum)
        return self.output

    def backPropagationAlgo(self, trainInst, key, learnRate, momentum):

        #error for output
        deltaOutput = sigmoid_deriv(self.output)*(key - self.output)

        #error for hiddens
        deltaHiddens = [0.0]*self.hiddenLayerSize
        for i in xrange(0, self.hiddenLayerSize):
            deltaHiddens[i] = sigmoid_deriv(self.hiddenValues[i])*(deltaOutput*self.outWeights[i])

        #update output weights
        for i in xrange(0, self.hiddenLayerSize):
            self.outWeights[i] += learnRate*deltaOutput*self.hiddenValues[i]

        #update input weights
        for i in xrange(0, self.hiddenLayerSize):
            for j in xrange(0, self.inputSize+1):
                self.inWeights[i][j] += learnRate*deltaHiddens[i]*self.inputs[j]

        #calculate total error
        error = 0.5*(key - self.output)**2

        return error

    def train(self, trainInsts, trainKeys, maxIter, startTime, learnRate = 0.5, momentum = 0.2):
        iteration = 0
        prev = float("inf")
        while iteration < maxIter and time.time()-startTime < 170:
            error = 0.0
            for i in xrange(0, len(trainInsts)):
                inst = trainInsts[i]
                key = trainKeys[i]
                output = self.feedForward(inst)
                error += self.backPropagationAlgo(inst, key, learnRate, momentum)
            iteration += 1
            if prev > error:
                prev = error
            else:
                break
            print error
        return error

    def vaidate(self, testFeature, testInsts, testKeys):
        print "TRAINING COMPLETED! NOW PREDICTING."
        hit = 0
        ret = ""
        n = len(testInsts)
        for i in xrange(0, n):
            output = self.feedForward(testInsts[i])
            if (output - 0.5)*10 > 0.5:
                ret = "yes"
            else:
                ret = "no"

            if ret == testKeys[i]:
                hit += 1

            print ret
            #print output
            print str(hit) + "/" + str(len(testKeys))
        return 0

def normalizeCol(instances, col):

    min_val = min(zip(*instances)[col])
    max_val = max(zip(*instances)[col])

    for i in xrange(0, len(instances)):
        instances[i][col] = (instances[i][col] - min_val)/(max_val - min_val)

    return instances

def createInstance(dataFile, purpose):
    file = open(dataFile, "r")
    setStr = file.read()
    file.close()

    setStr = setStr.replace("\r", "")
    instanceList = setStr.split("\n")
    instanceList = filter(None, instanceList)

    if len(instanceList) < 1:
        return None

    featureStr = instanceList[0];
    features = featureStr.split(",")

    instanceList.remove(featureStr)

    instances = []
    for instanceStr in instanceList:
        tmp = instanceStr.split(",")
        instance = []

        for attr in tmp:
            if attr == "yes":
                instance.append(1.0)
            elif attr == "no":
                instance.append(0.0)
            else:
                instance.append(float(attr))
        instances.append(instance)

    instances = normalizeCol(instances, 0)
    instances = normalizeCol(instances, 1)

    if purpose == "train":
        keys = []
        keyIndex = len(features)-1
        for inst in instances:
            keys.append(inst[keyIndex])
            inst.pop()
        return features, instances, keys
    else:
        return features, instances

def createTestKey(keyFile):

    file = open(keyFile, "r")
    setStr = file.read()
    file.close()
    keyList = setStr.split("\n")
    return keyList

def _main():

    start = time.time()

    trainFeature, trainInsts, trainKey = createInstance(sys.argv[1], "train")
    testFeature, testInsts = createInstance(sys.argv[2], "test")

    testKey = createTestKey("music_dev_keys.txt")

    ann = ANN_1HL(3, len(testFeature))

    trainError = ann.train(trainInsts, trainKey, 250, start, 0.1, 0)
    #print trainError

    testError = ann.vaidate(testFeature, testInsts, testKey)
    #print testError

    return

_main()



