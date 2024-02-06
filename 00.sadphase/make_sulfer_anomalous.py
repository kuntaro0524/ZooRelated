#!/usr/bin/env python
import os,sys

sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs")
import AnaLog

if __name__ == "__main__":
    # proc path
    proc_path=sys.argv[1]

    anode_path=os.path.join(proc_path, "anode.log")
    al=AnaLog.AnaLog(anode_path)
    al.readFile()

    def find_atom(series, atom_type="S"):
        comma_divs=series['NearAtom'].split(":")

        tmp_atom_type=comma_divs[0][0]
        tmp_res_type=comma_divs[1][0:3]
        tmp_res_num=comma_divs[1][3:]

        if tmp_atom_type==atom_type:
            return(tmp_atom_type, tmp_res_type, tmp_res_num)
        return(None)

    import pandas as pd

    cols1=(al.sandwitchReading("Averaged anomalous densities (sigma)", "Strongest unique anomalous peaks"))
    cols2=(al.sandwitchReading("X        Y        Z   Height(sig)  SOF     Nearest atom","Peaks output to file"))

    index=["dummy","X","Y","Z","Height","sig","SOF","NearAtom"]

    df=pd.DataFrame(cols2)
    df.columns=index
    # Convert column type
    df[['X', 'Y', "Z", "Height", "sig", "SOF"]]=df[['X', 'Y', "Z", "Height", "sig", "SOF"]].astype(float)
    
    s_df_array=[]
    for index, each_row in df.iterrows():
        s_atoms=find_atom(each_row, atom_type="S")
        s_index=0
        if s_atoms is not None:
            atom_type, res_type, res_num = s_atoms
            s_index_char="S%02d" % s_index
            each_row[s_index_char]=s_index
            each_row['res_type']=res_type
            each_row['res_num']=res_num
            s_df_array.append(each_row)
            s_index+=1
        
    # if sulfers are not contained.
    if len(s_df_array)!=0:
        s_df=pd.DataFrame(s_df_array)
    else:
        print("This data does not include ")
        sys.exit()

    final_dic={}
    for res_type, each_df in s_df.groupby('res_type'):
        print("EACH_DF", each_df)
        mean_height=each_df['Height'].mean()
        mean_dist=each_df['SOF'].mean()
        n_data=len(each_df)
        height_name="%s_mean_height" % res_type
        ndata_name="%s_n_data" % res_type
        dist_label="%s_mean_dist" % res_type
    
        final_dic[height_name]=mean_height
        final_dic[ndata_name]=n_data
        final_dic[dist_label]=mean_dist
    
    # if final_dic has a size
    print("FINAL_DIC=",len(final_dic))
    if len(final_dic)!=0:
        final_df=pd.DataFrame.from_dict([final_dic])
        # S anomalous data csv
        csv_path=os.path.join(proc_path, "cysmet.csv")
        final_df.to_csv(csv_path, index=False)
