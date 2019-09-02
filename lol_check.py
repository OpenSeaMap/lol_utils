'''
Created on Aug 27, 2019

@author: stevo
'''

from utils.lol import LoL, lolkey


samplefilename = "./downloads/LoL/Pub114.xml"
samplefilename = "./samples/LoL/sample.xml"


def AnalyseLoLFile(infilename):
    data = LoL(infilename)
    print("##########################################################")
    print("statistic lol database")
    print("file: {}".format(infilename))
    print("number of Lights (key={} val={}) = {}".format(lolkey.key_LightFeature, "*", data.LightFeature_cnt))
    print("number of RadioBeacons (key={} val={}) = {}".format(lolkey.key_RBFeature, "*", data.DGPS_Feature_cnt))
    print("number of DiffGPS (key={} val={}) = {}".format(lolkey.key_DGPSFeature, "*", data.RB_Feature_cnt))
    print("")


if __name__ == "__main__":
    #AnalyseLoLFile(["./samples/LoL/sample.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub110.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub111.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub112.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub113.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub114.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub115.xml"])
    AnalyseLoLFile(["./downloads/LoL/Pub116.xml"])
