'''
Created on Aug 30, 2019

@author: stevo
'''

import math
from difflib import SequenceMatcher


def CalcDistance(lat1, lon1, lat2, lon2):

    try:
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c
    except:
        distance = 20000.0

    return distance

def NormatizeSeaMarkId(name):
    name = name.replace(' ', '')

    length = len(name)
    if(length == 5):
        name += ".00"
    elif(length == 6):
        name += "00"
    elif(length == 7):
        name += "0"

    return name


def NormalizeSeaMarkname(name):
    name = name.replace(' ', '')
    try:
        while name[-1] is ".":
            name = name[:-1]
        while name[0] is "-":
            name = name[1:]
    except:
        # print("error NormalizeSeaMarkname: {}".format(name))
        pass

    return name


def SeaNameMatcher(osm_name, lol_name):
    osm_name=NormalizeSeaMarkname(osm_name)
    lol_name=NormalizeSeaMarkname(lol_name)
    if(osm_name is None or lol_name is None):
        return 0.0

    return SequenceMatcher(None, osm_name, lol_name).ratio()



class osmkey():
    key_seamark_light_character = "seamark:light:character"
    key_seamark_light_1_character = "seamark:light:1:character"
    key_seamark_type = "seamark:type"
    key_seamark_light_reference = "seamark:light:reference"
    key_seamark_name = "seamark:name"


class osmval():
    value_light_minor = "light_minor"
    value_light_major = "light_major"


class lolkey():
    key_LightFeature = "LightFeature"
    key_DGPSFeature = "DGPSFeature"
    key_RBFeature = "RBFeature"
    key_Latitude = "Latitude"
    key_Longitude = "Longitude"
    key_IntlNo = "IntlNo"
    key_AidNo = "AidNo"
    key_NameLocation = "NameLocation"
