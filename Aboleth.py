#dnd runner
from PIL import ImageFont,Image,ImageDraw
import pprint
import os
import json

monsters = "5e-SRD-Monsters.json"
skilldoc = "5e-SRD-Ability-Scores.json"

def main():
    jsondatabase = {}
    path = '../open5e/'
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(path+file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = jsondatabase.keys()
    skills = []
    for element in jsondatabase[skilldoc]:
        skills.append(element["full_name"])
    while True:
        stype = input()
        query = input()
        if stype == "stats" or stype == "stat":
            for element in jsondatabase[monsters]:
                if element["name"] == query:
                    #pprint.pprint(element, indent=2)
                    card = Image.open('./images/basecard.png')
                    cardplt = ImageDraw.Draw(card)
                    for skill in skills:
                        print('%13s%5d'%(skill, (element[skill.lower()])))
                        skilldraw(cardplt,element[skill.lower()],skills.index(skill))
                    card.save('./images/updated.png')
def skilldraw(image,stat,index):
    font = ImageFont.truetype('arial.ttf',size=75)
    if(abs(stat/10) < 1):
        (x,y)=(490+index*288,885)
    else:
        (x,y)=(467+index*288,885)
    color = 'rgb(0,0,0)'
    image.text((x,y),str(stat),fill=color,font=font)
    font = ImageFont.truetype('arial.ttf',size=125)
    stat = int((stat-10)/2)
    if(stat < 0):
        (x,y)=(455+index*288,715)
    else:
        (x,y)=(478+index*288,715)
    image.text((x,y),str(stat),fill=color,font=font)
main()

                
                
