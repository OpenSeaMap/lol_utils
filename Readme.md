This Project includes some scripts and instructions how to compare lights listed in "NGA List of Lights" with 
lights stored in osm database.

# Prepare Analysis

## download NGA documents

	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub110/Pub110.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub111/Pub111.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub112/Pub112.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub113/Pub113.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub114/Pub114.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub115/Pub115.xml
	wget https://msi.nga.mil/MSISiteContent/StaticFiles/NAV_PUBS/NIMA_LOL/Pub116/Pub116.xml

## get extract of current osm seamarks
    wget -O downloads/osm/seamarks-planet.osm  --timeout=600 --post-file=./query/overpass-api-planet.overpassql        "http://overpass-api.de/api/interpreter"

## get extract of current osm seamarks (only lights)
    wget -O downloads/osm/lights-planet.osm    --timeout=600 --post-file=./query/overpass-api-lights-planet.overpassql "http://overpass-api.de/api/interpreter"


# Bookmarks:
	 https://wiki.openstreetmap.org/wiki/OpenSeaMap/List_of_Lights_Import#Data_Source
	 https://wiki.openstreetmap.org/wiki/Key:seamark:fixme
