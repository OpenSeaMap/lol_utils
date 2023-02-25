'''
Created on Aug 27, 2019

@author: stevo
'''

import xml.dom.minidom
from xml.dom.minidom import Document
from utils.lol import Light
from utils.common import lolkey, osmkey, osmval, NormalizeSeaMarkname,\
    CalcDistance, NormatizeSeaMarkId


class osmdb():

    def __init__(self, filename):
        self.filename = filename
        self.seamark_type_cnt = 0
        self.seamark_type_light_minor_cnt = 0
        self.seamark_type_light_major_cnt = 0
        self.seamark_light_character_cnt = 0
        self.seamark_light_character_1_cnt = 0
        self.rm_cnt = 0
        self.lightlist = list()

        self._ParseLights()
        self._AnalyseData()

    def crosscheck(self, lol_data):
        self.check_cnt1 = 0
        self.check_cnt2 = 0
        self.check_cnt3 = 0
        self.check_cnt4 = 0

        out1 = ""
        out2 = ""
        out3 = ""
        out4 = ""

        # loop over all lights and create list with lights which are still present in osm and lol
        for osm_light in self.lightlist:
            ref = osm_light.GetProperty(osmkey.key_seamark_light_character)
            tmpres = lol_data.CheckRef(ref)
            if tmpres:
                lol_lat = tmpres.GetProperty(lolkey.key_Latitude)
                lol_lon = tmpres.GetProperty(lolkey.key_Longitude)
                # handling for lights which exists in both databases (osm and lol)
                out1 += "id: {}\n".format(osm_light.id)
                out1 += "  ref: {}\n".format(ref)
                out1 += "  name: {}\n".format(osm_light.GetProperty(osmkey.key_seamark_name))
                out1 += "  url: https://www.openstreetmap.org/node/{}\n".format(osm_light.id)
                out1 += "  position osm:{},{}\n".format(osm_light.lat, osm_light.lon)
                out1 += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(osm_light.lat, osm_light.lon,osm_light.lat, osm_light.lon)
                out1 += "  position lol:{},{}\n".format(lol_lat, lol_lon)
                out1 += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(lol_lat, lol_lon, lol_lat, lol_lon)
                out1 += "\n"
                self.check_cnt1 += 1

            elif ref:
                # handling for lights with exists in osm and have reference but cannot find in pubxxx
                out2 += "id: {}\n".format(osm_light.id)
                out2 += "  ref: {}\n".format(ref)
                out2 += "  name: {}\n".format(osm_light.GetProperty(osmkey.key_seamark_name))
                out2 += "  url: https://www.openstreetmap.org/node/{}\n".format(osm_light.id)
                out2 += "  position osm:{},{}\n".format(osm_light.lat, osm_light.lon)
                out2 += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(osm_light.lat, osm_light.lon,osm_light.lat, osm_light.lon)
                out2 += "\n"
                self.check_cnt2 += 1

            else:
                # handling for all other
                out3 += "id: {}\n".format(osm_light.id)
                out3 += "  name: {}\n".format(osm_light.GetProperty(osmkey.key_seamark_name))
                out3 += "  https://www.openstreetmap.org/node/{}\n".format(osm_light.id)
                out3 += "  position osm:{},{}\n".format(osm_light.lat, osm_light.lon)
                out3 += "    http://map.openseamap.org/?zoom=17&lat={}&lon={}&mlat={}&mlon={}&layers=0FTFFFFFFTFBFFFFFFFFFF\n".format(osm_light.lat, osm_light.lon,osm_light.lat, osm_light.lon)
                out3 += "\n"

                self.check_cnt3 += 1

        print("lights with reference in osm and lol")
        print("cnt={}".format(self.check_cnt1))
        print(out1)

        print("lights with reference in osm but no entry in lol")
        print("cnt={}".format(self.check_cnt2))
        print(out2)

        print("all other lights")
        print("cnt={}".format(self.check_cnt3))
        print(out3)

    def CheckRef(self, lol_light):

        lol_ref = lol_light.GetProperty(lolkey.key_IntlNo)
        lol_lat = lol_light.lat
        lol_lon = lol_light.lon

        # search for reference in LoL and return osm_light
        retv = None
        cand = None
        mindist=20000.0

        if lol_ref is not None:
            for osm_light in self.lightlist:
                osm_ref = osm_light.GetProperty(osmkey.key_seamark_light_reference)
                osm_name = osm_light.GetProperty(osmkey.key_seamark_name)

                if osm_ref:
                    osm_ref = NormatizeSeaMarkId(osm_ref)  # osm_ref.replace(' ', '')
                    lol_ref = NormatizeSeaMarkId(lol_ref)  # lol_ref.replace(' ', '')
                    if lol_ref.find(osm_ref) is 0:
                        # entry found
                        retv = osm_light
                        mindist = CalcDistance(osm_light.lat, osm_light.lon, lol_lat, lol_lon)
                        break

                dist = CalcDistance(osm_light.lat, osm_light.lon, lol_lat, lol_lon)
                if(mindist > dist):
                    mindist = dist
                    cand = osm_light

        if retv is None and cand is None:
            print("error: {}".format(lol_light.GetProperty(lolkey.key_IntlNo)))

        return retv, mindist, cand

    def _ParseLights(self):
        print("load osm file {}".format(self.filename))
        # Open XML document using minidom parser
        DOMTree = xml.dom.minidom.parse(self.filename)
        collection = DOMTree.documentElement

        # Get all the overpass-api-lights-planet.overpassql movies in the collection
        self.SeaMarkList = collection.getElementsByTagName("node")
        self.SeaMarkList += collection.getElementsByTagName("rel")
        self.SeaMarkList += collection.getElementsByTagName("way")

    def Write(self, filename):
        doc = Document()

        osm = doc.createElement("osm")
        osm.setAttribute("version", '0.6')

        for seamark in self.SeaMarkList:
            retv = seamark.getElementsByTagName('tag')
            if(len(retv) > 0):
                osm.appendChild(seamark)

        doc.appendChild(osm)

        doc.writexml(open(filename, 'w'),
                     indent="  ",
                     addindent="  ")
        doc.unlink()

    def _AnalyseData(self):
        print("analyse osm file {}, Elements: {}".format(self.filename, len(self.SeaMarkList)))
        for seamark in self.SeaMarkList:
            try:
                retv = seamark.getElementsByTagName('tag')
                is_light = False
                if(len(retv) > 0):
                    light = Light()
                    for tag in retv:
                        key = tag.getAttribute('k')
                        val = tag.getAttribute('v')
                        light.SetProperty(key, val)

                        if key.find(osmkey.key_seamark_light_character) != -1:
                            self.seamark_light_character_cnt += 1
                            is_light = True

                        if key.find(osmkey.key_seamark_light_1_character) != -1:
                            self.seamark_light_character_1_cnt += 1
                            is_light = True

                        if key.find(osmkey.key_seamark_type) != -1:
                            self.seamark_type_cnt += 1
                            if val.find(osmval.value_light_minor) != -1:
                                self.seamark_type_light_minor_cnt += 1
                                is_light = True
                            if val.find(osmval.value_light_major) != -1:
                                self.seamark_type_light_major_cnt += 1
                                is_light = True
                    if(is_light):
                        light.id = seamark.getAttribute("id")
                        try:
                            light.lat = float(seamark.getAttribute("lat"))
                            light.lon = float(seamark.getAttribute("lon"))
                        except:
                            light.lat = None
                            light.lon = None

                        self.lightlist.append(light)
                else:
                    self.rm_cnt += 1

            except:
                print("error")
                pass

