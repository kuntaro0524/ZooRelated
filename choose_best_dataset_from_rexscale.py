#!/usr/bin/env python
import pandas as pd
import glob, sys

filename = sys.argv[1]
file_list = glob.glob("*/%s"%filename)

isInitFlag=False
total_df=None

for each_file in file_list:
    each_df = pd.read_csv(each_file)
    each_df['dataname']=each_file
    if isInitFlag==False:
        total_df=each_df
        isInitFlag=True
    else:
        total_df = pd.concat([total_df, each_df])

# label check
total_df.columns
# Selection and Sort
total_df.sort_values('overall_cchalf', ascending=False)

# Selection (Overall CC(1/2) > 98.0)
select_cchalf = total_df['overall_cchalf'] > 98.0
select01 = total_df[select_cchalf]

# Sort and check
select01.sort_values('overall_isigi', ascending=False)

# output CSV files 
select01.to_csv("report.csv")
