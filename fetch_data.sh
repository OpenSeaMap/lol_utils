#!/bin/bash

wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub110/Pub110.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub111/Pub111.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub112/Pub112.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub113/Pub113.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub114/Pub114.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub115/Pub115.xml
wget -N -O downloads/LoL https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub116/Pub116.xml

## get extract of current osm seamarks
wget -O downloads/osm/seamarks-planet.osm  --timeout=600 --post-file=./query/overpass-api-planet.ql        "http://overpass-api.de/api/interpreter"

