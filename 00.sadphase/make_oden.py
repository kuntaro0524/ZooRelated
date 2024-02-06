# 2020/12/09 ver0.00 prep_oden.py
# make 'oden_prep.csv'

import sys
import os
import glob
import numpy
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/nabe/oden")
sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs/")
import DirectoryProc # currently not used
import ComRefine
import ResolutionFromXscaleHKL # currently not used
import NabeMaster
import ODEN
#import AnaXSCALE

if __name__ == "__main__":
    nm = NabeMaster.NabeMaster()
    if len(sys.argv) == 3:
        oden_dir_name = sys.argv[1]
        nm.make_oden(oden_dir=oden_dir_name, thorough=True)
    elif len(sys.argv) == 2:
        oden_dir_name = sys.argv[1]
        nm.make_oden(oden_dir=oden_dir_name)
    else:
        nm.make_oden()
