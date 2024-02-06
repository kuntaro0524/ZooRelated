import sys,os
import pandas as pd
import glob

sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs")
sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/summarize_stats/")

import AnaXSCALE
import PhenixMergingStats

df = pd.read_csv(sys.argv[1])

phs_log=".PHASING"

n_file=0

def ana_phasing_result(procpath, subdir="00.SAD", column="dm100"):
    sadpath=os.path.join(procpath,subdir)
    target_file=os.path.join(sadpath, phs_log)
    csv_file=os.path.join(sadpath,"phasing_results.csv")

    cols=di.split("/")
    wavelength=float(cols[8].split("_")[1].replace("A",""))/10.0
    dose=float(cols[8].split("_")[2].replace("MGy",""))
    n_merged=int(cols[-1].split("_")[0].replace("merge",""))
    merge_index=int(cols[-1].split("_")[1].replace("index",""))
    print(wavelength,dose,n_merged,merge_index)

    # Column title of mapcc
    # 00.SAD == 100 cycle DM.
    # I do not like to rewrite plotting program.
    # Then, 00.SAD holds 'non-tagged' column name
    if subdir=="00.SAD":
        mapcc_overall="overall_cc"
        mapcc_local="local_cc"
    else:
        mapcc_overall="overall_cc_%s" % column
        mapcc_local="local_cc_%s" % column

    if os.path.exists(csv_file):
        tmpdf=pd.read_csv(csv_file)
        tmpdf['path']=procpath
        tmpdf['wavelength']=wavelength
        tmpdf['dose']=dose
        tmpdf['n_merged']=n_merged
        tmpdf['merge_index']=merge_index

        # Read from mapcc.dat
        mapcc_file=os.path.join(sadpath,"mapcc.dat")
        # Writing mapcc file
        if os.path.exists(mapcc_file):
            lines=open(mapcc_file,"r").readlines()
            for line in lines:
                if "overall CC:" in line:
                    overall_cc=float(line.split()[2])
                if "local CC:" in line:
                    local_cc=float(line.split()[2])
            # Save values to data frame
            tmpdf[mapcc_overall]=overall_cc
            tmpdf[mapcc_local]=local_cc
        else:
            tmpdf[mapcc_overall]=0.0
            tmpdf[mapcc_local]=0.0

        return tmpdf
    else:
        print("open failed %s" % csv_file)

# For each merging directory
def ana_intensity_stats(procpath):
    # logging check
    import logging, logging.config
    logname = "summarize_xscale_phenix_stats.log"
    configfile = "/isilon/users/target/target/Staff/rooms/kuntaro/Libs/logging.conf"
    logging.config.fileConfig(configfile, defaults={'logfile_name': logname})
    logger=logging.getLogger("BL32XU")

    lpfile=os.path.join(procpath,"XSCALE.LP")
    mgfile=os.path.join(procpath,"merging_stats.log")

    logger.info("Processing LPFILE %s\n"%lpfile)
    logger.info("%s\n" % mgfile)

    if os.path.exists(lpfile)==False:
        logger.info("%s does not exist" % lpfile)
        sys.exit()
    if os.path.exists(mgfile)==False:
        logger.info("%s does not exist" % mgfile)
        sys.exit()

    logger.info("AnaXSCALE starts")
    ac = AnaXSCALE.AnaXSCALE(lpfile)
    s1 = ac.makeStatsSeries()
    logger.info("AnaXSCALE %5d" % len(s1))

    logger.info("Merging stats.")
    pms = PhenixMergingStats.PhenixMergingStats(mgfile)
    s2 = pms.makeDataSeriesLog()
    logger.info("Merging %5d" % len(s2))

    logger.info("Merge two lines")
    s1["logname"] = lpfile
    s12 = pd.concat([s1,s2])
    logger.info("Merged data length= %5d" % len(s12))
    logger.info("Merged dataframe (XSCALE+phenix.merging...%s" % type(s12))

    d1 = pd.DataFrame([s12])

    return d1

n_file=0
for index, col in df.iterrows():
    filepath=col['procpath']
    dirlist=glob.glob("%s/*"%filepath)
    print(filepath)
    # For 'merging directories'
    for di in dirlist:
        if "merge" in di and "index" in di:
            # Intensity statistics data frame
            stats_df=ana_intensity_stats(di)

            # DM 100 cycle data frame
            phsdf_020=ana_phasing_result(di, "02.SAD_DM20", column="dm020")
            phsdf_100=ana_phasing_result(di, "00.SAD", column="dm100")

            newdf=pd.concat([phsdf_020, phsdf_100, stats_df],axis=1)

            if n_file==0:
                final_df=newdf
            else:
                final_df=pd.concat([final_df, newdf])
 
            # Number of data directories
            n_file+=1

final_df.to_csv(sys.argv[2], index=None)
