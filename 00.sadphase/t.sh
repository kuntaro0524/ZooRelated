#!/bin/bash
while read filepath
do
echo $filepath
wd=$filepath sh test.sh
done < proc_path.lst
