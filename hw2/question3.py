import os
import sys

file = open(sys.argv[2], "r")
stopwordListStr = file.read()
file.close()

stopwordList = stopwordListStr.split("\n")

file = open(sys.argv[1], "r")
text = file.read()
file.close()

#textNoPunc = "".join(c for c in text if c not in ('!','.',':',','))
#tokens = textNoPunc.split(" ")
text = text.strip()
text = text.replace("\n", "")
text = text.lower()

tokens = text.split(" ")

tokens = [x for x in tokens if x]

for stopword in stopwordList:
	while (stopword in tokens):
		tokens.remove(stopword)

tokenMap={}
for token in tokens:
	if (token in tokenMap):
		tokenMap[token] += 1; 
	else:
		tokenMap[token] = 1; 


output = ""
for token in sorted(tokenMap.keys()):
	output += token+ ":" + str(tokenMap[token])+ ","

output = output[:-1]

sys.stdout.write(output)

#print '\n'




