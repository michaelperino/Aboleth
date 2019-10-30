#dnd runner
import pprint
import os
import json
import tabulate
jsondatabase = {}
path = 'K:\\dnd\\5e\\open5e\\'
for file in os.listdir(path):
    if file.endswith(".json"):
        with open(path+file, 'r') as f:
            jsondatabase[file] = json.load(f)
elementas = jsondatabase.keys()
print(list(elementas))
print(list(elementas)[0])
#print(jsondatabase['5e-SRD-StartingEquipment.json'])
while True:
    stype = input()
    query = input()
    if stype == "name":
        for element in jsondatabase["5e-SRD-Monsters.json"]:
            if element["name"] == query:
                skills = ['Strength',
                print(tabulate([[
                pprint.pprint(element, indent=2)
