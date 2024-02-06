import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

if len(sys.argv)==3:
    n_dm=int(sys.argv[2])
elif len(sys.argv)==4:
    n_dm=int(sys.argv[2])
    build_cycle=int(sys.argv[3])
else:
    n_dm=20

df['prefix']="ssad"
df['space_group']="P43212"
df['anom_atom']="S"
df['n_anom']=8
df['solv_cnt']=0.4
df['build_cycle']=build_cycle
df['n_dm']=n_dm

df.to_csv("oden_prep.csv", index=False)
# prefix,hkl_file,cell_params,space_group,anom_atom,n_anom,n_try,phase_dmax,solv_cnt,n_dm,build_cycle,dmin
