'''
Created on Aug 27, 2019

@author: stevo
'''

from utils.osm import osmdb, osmval, osmkey
from utils.lol import LoL


def AnalyseOsmFile(osm_filename, lol_filename_list):

    print("load osm file {}".format(osm_filename))
    osm_data = osmdb(osm_filename)

    lol_data = LoL(lol_filename_list)

    print("start cross of osm database the lol database")
    osm_data.crosscheck(lol_data)


if __name__ == "__main__":

    # AnalyseOsmFile("./samples/osm/sample.osm",["./samples/LoL/sample.xml"])

    AnalyseOsmFile("./downloads/osm/seamarks-planet.osm",  # ./downloads/osm/lights-planet.osm",
                   ["./downloads/LoL/Pub110.xml",
                    "./downloads/LoL/Pub111.xml",
                    "./downloads/LoL/Pub112.xml",
                    "./downloads/LoL/Pub113.xml",
                    "./downloads/LoL/Pub114.xml",
                    "./downloads/LoL/Pub115.xml",
                    "./downloads/LoL/Pub116.xml"
                    ])
    print("ready")
