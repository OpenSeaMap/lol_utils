'''
Created on Aug 27, 2019

@author: stevo
'''

from utils.osm import osmdb, osmval, osmkey


def AnalyseOsmFile(infilename, outfilename):
    data = osmdb(infilename)
    print("##########################################################")
    print("statistic osm database")
    print("file: {}".format(infilename))
    print("number of seamarks (key={} val={}) = {}".format(osmkey.key_seamark_type, "*", data.seamark_type_cnt))
    print("number of seamarks (key={} val={}) = {}".format(osmkey.key_seamark_light_character, "*", data.seamark_light_character_cnt))
    print("number of seamarks (key={} val={}) = {}".format(osmkey.key_seamark_light_1_character, "*", data.seamark_light_character_1_cnt))
    print("number of seamarks (key={} val={}) = {}".format(osmkey.key_seamark_type, osmval.value_light_major, data.seamark_type_light_major_cnt))
    print("number of seamarks (key={} val={}) = {}".format(osmkey.key_seamark_type, osmval.value_light_minor, data.seamark_type_light_minor_cnt))
    print("")


if __name__ == "__main__":
    AnalyseOsmFile("./samples/osm/sample.osm", "results/sample.osm")
    AnalyseOsmFile("./downloads/osm/lights-planet.osm", "results/lights-planet.osm")
    AnalyseOsmFile("./downloads/osm/seamarks-planet.osm", "results/seamarks-planet.osm")

    print("ready")
