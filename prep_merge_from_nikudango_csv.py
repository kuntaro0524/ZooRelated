import sys
import pandas as pd
import numpy 

if len(sys.argv) < 2:
    print("Usage: python prep_merge_from_nikudango_csv.py SAMPLE_NAME CSV_FILE1 CSV_FILE2 ....")
    sys.exit()

sample_name = sys.argv[1]
input_csvs = sys.argv[2:]

xdsstr=""

# output script name
output_name = "prep_merge.com"
ofile=open(output_name,"w")

for input_csv in input_csvs:
    print(input_csv)
    # Read csv from nikudango
    df = pd.read_csv(input_csv)

    # Selection of the target name
    #print(df['name'])

    
    select_flag = df['name'] == sample_name
    sel_df = df[select_flag]

    print(len(sel_df))
    
    for index,row in sel_df.iterrows():
        print(row['topdir'])
        xdsstr += "xdsdir=%s \\\n" % row['topdir']
        #print("INDEX:",index)

    #print(xdsstr)

header = """
#!/bin/csh
unset autologout
/oys/xtal/cctbx/snapshots/upstream/build/bin/yamtbx.python /oys/xtal/cctbx/snapshots/upstream/modules/yamtbx/dataproc/auto/command_line/multi_prep_merging.py \
%sworkdir=merge_manual\
""" % xdsstr

ofile.write(header)
ofile.close()
