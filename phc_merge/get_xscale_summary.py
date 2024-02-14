import os,sys
import AnaXSCALE2


xscale_lp_path=sys.argv[1]
xs2 = AnaXSCALE2.AnaXSCALE2(xscale_lp_path)

df = xs2.getDataFrame()
print(df)
