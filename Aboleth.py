# dnd runner
from PIL import ImageFont, Image, ImageDraw
import pprint
import os
import json
from Spellcheck import spellcheck

monsters = ["5e-SRD-Monsters.json", "Great-DND5e-Monster-Spreadsheet.json", "Great-DND5e-Monster-Spreadsheet-Homebrew.json"]
skilldoc = "5e-SRD-Ability-Scores.json"
cardfile = "./images/cardlayout.json"

jsondatabase = {}

def main():
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
    print('Monster list?')
    count = 0
    for element in monsters:
        print(str(count) + ': ' + element)
        count += 1
    chosenlist = '-1'
    while chosenlist.isnumeric() == False or int(chosenlist) not in range(0, len(monsters)):
        chosenlist = input()
    print('Type "back" to choose a different monster list')
    monsterList = monsters[int(chosenlist)]
    inputneeded = True
    while True:
        if inputneeded:
            stype = input()
            if stype == "back":
                break
            query = input()
            if query == "back":
                break
        else:
            inputneeded = True
        if stype == "stats" or stype == "stat":
            found = False
            for element in jsondatabase[monsterList]:
                if element["name"].lower() == query.lower():
                    # pprint.pprint(element, indent=2)
                    print('Done. Your ' + element['name'] + ' card is ready, here are the raw stats anyway.')
                    card = Image.open('./images/basecard.png')
                    cardplt = ImageDraw.Draw(card)
                    carddraw(cardplt, cardlayout, element, skills)
                    card.save('./images/updated.png')
                    found = True
                    for i in range(0,len(skills[0])):
                        print(skills[1][i] + ' ' + str(element[str(skills[0][i]).lower()]))
            if not found:
                print("Didn't see it, did you mean...")
                intended = spellcheck(query, path, monsterList)
                if intended is not None:
                    stype = "stat"
                    query = intended
                    inputneeded = False

    main()


def carddraw(image, cardlayout, monsterdata, skills):
    for element in cardlayout:
        element = cardlayout[element]
        font = element["font"]["font"]
        color = element["font"]["color"]
        size = element["font"]["size"]
        al = element["font"]["align"]
        font = ImageFont.truetype(font, size=int(size))
        count = 0
        for elementint in element["elements"]:
            x = monsterdata[elementint["name"].lower()]
            if x == 'TEMP':
                break
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
