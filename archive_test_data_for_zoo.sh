#!/bin/bash

# crystal pictures
filelist="logtest.lst"
find . -name '*ppm' >> $filelist
find . -name '*jpg' >> $filelist
find . -name 'summary.dat'>> $filelist
find . -name 'shika.db'>> $filelist
find . -name '*log'>> $filelist
find . -name '*html'>> $filelist
find . -name 'CORRECT.LP'>> $filelist
find . -name 'XSCALE.LP'>> $filelist
find . -name 'XSCALE.INP'>> $filelist
find . -name '*sch'>> $filelist
find . -name '*png'>> $filelist
find . -name '*css'>> $filelist
find . -name '*js'>> $filelist

tar cvfz arc.tgz -T $filelist
