import os
import sys

path = sys.argv[1]

file = open(path, "r")
text = file.read()
file.close()

#textNoPunc = "".join(c for c in text if c not in ('!','.',':',','))
#tokens = textNoPunc.split(" ")
text = text.strip()
text = text.replace("\n", "")
text = text.lower()

tokens = text.split(" ")

tokens = [x for x in tokens if x]

tokenMap={}

for token in tokens:
	if (token in tokenMap):
		tokenMap[token] += 1; 
	else:
		tokenMap[token] = 1; 

output = ""

for token in sorted(tokenMap.keys()):
	output += token+ ","

output = output[:-1]


sys.stdout.write(output)

#print '\n'

