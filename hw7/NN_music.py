from numpy import *
import random
import sys
import math
import time

def sigmoid(x):
    if x > 200:
        x = 200
    if x < -200:
        x = -200
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
                self.inWeights[i][j] = random.uniform(-0.5, 0.5)

        self.outWeights = []
        for i in xrange(0, hiddenLayerSize):
            self.outWeights.append(random.uniform(-0.5, 0.5))

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
        error = key - self.output
        deltaOutput = sigmoid_deriv(self.output)*error

        #error for hiddens
        deltaHiddens = [0.0]*self.hiddenLayerSize
        error = 0.0
        for i in xrange(0, self.hiddenLayerSize):
            error = deltaOutput*self.outWeights[i]
            deltaHiddens[i] = error*sigmoid_deriv(self.hiddenValues[i])

        #update output weights
        for i in xrange(0, self.hiddenLayerSize):
            change = deltaOutput*self.hiddenValues[i]
            self.outWeights[i] += learnRate*change + momentum*self.outWeightsPrev[i]
            self.outWeightsPrev[i] = change

        #update input weights
        for i in xrange(0, self.hiddenLayerSize):
            for j in xrange(0, self.inputSize+1):
                change = deltaHiddens[i] * self.inputs[j]
                self.inWeights[i][j] += learnRate*change + momentum*self.inWeightsPrev[i][j]
                self.inWeightsPrev[i][j] = change

        #calculate total error
        error = 0.5*(key - self.output)**2

        return error

    def train(self, trainInsts, trainKeys, maxIter, startTime, learnRate = 0.5, momentum = 0.2):
        iteration = 0
        while iteration < maxIter and time.time()-startTime < 170:
            error = 0.0
            for i in xrange(0, len(trainInsts)):
                inst = trainInsts[i]
                key = trainKeys[i]
                output = self.feedForward(inst)
                error += self.backPropagationAlgo(inst, key, learnRate, momentum)
            iteration += 1
            print error
        return error


    def vaidate(self, testFeature, testInsts, testKeys):
        print "TRAINING COMPLETED! NOW PREDICTING."
        error = 0.0
        n = len(testInsts)
        for i in xrange(0, n):
            output = self.feedForward(testInsts[i])
            if output > 0.5:
                print "yes"
            else:
                print "no"
            #print output
            #error += 0.5*(testKeys[i]-output)**2
        return 0

def normalizeCol(instances, col):

    avg = mean(zip(*instances)[col])
    s = std(zip(*instances)[col])

    for i in xrange(0, len(instances)):
        instances[i][col] = (instances[i][col] - avg)/s

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

    for inst in instances:
        inst[0] -= 1950
        inst[1] -= 5
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
    numKeys = []
    for key in keyList:
        if key == "yes":
            numKeys.append(1.0)
        else:
            numKeys.append(0.0)
    return numKeys


def _main():

    start = time.time()

    trainFeature, trainInsts, trainKey = createInstance(sys.argv[1], "train")
    testFeature, testInsts = createInstance(sys.argv[2], "test")

    testKey = createTestKey("music_dev_keys.txt")

    ann = ANN_1HL(35, len(testFeature))

    trainError = ann.train(trainInsts, trainKey, 50, start, 0.9, 0.1)
    #print trainError

    testError = ann.vaidate(testFeature, testInsts, testKey)
    #print testError

    return

_main()



