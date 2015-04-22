__author__ = 'laceyliu'
from logsum import log_sum
import string
import sys

from collections import *
from numpy import *

#DIR = "hw10-data/"
DIR = ""
TRAIN = DIR + "train.txt"

class HMM:
    def __init__(self, trans, emit, prior):
        self.trans = create2DMap(trans)
        self.emit = create2DMap(emit)
        self.prior = create1DMap(prior)
        self.pi = self.prior
        self.alpha = []
        self.beta = []
        self.q = []
        self.vp = []

    def forward_evaluation(self, test):
        ret = []
        with open(test, "r") as f:
            for line in f:
                line = line.strip("\n")
                words = filter(None, line.split(" "))
                self.alpha = []
                a_tmp = {}

                for state in self.pi.keys():
                    a_tmp[state] = self.pi[state] + self.emit[state][words[0]]
                self.alpha.append(a_tmp)

                t = 0
                words = words[1:]

                for word in words:
                    a_tmp = {}
                    for state in self.emit.keys():
                        a_tmp[state] = self.emit[state][word]
                        cnt = 0
                        tmp = 0.0
                        for prev_state in self.alpha[t].keys():
                            if cnt == 0:
                                tmp = self.alpha[t][prev_state] + self.trans[prev_state][state]
                            else:
                                tmp = log_sum(tmp, self.alpha[t][prev_state] + self.trans[prev_state][state])
                            cnt += 1
                        a_tmp[state] += tmp
                    self.alpha.append(a_tmp)
                    t += 1

                cnt = 0
                pO_lambda = 0.0
                for state in self.alpha[t].keys():
                    if cnt == 0:
                        pO_lambda = self.alpha[t][state]
                    else:
                        pO_lambda = log_sum(pO_lambda, self.alpha[t][state])
                    cnt += 1
                ret.append(pO_lambda)

        return ret

    def backward_evaluation(self, test):
        ret = []
        with open(test, "r") as f:
            for line in f:

                line = line.strip("\n")
                words = filter(None, line.split(" "))
                self.beta = []
                b_tmp = {}

                for state in self.pi.keys():
                    b_tmp[state] = 0.0
                self.beta.append(b_tmp)
                t = 0

                o1 = words[0]
                words = words[1:]
                words = words[::-1]

                for word in words:
                    b_tmp = {}
                    for state in self.emit.keys():
                        cnt = 0
                        for next_state in self.beta[t].keys():
                            bb = self.beta[t][next_state] + self.emit[next_state][word] + self.trans[state][next_state]
                            if cnt == 0:
                                b_tmp[state] = bb
                            else:
                                b_tmp[state] = log_sum(b_tmp[state], bb)
                            cnt += 1
                    self.beta.append(b_tmp)
                    t += 1

                cnt = 0
                pO_lambda = 0.0
                for state in self.beta[t].keys():
                    tmp = self.pi[state]+self.emit[state][o1]+self.beta[t][state]
                    if cnt == 0:
                        pO_lambda = tmp
                    else:
                        pO_lambda = log_sum(pO_lambda, tmp)
                    cnt += 1
                ret.append(pO_lambda)

        return ret

    def viterbiDecoding(self, test):

        ret = []
        with open(test, "r") as f:
            for line in f:
                line = line.strip("\n")
                words = filter(None, line.split(" "))
                self.vp = []
                self.q = []
                a_tmp = {}

                q_star = {}
                for state in self.pi.keys():
                    a_tmp[state] = self.pi[state] + self.emit[state][words[0]]
                    q_star[state] = state
                self.vp.append(a_tmp)
                self.q.append(q_star)

                t = 0
                words2 = words[1:]

                for word in words2:
                    a_tmp = {}
                    q_star = {}

                    for state in self.emit.keys():
                        max = float("-inf")
                        a_tmp[state] = self.emit[state][word]
                        for prev_state in self.vp[t].keys():
                            tmp = self.vp[t][prev_state] + self.trans[prev_state][state]
                            if max < tmp:
                                max = tmp
                                q_star[state] = self.q[t][prev_state] + "." + state
                        a_tmp[state] += max

                    self.vp.append(a_tmp)
                    self.q.append(q_star)
                    t += 1


                max_seq = []
                max_prob = float("-inf")

                for state in self.vp[t].keys():
                    if max_prob < self.vp[t][state]:
                        max_prob = self.vp[t][state]
                        max_seq = self.q[t][state].split(".")

                tags = []
                for i in xrange(0, len(words)):
                    tags.append(words[i] + "_" + max_seq[i])
                ret.append(tags)
        return ret

def create2DMap(path):
    tmp = defaultdict(dict)
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\n")
            state_list = line.split(" ")
            state_list = filter(None, state_list)
            key = state_list[0]
            state_list = state_list[1:]
            t = {}
            for state in state_list:
                prob = state.split(":")
                t[prob[0]] = math.log(float(prob[1]))
            tmp[key] = t
    f.close()
    return tmp

def create1DMap(path):
    tmp = defaultdict(float)
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\n")
            prob = line.split(" ")
            tmp[prob[0]] = math.log(float(prob[1]))
    f.close()
    return tmp

def _main():
    global DIR, TRAIN
    test = DIR + sys.argv[1]
    trans = DIR + sys.argv[2]
    emit = DIR + sys.argv[3]
    prior = DIR + sys.argv[4]

    hmm = HMM(trans, emit, prior)

    #ret = hmm.forward_evaluation(test)
    #ret = hmm.backward_evaluation(test)
    ret = hmm.viterbiDecoding(test)
    out = ""
    for sentence in ret:
        for tag in sentence:
            out += tag + " "
        out = out[:-1]
        out += "\n"
    print out[:-1]
_main()


