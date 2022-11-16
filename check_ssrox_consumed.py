import sys,os,glob
import datetime

allpath = glob.glob("./*")
datapath = []


def get_size_dir(path='.'):
    total_size = 0
    for dir_path in os.listdir(path):
        full_path = os.path.join(path, dir_path)
        if os.path.isfile(full_path):
            total_size += os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            total_size += get_size_dir(full_path)
    return total_size

def getNlines(sch_file_path):
    
    lines = open(sch_file_path, "r").readlines()
    
    found_flag=False
    for line in lines:
        comment="Raster Vertical Points:"
        if comment in line:
            found_flag = True
            nlines=int(line.split()[3])
    
    if found_flag:
        return(nlines)
    else:
        return(0)

for each_path in allpath:
    if os.path.isdir(each_path):
        if "HSK" in each_path:
            datapath.append(each_path)

for each_path in datapath:
    anadir = './%s/scan00/ssrox/' % each_path
    h5_files = glob.glob("%s/*h5"%anadir)

    file_list=[]

    for h5_file in h5_files:
        t = os.path.getmtime(h5_file)
        d = datetime.datetime.fromtimestamp(t)
        file_list.append((t,d,h5_file))

    if len(file_list) == 0:
        #print("This is 'multi data' %s" % each_path)
        continue

    # Get lines from schedule file
    filepath="%s/ssrox.sch" % anadir
    nlines=getNlines(filepath)

    # directory size
    fsize = get_size_dir(anadir)
    #print(anadir,fsize)

    # sort by 'time stamp'
    # The newest entry
    newest=sorted(file_list, key=lambda x:x[0])[0]
    oldest=sorted(file_list, key=lambda x:x[0],reverse=True)[0]
    
    #print(newest[1], oldest[1])
    minutes = (oldest[1]-newest[1]).seconds / 60.0
    print("%s,%d,%d,%s"%(anadir,nlines,minutes,fsize))

