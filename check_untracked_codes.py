import os,math,glob
import subprocess

#file_list1 = glob.glob("*.py")
#file_list2 = glob.glob("Libs/*.py")

def do(command="TEST"):
    output = subprocess.check_output([command],shell=True)
    lines = output.split("\n")
    icount = 0
    for line in lines:
        if line.endswith(".py") and line.rfind("deleted")==-1:
            print(line)
            cols = line.split()

do("git status")
