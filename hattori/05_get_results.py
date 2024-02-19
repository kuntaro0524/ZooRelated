import sys,os
import DirectoryProc

def anaPath(pathname):
    # CC log name
    olog=os.path.join(pathname,"cc_orig.log")
    ilog=os.path.join(pathname,"cc_inv.log")
    
    def read_values(filename):
        if os.path.exists(filename)==False:
            return -999.999
        lines = open(filename,'r').readlines()
        
        for line in lines:
            if "overall CC" in line:
                #print(line)
                cols=line.split()
                #print(cols)
                value = float(cols[2])
                return value
    
    ovalue=(read_values(olog))
    ivalue=(read_values(ilog))
    
    if ovalue > ivalue:
        pvalue=ovalue
    else:
        pvalue=ivalue

    return pvalue

dp=DirectoryProc.DirectoryProc("./")
phase_dirs=dp.findTargetDirs("phase")

da=[]
for d in phase_dirs:
    if d.rfind("temp")!=-1:
        continue
    pvalue=anaPath(d)
    # cluster_#####
    ds = d.strip().split("/")[1]
    # columns
    try:
        run_id = int(d.strip().split("/")[2].split("_")[1])
        cindex = int(ds.replace("/","").replace(".","").split("_")[1])
    except:
        run_id=9999
        cindex=0
    da.append((d,cindex,run_id,pvalue))

import pandas as pd
df = pd.DataFrame(da, columns =['path', 'cluster_id','runid','mapcc'])
print(df)

df.to_csv("mapcc.csv")
