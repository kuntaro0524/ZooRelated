import sys,os
import re

def isfloat2(s):
    p = '[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?'
    return True if re.fullmatch(p, s) else False

filename = sys.argv[1]

lines = open(filename,'r').readlines()

isRewrite=False
for line in lines:
    word = line.strip()
    if isfloat2(word):
        continue
    else:
        print("Not good", filename)
        resol = 10.0

if isRewrite:
    print("Rewriting!:",filename)
    ofile=open(filename,"w")
    ofile.write("%8.3f\n"%resol)
    ofile.close()
