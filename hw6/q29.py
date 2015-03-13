import math
from collections import defaultdict

DATA_PATH = ""
TESTSET = [[8.03, 6.9], [8.03, 8.19], [8.03, 7.45], [8.03, 5.7]]

def createInstance(path):
    instances = []

    file = open(path, "r")
    setStr = file.read()
    file.close()
    setStr = setStr.replace("\r", "")

    instanceStrs = setStr.split("\n")
    instanceStrs = filter(None, instanceStrs)

    for instanceVal in instanceStrs:
        instance = instanceVal.split("\t")
        instances.append(instance)

    return instances

def calculateExpect(instances, col):
    expect = 0.0
    valMap = defaultdict(float)
    N = len(instances)

    for instance in instances:
        valMap[instance[col]] += 1.0/N

    for val in valMap.keys():
        expect += float(val)*valMap[val]

    return expect

def calculateVariance(instances, col):
    var = 0.0

    exp = calculateExpect(instances, col)

    valMap = defaultdict(float)
    N = len(instances)

    for instance in instances:
        val = float(instance[col]) - exp
        valMap[val*val] += 1.0/N

    for val in valMap.keys():
        var += val*valMap[val]

    return var

def calculateCov(instances, x, y):
    exp_x = calculateExpect(instances, x)
    exp_y = calculateExpect(instances, y)

    cov = 0.0

    valMap = defaultdict(float)
    N = len(instances)

    for instance in instances:
        x_val = float(instance[x]) - exp_x
        y_val = float(instance[y]) - exp_y
        valMap[x_val*y_val] += 1.0/N

    cov = 0.0
    for val in valMap.keys():
        cov += val*valMap[val]

    return cov


def main():

    for i in xrange(1, 5):

        DATA_PATH = "data"+str(i)+".txt"
        instances = createInstance(DATA_PATH)

        exp_X = calculateExpect(instances, 0)
        exp_Y = calculateExpect(instances, 1)

        var_X = calculateVariance(instances, 0)
        var_Y = calculateVariance(instances, 1)

        cov = calculateCov(instances, 0, 1)

        slope = cov/var_X
        y_intercept = exp_Y - slope*exp_X

        cor = cov/math.sqrt(var_X)/math.sqrt(var_Y)

        testPoint = TESTSET[i-1]

        test_x = testPoint[0]
        test_y = testPoint[1]

        error = math.fabs(test_y - (slope*test_x+y_intercept))

        print ("-------------data"+str(i)+"----------------")
        print ("EXP_X: "+ "{:.1f}".format(exp_X))
        print ("EXP_Y: "+ "{:.1f}".format(exp_Y))
        print ("VAR_X: "+ "{:.1f}".format(var_X))
        print ("VAR_Y: "+ "{:.1f}".format(var_Y))
        print ("Slope: "+ "{:.1f}".format(slope))
        print ("Y_Intercept: "+ "{:.1f}".format(y_intercept))
        print ("Cor_XY: "+ "{:.1f}".format(cor))
        print ("Error: "+ "{:.1f}".format(error))

    '''

    for i in xrange(1,3):
        DATA_PATH = "debug"+str(i)+".txt"
        instances = createInstance(DATA_PATH)

        exp_X = calculateExpect(instances, 0)
        exp_Y = calculateExpect(instances, 1)

        var_X = calculateVariance(instances, 0)
        var_Y = calculateVariance(instances, 1)

        cov = calculateCov(instances, 0, 1)

        slope = cov/var_X
        y_intercept = exp_Y - slope*exp_X

        cor = cov/math.sqrt(var_X)/math.sqrt(var_Y)

        print ("-------------data"+str(i)+"----------------")
        print ("EXP_X: "+ "{:.1f}".format(exp_X))
        print ("EXP_Y: "+ "{:.1f}".format(exp_Y))
        print ("VAR_X: "+ "{:.1f}".format(var_X))
        print ("VAR_Y: "+ "{:.1f}".format(var_Y))
        print ("Slope: "+ "{:.1f}".format(slope))
        print ("Y_Intercept: "+ "{:.1f}".format(y_intercept))
        print ("Cor_XY: "+ "{:.1f}".format(cor))

    '''
main()