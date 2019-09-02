#!/bin/bash

DATE=date
DIRECTORY="reports"

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

time python3 crosscheck_osm.py > $DIRECTORY/cross_check_osm.log
