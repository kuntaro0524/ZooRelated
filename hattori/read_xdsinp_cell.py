import os,sys

filename=sys.argv[1]

lines=open(filename,"r").readlines()

for line in lines:
    if "UNIT_CELL" in line:
        cols=line.split()
        print("%8s %8s %8s %8s %8s %8s"% (cols[1],cols[2],cols[3],cols[4],cols[5],cols[6]))
