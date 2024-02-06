import sys,os
import pandas as pd
import glob

df = pd.read_csv(sys.argv[1])
phs_log=".PHASING"

n_file=0

def ana_phasing_result(procpath):
    sadpath=os.path.join(procpath,"00.SAD")
    target_file=os.path.join(sadpath, phs_log)
    csv_file=os.path.join(sadpath,"phasing_results.csv")

    cols=di.split("/")
    wavelength=float(cols[8].split("_")[1].replace("A",""))/10.0
    dose=float(cols[8].split("_")[2].replace("MGy",""))
    n_merged=int(cols[-1].split("_")[0].replace("merge",""))
    merge_index=int(cols[-1].split("_")[1].replace("index",""))
    print(wavelength,dose,n_merged,merge_index)

    if os.path.exists(csv_file):
        tmpdf=pd.read_csv(csv_file)
        tmpdf['path']=procpath
        tmpdf['wavelength']=wavelength
        tmpdf['dose']=dose
        tmpdf['n_merged']=n_merged
        tmpdf['merge_index']=merge_index

        # Read from mapcc.dat
        mapcc_file=os.path.join(sadpath,"mapcc.dat")
        if os.path.exists(mapcc_file):
            lines=open(mapcc_file,"r").readlines()
            for line in lines:
                if "overall CC:" in line:
                    overall_cc=float(line.split()[2])
                if "local CC:" in line:
                    local_cc=float(line.split()[2])
            tmpdf['overall_cc']=overall_cc
            tmpdf['local_cc']=local_cc
        else:
            tmpdf['overall_cc']=-9999.9999
            tmpdf['local_cc']=-9999.9999

        return tmpdf
    else:
        print("open failed %s" % csv_file)

n_store=0
for index, col in df.iterrows():
    filepath=col['procpath']
    dirlist=glob.glob("%s/*"%filepath)
    for di in dirlist:
        if "merge" in di and "index" in di:
            tmpdf=ana_phasing_result(di)
            
            if n_file==0:
                final_df=tmpdf
            else:
                final_df=pd.concat([final_df,tmpdf])
            n_file+=1

final_df.to_csv("phasing_summary_merged.csv", index=None)

