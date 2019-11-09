# monster names
import os
import json


def generate_name_dict():
    jsondatabase = {}
    path = '../open5e/'
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(path + file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = list(jsondatabase.keys())
    names = {}
    for element in elementas:
        names[element] = []
        for elementint in jsondatabase[element]:
            if "name" in elementint:
                names[element].append(elementint["name"])
    with open("./namelist.json", "w+") as namefile:
        json.dump(names, namefile, sort_keys=True, indent=4, separators=(',', ': '))