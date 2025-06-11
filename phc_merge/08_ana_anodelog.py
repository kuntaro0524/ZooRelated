import os,sys

filepath=sys.argv[1]

directory_path = os.path.dirname(os.path.abspath(filepath))

if os.path.exists(filepath)==False:
    print("File not found")
    sys.exit()

else:
    outfile=os.path.join(directory_path,"anode.csv")
    ofile=open(outfile,"w")
    lines=open(filepath,"r").readlines()
    ofile.write("name,peak_height\n")

    isFound=False
    for line in lines:
        if "MET124" in line:
            cols = line.split()
            if cols[0].rfind("S")!=-1:
                value=float(cols[4])
                ofile.write("%s,%8.3f\n"%(directory_path,value))
                isFound=True

    if isFound==False:
        ofile.write("No peaks")

    ofile.close()
