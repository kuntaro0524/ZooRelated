import DirectoryProc
import pandas as pd

dp = DirectoryProc.DirectoryProc("./")

def getB(fname):
    lines = open(fname,"r").readlines()
    for line in lines:
        if "Least squares straight line gives:" in line:
            idx=line.rfind("B  =")
            str1=line[idx:].split("=")
            try:
                bfactor = float(str1[1].split()[0])
            except:
                bfactor = -9999
                print(line)
            try:
                scale = float(str1[2])
            except:
                scale = -9999
                print(line)
            return scale, bfactor

def clusterInfo(fname):
    paths = fname.split('/')
    print(paths)
    for p in paths:
        try:
            if "cluster" in p:
                cluster_id = int(p.replace("cluster_",""))
        except:
            cluster_id = 99999
        try:
            if "run" in p:
                run_number = int(p.replace("run_",""))
        except:
            run_number = 99999

    return cluster_id, run_number

flist,dlist=dp.findTarget("wilson.log")
dic_list=[]
for fname,dname in zip(flist,dlist):
    scale,bfactor=getB(fname)
    cluster_id, run_number = clusterInfo(fname)
    dic_tmp={"scale":scale, "bfactor": bfactor, "path": fname,"cluster": cluster_id, "run":run_number}
    dic_list.append(dic_tmp)

    clusterInfo(fname)

df = pd.DataFrame(dic_list)

df.to_csv("wilson.csv")
