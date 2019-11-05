# dnd runner
from PIL import ImageFont, Image, ImageDraw
import pprint
import os
import json
from Spellcheck import spellcheck

monsters = ["5e-SRD-Monsters.json", "Great-DND5e-Monster-Spreadsheet.json",
            "Great-DND5e-Monster-Spreadsheet-Homebrew.json", "players.json", "custom_monsters.json"]
skilldoc = "5e-SRD-Ability-Scores.json"
cardfile = "./images/cardlayout.json"
path = '../open5e/'

jsondatabase = {}
attributes = [[], []]
cardlayout = None
if os.path.exists(cardfile):
    with open(cardfile, 'r') as f:
        cardlayout = json.load(f)
else:
    print('ERROR: No card layout detected. Unable to create stat cards.')


def main():
    path = '../open5e/'
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(path + file, 'r') as f:
                jsondatabase[file] = json.load(f)
    elementas = jsondatabase.keys()
    for element in jsondatabase[skilldoc]:
        attributes[0].append(element["full_name"])
        attributes[1].append(element["name"])
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
    while True:
        stype = input().lower()
        if stype == "back":
            break
        else:
            inputneeded = True
        if stype == "stats" or stype == "stat":
            monstAttribs = stats("", monsterList, True)
            if monstAttribs is not None:
                for i in range(0, len(monstAttribs[1])):
                    print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(monstAttribs[2][i])) + '\t\t' + str(
                        monstAttribs[1][i]))
        if stype == "enounter":
            runencounter()
        if stype == "addplayer":
            addplayer()
    main()


def addplayer():
    newplayer = {}
    print("Please provide the following values (if multiple ex proficiencies/languages, separate with commas)")
    queries = ["name", "size", "alignment", "armor_class", "hit_points", "hit_dice", "speed{", "walk", "swim", "fly",
               "climb", "}", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "skills",
               "senses", "languages", "level"]
    indent = 0
    indentedel = 0
    for element in queries:
        print(element)
        if indent == 0:
            if '{' not in element:
                stat = input()
                if stat.isnumeric() and float(stat) % 1 < .0001:
                    newplayer[element] = int(stat)
                elif isinstance(stat, str) and stat.count(',') > 0:
                    stat = stat.split(',')
                    replacement = []
                    for fix in stat:
                        replacement.append(fix.strip().title())
                    stat = replacement
                    newplayer[element] = stat
                else:
                    newplayer[element] = stat
            else:
                newplayer[element.split("{")[0]] = {}
                indent += 1
                indentedel = newplayer[element[0:-1]]
        else:
            if '}' not in element:
                stat = input()
                if stat.isnumeric() and float(stat) % 1 < .0001:
                    indentedel[element] = int(stat)
                if isinstance(stat, str) and stat.count(',') > 0:
                    stat = stat.split(',')
                    replacement = []
                    for fix in stat:
                        replacement.append(fix.strip().title())
                    stat = element
                    indentedel[element] = stat
                else:
                    indentedel[element] = stat
            else:
                indentedel = 0
                indent -= 1
    newplayer["challenge_rating"] = newplayer["level"]
    with open(path+'players.json', "r") as f:
        playerscurr = json.load(f)
        playerscurr.append(newplayer)
    json.dumps(playerscurr)
    with open(path+'players.json', "w") as f:
        json.dump(playerscurr, f, sort_keys=True, indent=4, separators=(',', ': '))
    print("If you are in player list, back out and return before attempting to print cards or run encounters")


def runencounter():
    print('New encounter or loaded? ("new" or "load")')
    doload = input().lower()
    if doload in "new":
        print('Encounter name?')
        encname = input()
        if os.path.exists("./encounters/" + str(encname) + '.json'):
            print("ERROR: FILE EXISTS")
            return None
        with open("./encounters/" + str(encname) + '.json', "w+") as f:
            print("Enter combatants (empty line signals completion)")
            while True:
                combatant_name = input()
                print("Combatant source?")
                count = 0
                for element in monsters:
                    print(str(count) + " : " + element)
                choice = input()
                if choice.isnumeric() and int(choice) < len(monsters):
                    monstAttribs = stats(combatant_name, monsters[choice], False)
                    if monstAttribs is not None:
                        for i in range(0, len(monstAttribs[1])):
                            print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(monstAttribs[2][i])) + '\t\t' + str(
                                monstAttribs[1][i]))


def stats(query, monsterList, inputneeded):
    found = False
    if inputneeded:
        query = input().lower()
    else:
        query = query.lower()
    monstAttribs = [[], [], []]
    if query == "back":
        monstAttribs[0].append("back")
        return monstAttribs
    for element in jsondatabase[monsterList]:
        if element["name"].lower() == query:
            # pprint.pprint(element, indent=2)
            print('Done. Your ' + element['name'] + ' card is ready, here are the raw stats anyway.')
            card = Image.open('./images/basecard.png')
            cardplt = ImageDraw.Draw(card)
            carddraw(cardplt, cardlayout, element)
            card.save('./images/updated.png')
            found = True

            for attrib in attributes[0]:
                monstAttribs[0].append(attrib)
                monstAttribs[1].append(element[attrib.lower()])
                monstAttribs[2].append((element[attrib.lower()] - element[attrib.lower()] % 2 - 10) / 2)
            return monstAttribs
    if not found:
        print("Didn't see it, did you mean...")
        intended = spellcheck(query, path, monsterList)
        if intended is not None:
            query = intended
            return stats(query, monsterList, False)


def carddraw(image, cardlayout, monsterdata):
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
