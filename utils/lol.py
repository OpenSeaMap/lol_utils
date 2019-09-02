'''
Created on Aug 27, 2019

@author: stevo
'''

import xml.dom.minidom
from utils.common import CalcDistance, SeaNameMatcher
from utils.common import osmkey, lolkey


class Light():
    def __init__(self):
        self.properties = dict()
        pass

    def GetProperty(self, key):
        try:
            retv = self.properties[key]
        except:
            retv = None

        return retv

    def SetProperty(self, key, val):
        self.properties[key] = val


class LightGroup():
        val1 = 0
        val2 = 1
        val3 = 2
        val4 = 3
        val5 = 4


class LightMetaData():
    def __init__(self, lol_light, osm_light, mindist, cand):
        self.lol_light = lol_light

        self.link = False
        self.NameMatchValue = 0.0
        self.Distance = mindist

        if osm_light:
            self.osm_light = osm_light
            self.link = True
            self.group = LightGroup.val1
        else:
            self.osm_light = cand
            self.link = False

        osm_name = self.osm_light.GetProperty(osmkey.key_seamark_name)
        lol_name = self.lol_light.GetProperty(lolkey.key_NameLocation)
        if(osm_name):
            self.NameMatchValue = SeaNameMatcher(osm_name, lol_name)
        else:
            self.NameMatchValue = 0

        self.lol_ref_int = lol_light.GetProperty(lolkey.key_IntlNo)
        self.lol_ref_aid = lol_light.GetProperty(lolkey.key_AidNo)

        if self.link is False:
            # identify candidates with matching name and Position +/- 200m (manual merge needed)
            if(self.NameMatchValue > 0.99 and mindist < 0.2):
                self.group = LightGroup.val2

            # identify candidates with matching position +/- 100m (merge procedure needed)
            elif mindist < 0.1:
                self.group = LightGroup.val3

            # identify candidates without other light in distance > 2000m (import )
            elif mindist > 2:
                self.group = LightGroup.val4

            # all others (further investigations needed)
            else:
                self.group = LightGroup.val5


class LoL():

    def __init__(self, filenamelist):
        self.lol = list()
        self.rb = list()
        self.dgps = list()

        self.filenamelist = filenamelist
        self.LightFeature_cnt = 0
        self.DGPS_Feature_cnt = 0
        self.RB_Feature_cnt = 0
        self._ParseLights()

    def crosscheck(self, osm_data):
        print("start cross check of lol database with osm database\n")

        self.lightdatalist = list()

        # search all seamarks from lol which are not exists in osm
        cnt = len(osm_data.lightlist)

        # loop over entrys in lol db
        for lol_light in self.lol:

            # search reference in osm db
            osm_light, mindist, cand = osm_data.CheckRef(lol_light)

            if(osm_light is None and cand is None):
                print("error: {}".format(lol_light.GetProperty(lolkey.key_IntlNo)))
            else:
                self.lightdatalist.append(LightMetaData(lol_light, osm_light, mindist, cand ))

        osm_light = None
        mindist = None
        cand = None

        # generate report
        groupcnt = [0, 0, 0, 0, 0]
        outbuff = ["", "", "", "", ""]
        lightgroup = [LightGroup.val1,
                      LightGroup.val2,
                      LightGroup.val3,
                      LightGroup.val4,
                      LightGroup.val5]

        for lightdata in self.lightdatalist:
            groupcnt[lightdata.group]+=1

        # prepare report header
        # for group in lightgroup:
        #    outbuff[group] = "report for lights in group = {}\n".format(groupcnt[group]+1)

        # print details for each entry
        for lightdata in self.lightdatalist:

            lol_light = lightdata.lol_light
            lol_ref_int = lol_light.GetProperty(lolkey.key_IntlNo)
            lol_ref_aid = lol_light.GetProperty(lolkey.key_AidNo)
            lol_lat = lol_light.lat
            lol_lon = lol_light.lon
            lol_name = lol_light.GetProperty(lolkey.key_NameLocation)

            osm_light = lightdata.osm_light
            osm_ref = osm_light.GetProperty(osmkey.key_seamark_light_reference)
            osm_name = osm_light.GetProperty(osmkey.key_seamark_name)
            osm_lat = osm_light.lat
            osm_lon = osm_light.lon

            outbuff[lightdata.group] += "ref int: {}\n".format(lol_ref_int)
            outbuff[lightdata.group] += "ref us: {}\n".format(lol_ref_aid)
            outbuff[lightdata.group] += "  name: {}\n".format(lol_name)
            outbuff[lightdata.group] += "  position lol:{},{}\n".format(lol_light.lat, lol_lon)
            outbuff[lightdata.group] += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(lol_lat, lol_lon, lol_lat, lol_lon)
            outbuff[lightdata.group] += "    https://www.openstreetmap.org/#map=18/{}/{}\n".format(lol_lat, lol_lon)
            outbuff[lightdata.group] += "  id (osm): {}\n".format(osm_light.id)
            outbuff[lightdata.group] += "  ref (osm): {}\n".format(osm_ref)
            outbuff[lightdata.group] += "  name (osm): {}\n".format(osm_name)
            outbuff[lightdata.group] += "    https://www.openstreetmap.org/node/{}\n".format(osm_light.id)
            outbuff[lightdata.group] += "  position osm:{},{}\n".format(osm_lat, osm_lon)
            outbuff[lightdata.group] += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(osm_lat, osm_lon, osm_lat, osm_lon)
            outbuff[lightdata.group] += "    https://www.openstreetmap.org/#map=18/{}/{}\n".format(osm_lat, osm_lon)
            outbuff[lightdata.group] += "  quality info:\n"
            outbuff[lightdata.group] += "    distance: {}\n".format(lightdata.Distance)
            outbuff[lightdata.group] += "    namematch: {}\n".format(lightdata.NameMatchValue)
            outbuff[lightdata.group] += "    group: {}\n".format(lightdata.group+1)
            outbuff[lightdata.group] += "    link: {}\n".format(lightdata.link)
            outbuff[lightdata.group] += "\n"

        # prepare report header
        print("report summary")
        for group in lightgroup:
            print("  number of element in group {} = {}".format(group+1, groupcnt[group]))

        print("\n")
        print("1 - lights with matching int reference")
        print("2 - lights with matching name and position +/- 200m")
        print("3 - lights with matching position +/- 100m")
        print("4 - lights without other lights in distance < 2000m")
        print("5 - all other \n")
        print("\n")

        for group in lightgroup:
            print("detailed report for group {}\n{}\n".format(group+1, outbuff[group]))


    def CheckRef(self, value):
        # search for reference in LoL and return data
        retv = None

        if value is not None:
            value = value.replace(' ', '')
            for entry in self.lol:
                ref = entry.GetProperty(lolkey.key_IntlNo)
                if ref and ref.find(value) is 0:
                    # entry found
                    retv = entry
                    break

        return retv

    def _GetElementText(self, element, name):
        try:
            retv = element.getElementsByTagName(name)[0].firstChild.data
        except:
            retv = None
        return retv

    def _ParseLights(self):

        for filename in self.filenamelist:
            print("analyse lol file {}".format(filename))
            # Open XML document using minidom parser
            DOMTree = xml.dom.minidom.parse(filename)
            collection = DOMTree.documentElement

            LightFeatures = collection.getElementsByTagName(lolkey.key_LightFeature)
            print("analyse lol file {}, Elements: {}".format(filename, len(LightFeatures)))
            for LightFeature in LightFeatures:

                light = Light()
                nodeList = LightFeature.getElementsByTagName("*")
                for t in nodeList:
                    key = t.tagName
                    try:
                        val = t.firstChild.data
                    except:
                        val = ""
                    light.SetProperty(key, val)
                    try:
                        light.lon = float(light.GetProperty(lolkey.key_Longitude))
                        light.lat = float(light.GetProperty(lolkey.key_Latitude))
                    except:
                        light.lon = None
                        light.lat = None
                self.lol.append(light)
            self.LightFeature_cnt += len(LightFeatures)

            DGPSFeature = collection.getElementsByTagName(lolkey.key_DGPSFeature)
            self.DGPS_Feature_cnt += len(DGPSFeature)

            RBFeature = collection.getElementsByTagName(lolkey.key_RBFeature)
            self.RB_Feature_cnt += len(RBFeature)
