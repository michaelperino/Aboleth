#dnd runner
from PIL import ImageFont,Image,ImageDraw
import pprint
import os
import json

monsters = "5e-SRD-Monsters.json"
skilldoc = "5e-SRD-Ability-Scores.json"
cardfile = "./images/cardlayout.json"

def main():
    jsondatabase = {}
    path = '../open5e/'
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(path+file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = jsondatabase.keys()
    skills = []
    cardlayout = None
    if os.path.exists(cardfile):
        with open(cardfile,'r') as f:
            cardlayout = json.load(f)
    else:
        print('ERROR: No card layout detected. Unable to create stat cards.')
    for element in jsondatabase[skilldoc]:
        skills.append([])
        skills[-1].append(element["full_name"])
        skills[-1].append(element["name"])
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
                        print('%13s%5d'%(skill[1], (element[skill[0].lower()])))
                        if cardlayout != None:
                            skilldraw(cardplt,element[skill[0].lower()],skill,cardlayout)
                    topfielddraw(cardplt,element,cardlayout)
                    card.save('./images/updated.png')
def skilldraw(image,stat,statname,cardlayout):
    colorMod = cardlayout["MODfont"]["color"]
    colorRawScore = cardlayout["RAWSCOREfont"]["color"]
    fontMod = ImageFont.truetype(cardlayout["MODfont"]["font"],size=int(cardlayout["MODfont"]["size"]))
    fontRawScore = ImageFont.truetype(cardlayout["RAWSCOREfont"]["font"],size=int(cardlayout["RAWSCOREfont"]["size"]))
    for element in cardlayout["MOD"]:
        if element["name"] == statname[0]:
            mod = "{0:+.0f}".format((stat-10)/2 - ((stat-10)/2)%1)
            (x,y,xs,ys) = (element['x'],element['y'],element['xs'],element['ys'])
            size = fontMod.getsize(str(mod))        
    image.text((x+xs/2-size[0]/2,y+ys/2-size[1]/2),str(mod),fill=colorMod,font=fontMod)
    for element in cardlayout["RAWSCORE"]:
        if element["name"] == statname[0]:
            mod = int(stat)
            (x,y,xs,ys) = (element['x'],element['y'],element['xs'],element['ys'])
            size = fontRawScore.getsize(str(mod))        
    image.text((x+xs/2-size[0]/2,y+ys/2-size[1]/2),str(mod),fill=colorRawScore,font=fontRawScore)

def topfielddraw(image,monsterdata,cardlayout):
    name = monsterdata["name"]
    comrate = monsterdata["challenge_rating"]
    element = cardlayout["MONSTNAMEfont"]
    colorName = element["color"]
    fontName = ImageFont.truetype(element["font"],size=int(element["size"]))
    element = cardlayout["MONSTNAME"]
    size = fontName.getsize(name)   
    (x,y,xs,ys) = (element['x'],element['y'],element['xs'],element['ys'])
    image.text((x,y+ys/2-size[1]/2),name,fill=colorName,font=fontName)

    element = cardlayout["COMBATRATINGfont"]
    colorCR = element["color"]
    fontCR = ImageFont.truetype(element["font"],size=int(element["size"]))
    element = cardlayout["COMBATRATING"]
    (x,y,xs,ys) = (element['x'],element['y'],element['xs'],element['ys'])
    size = fontCR.getsize(str(comrate))        
    image.text((x+xs/2-size[0]/2,y+ys/2-size[1]/2),str(comrate),fill=colorCR,font=fontCR)

main()
