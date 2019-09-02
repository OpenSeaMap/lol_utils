#!/bin/bash

set -x 

DATE=date
DIRECTORY="reports"

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub110.xml > $DIRECTORY/cross_check_lol_pub110.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub111.xml > $DIRECTORY/cross_check_lol_pub111.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub112.xml > $DIRECTORY/cross_check_lol_pub112.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub113.xml > $DIRECTORY/cross_check_lol_pub113.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub114.xml > $DIRECTORY/cross_check_lol_pub114.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub115.xml > $DIRECTORY/cross_check_lol_pub115.log
time python3 crosscheck_lol.py -o ./downloads/osm/seamarks-planet.osm -l ./downloads/LoL/Pub116.xml > $DIRECTORY/cross_check_lol_pub116.log
