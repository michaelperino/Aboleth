# dnd runner
from PIL import ImageFont, Image, ImageDraw
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
            with open(path + file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = jsondatabase.keys()
    skills = [[], []]
    cardlayout = None
    if os.path.exists(cardfile):
        with open(cardfile, 'r') as f:
            cardlayout = json.load(f)
    else:
        print('ERROR: No card layout detected. Unable to create stat cards.')
    for element in jsondatabase[skilldoc]:
        skills[0].append(element["full_name"])
        skills[1].append(element["name"])
    while True:
        stype = input()
        query = input()
        if stype == "stats" or stype == "stat":
            for element in jsondatabase[monsters]:
                if element["name"] == query:
                    # pprint.pprint(element, indent=2)
                    card = Image.open('./images/basecard.png')
                    cardplt = ImageDraw.Draw(card)
                    carddraw(cardplt, cardlayout, element, skills)
                    card.save('./images/updated.png')


def carddraw(image, cardlayout, monsterdata, skills):
    for element in cardlayout:
        element = cardlayout[element]
        font = element["font"]["font"]
        color = element["font"]["color"]
        size = element["font"]["size"]
        al = element["font"]["align"]
        font = ImageFont.truetype(font, size=int(size))
        count = 0
        print(monsterdata)
        for elementint in element["elements"]:
            print(elementint)
            x = monsterdata[elementint["name"].lower()]
            print(x)
            if "modifier" in element:
                x = str(eval(element["modifier"])).split('Â')[-1]
            (xp, y, xs, ys) = (elementint['x'], elementint['y'], elementint['xs'], elementint['ys'])
            size = font.getsize(str(x))
            if al == "c":
                xp += xs / 2 - size[0] / 2
            if al == "l":
                xp = xp
            if al == "r":
                xp += -xs / 2 + size[0] / 2
            image.text((xp, y + ys / 2 - size[1] / 2), str(x), fill=color, font=font)
            count += 1


main()
