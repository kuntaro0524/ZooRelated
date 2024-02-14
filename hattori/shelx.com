#!/bin/bash
shelxc sad <<EOF | tee shelxc.log
SAD ../xscale.hkl
CELL 57.44    83.29    98.62  90.000  90.000  90.000
SPAG C222
FIND 9
NTRY 1000
EOF

shelxd sad_fa | tee shelxd.log
shelxe sad sad_fa -h -s0.6 -m200 -a3| tee shelxe.log
shelxe sad sad_fa -h -s0.6 -m200 -i -a3 | tee shelxe_i.log
