import os,sys
import pandas as pd

df = pd.read_csv(sys.argv[1])

n_pins=0
for pinid in df['pinid']:
    cols=(pinid.split('-'))
    if len(cols)==2:
        nth_smaller = int(cols[0])
        nth_larger = int(cols[1])
        n_pins += nth_larger - nth_smaller +1
        
    else:
        #print("Single")
        n_pins +=1

print("Total number of pins for data collection: %5d" % n_pins)
        
