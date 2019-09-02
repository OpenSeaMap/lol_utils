'''
Created on Aug 27, 2019

@author: stevo
'''

from utils.osm import osmdb
from utils.common import osmval, osmkey
from utils.lol import LoL
from optparse import OptionParser


def AnalyseLoLFile(osm_filename, lol_filename_list):

    osm_data = osmdb(osm_filename)

    lol_data = LoL(lol_filename_list)
    lol_data.crosscheck(osm_data)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-o", "--osmfilename", dest="osm", default="./samples/osm/sample.osm", help="filename osm")
    parser.add_option("-l", "--lolfilename", dest="lol", default="./samples/LoL/sample.xml", help="filename lol")

    (options, args) = parser.parse_args()

    lol_filelist = options.lol.split(";")

    AnalyseLoLFile(options.osm, lol_filelist)

    print("ready")
