#!/bin/bash
  phaser << eof > $PROCPATH/info_gain.log
  TITLe beta blip automatic
  MODE MR_AUTO
  HKLIn $FREEMTZ
  LABIn I=IMEAN SIGI=SIGIMEAN
  ENSEmble maru PDB $FINAL_PDB IDENtity 100
  SEARch ENSEmble maru NUM 1
  ROOT ./ # not the default
  INFO ON
  eof

