#!/bin/bash
while read filepath
do
WD=$filepath sh ./test.sh
done < $1
