#monster names
import os
import json

def generate_name_dict():
    jsondatabase = {}
    path = '../open5e/'
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(path+file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = list(jsondatabase.keys())
    names = {}
    for element in elementas:
        index = 0
        names[element] = []
        if "name" in jsondatabase[element][0]:
            for elementint in jsondatabase[element]:
                names[element].append(elementint["name"])
                index+=1
    with open("./namelist.json","w+") as namefile:
        json.dump(names,namefile,sort_keys=True,indent=4, separators=(',', ': '))
