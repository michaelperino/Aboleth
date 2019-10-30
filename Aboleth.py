#dnd runner
from PIL import ImageFont,Image,ImageDraw
import pprint
import os
import json
def main():
    jsondatabase = {}
    path = '../open5e/'
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
        if stype == "stats" or stype == "stat":
            for element in jsondatabase["5e-SRD-Monsters.json"]:
                if element["name"] == query:
                    skills = ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma']
                    pprint.pprint(element, indent=2)
                    card = Image.open('./images/basecard.png')
                    cardplt = ImageDraw.Draw(card)
                    for skill in skills:
                        print('%13s%5d'%(skill, (element[skill.lower()])))
                        skilldraw(cardplt,element[skill.lower()],skills.index(skill))
                    card.save('./images/updated.png')
def skilldraw(image,stat,index):
    font = ImageFont.truetype('arial.ttf',size=75)
    if(abs(stat/10) < 1):
        (x,y)=(487+index*288,885)
    else:
        (x,y)=(467+index*288,885)
    color = 'rgb(0,0,0)'
    image.text((x,y),str(stat),fill=color,font=font)

main()

                
                
