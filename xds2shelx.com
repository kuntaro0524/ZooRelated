#!/bin/bash
yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/xds/command_line/xds2shelx.py $1
