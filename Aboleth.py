# dnd runner
from PIL import ImageFont, Image, ImageDraw
import pprint
import os
import json
from Spellcheck import spellcheck
from generate_name_dict import generate_name_dict

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
    if len(attributes[1]) < 3:
        for element in jsondatabase[skilldoc]:
            attributes[0].append(element["full_name"])
            attributes[1].append(element["name"])
    print('Monster list?')
    count = 0
    for element in monsters:
        print(str(count) + ': ' + element)
        count += 1
    chosenlist = validintinput(0, len(monsters)-1)
    print('Type "back" to choose a different monster list')
    monsterList = monsters[int(chosenlist)]
    while True:
        print('Options:',['stats','encounter','addplayer','addmonster'])
        stype = input().lower()
        if stype == "back":
            break
        else:
            inputneeded = True
        if stype == "stats" or stype == "stat":
            monstAttribs, block = stats("", monsterList, True)
            if monstAttribs is not None:
                for i in range(0, len(monstAttribs[1])):
                    print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(monstAttribs[2][i])) + '\t\t' + str(
                        monstAttribs[1][i]))
        if stype == "encounter":
            runencounter()
        if stype == "addplayer":
            addplayer()
        if stype == "addmonster":
            addmonster()
    main()


def addplayer():
    newplayer = {}
    print("Please provide the following values (if multiple ex proficiencies/languages, separate with commas)")
    queries = ["name", "size", "alignment", "armor_class", "hit_points", "hit_dice", "speed{", "walk", "swim", "fly",
               "climb", "}", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "skills",
               "senses", "languages", "level", "class(es)"]
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
    print('How many actions to add?')
    actions = validintinput(0, 200)
    if actions > 0:
        newplayer["actions"] = []
    validkeys = {'attack_bonus': 0, 'desc': 0, 'name': 0}
    validkeys['damage'] = ['damage_bonus', 'damage_dice', 'damage_type']
    validkeys['dc'] = ['dc_type', 'dc_value', 'success_type']
    for i in range(0, actions):
        newplayer['actions'].append({})
        while True:
            print('Continue giving one of the following keys until satisfied. Enter empty line to go to next action.')
            print(validkeys.keys())
            level1 = input()
            if level1 == '':
                break
            if validkeys.get(level1) is not None and validkeys[level1] != 0:
                print('Second level key: ', validkeys[level1])
                level2 = input()
                if level2 in validkeys[level1]:
                    print('Value?')
                    value = input()
                    newplayer['actions'][-1].setdefault(level1, {})
                    newplayer['actions'][-1][level1][level2] = value
            elif validkeys.get(level1) is not None:
                print('Value?')
                value = input()
                newplayer['actions'][-1][level1] = value
    newplayer["challenge_rating"] = newplayer["level"]
    with open(path + 'players.json', "r") as f:
        playerscurr = json.load(f)
        playerscurr.append(newplayer)
    json.dumps(playerscurr)
    with open(path + 'players.json', "w") as f:
        json.dump(playerscurr, f, sort_keys=True, indent=4, separators=(',', ': '))
    print("If you are in player list, back out and return before attempting to print cards or run encounters")
    generate_name_dict()


def addmonster():
    newplayer = {}
    print("Please provide the following values (if multiple ex proficiencies/languages, separate with commas)")
    queries = ["name", "size", "alignment", "armor_class", "hit_points", "hit_dice", "speed{", "walk", "swim", "fly",
               "climb", "}", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "skills",
               "senses", "languages", "challenge_rating", "description"]
    indent = 0
    indentedel = 0
    for element in queries:
        print(element)
        if indent == 0:
            if '{' not in element:
                stat = input()
                if stat.isnumeric() or isFloat(stat):
                    if float(stat) % 1 < .0001:
                        newplayer[element] = int(stat)
                    else:
                        newplayer[element] = float(stat)
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
    print('How many actions to add?')
    actions = validintinput(0,200)
    if actions > 0:
        newplayer["actions"] = []
    validkeys = {'attack_bonus' : 0, 'desc' : 0, 'name' : 0}
    validkeys['damage'] = ['damage_bonus', 'damage_dice', 'damage_type']
    validkeys['dc'] = ['dc_type', 'dc_value', 'success_type']
    for i in range(0, actions):
        newplayer['actions'].append({})
        while True:
            print('Continue giving one of the following keys until satisfied. Enter empty line to go to next action.')
            print(validkeys.keys())
            level1 = input()
            if level1 == '':
                break
            if validkeys.get(level1) is not None and validkeys[level1] != 0:
                print('Second level key: ', validkeys[level1])
                level2 = input()
                if level2 in validkeys[level1]:
                    print('Value?')
                    value = input()
                    newplayer['actions'][-1].setdefault(level1,{})
                    newplayer['actions'][-1][level1][level2] = value
            elif validkeys.get(level1) is not None:
                print('Value?')
                value = input()
                newplayer['actions'][-1][level1] = value
    with open(path + 'custom_monsters.json', "r") as f:
        playerscurr = json.load(f)
        playerscurr.append(newplayer)
    json.dumps(playerscurr)
    with open(path + 'custom_monsters.json', "w") as f:
        json.dump(playerscurr, f, sort_keys=True, indent=4, separators=(',', ': '))
    print("If you are in custom monster list, back out and return before attempting to print cards or run encounters")
    generate_name_dict()


def runencounter():
    print('New encounter or loaded? ("new" or "load")')
    combatants = []
    encounter = {}
    doload = input().lower()
    if doload in "new":
        print('Encounter name?')
        encname = input()
        if os.path.exists("./encounters/" + str(encname) + '.json'):
            print("ERROR: FILE EXISTS")
            return None
        with open("./encounters/" + str(encname) + '.json', "w+") as f:
            while True:
                print("Enter combatant species (empty line signals completion, will be spellchecked)")
                combatant_species = input()
                if combatant_species == '':
                    break
                print("Combatant source?")
                count = 0
                for element in monsters:
                    print(str(count) + " : " + element)
                    count += 1
                choice = validintinput(0, len(monsters)-1)
                combatant_species = spellcheck(combatant_species, path, monsters[choice])
                if combatant_species is not None:
                    monstAttribs, block = stats(combatant_species, monsters[choice], False)
                    if monstAttribs is not None:
                        combatants.append({})
                        combatants[-1]["species"] = combatant_species
                        print("Found species. Nickname?")
                        for i in range(0, len(monstAttribs[1])):
                            print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(monstAttribs[2][i])) + '\t\t' + str(
                                monstAttribs[1][i]))
                        combatants[-1]["name"] = input()
                        combatants[-1]["stats"] = monstAttribs
                        combatants[-1]["fullblock"] = block
                        print("Hit points to start?")
                        if 'hit_points' in block:
                            print('Base hit points of the species are ' + str(block['hit_points']))
                        combatants[-1]["hit_points"] = int(input())
                        combatants[-1]['notes'] = []
            encounter["combatants"] = combatants
            encounter["rounds"] = []
            encounter['rounds'].append({})
            print("INITIATIVE TIME!")
            for element in encounter["combatants"]:
                print(element["name"] + '   ' + element["species"])
                element["initiative"] = validintinput(-2000,2000)
            encounter["initiative list"] = [[], []]
            comba = encounter["combatants"]
            max = -500
            max_creature = ''
            for element in comba:
                for element1 in comba:
                    if element1["initiative"] > max and element1['name'] not in encounter['initiative list'][1]:
                        max = element1["initiative"]
                        max_creature = element1["name"]
                encounter["initiative list"][0].append(max)
                encounter["initiative list"][1].append(max_creature)
                max = -500
            json.dump(encounter, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.flush()
            print('Encounter start saved!')
            doload = 'load'
    if doload in "load":
        try:
            doload = encname
        except UnboundLocalError:
            options = []
            for file in os.listdir('./encounters'):
                options.append(file)
            print(options)
            options.clear()
            print('Encounter name?')
            encname = input()
        if not os.path.exists("./encounters/" + str(encname) + '.json'):
            print("ERROR: MISSING FILE")
            return None
        with open("./encounters/" + str(encname).split('.json')[0] + '.json', 'r') as f:
            encounter = json.load(f)
        print('Turns will now begin to iterate until empty line input. To start combat enter "nextturn"')
        sincesave = 0
        encounter.setdefault('initiativecount', 0)
        print("TURN TO " + str(encounter['initiative list'][1][encounter['initiativecount']]))
        turnid = encounter['rounds'][-1].setdefault('turn_id', 0)
        while True:
            print('Options: stats, changehp (gives ac), sethp, actions, addnote, nextturn, save')
            option = input()
            count = 0
            if option in ['stats', 'changehp', 'sethp', 'addnote', 'actions']:
                for element in encounter["combatants"]:
                    print(str(count) + ' : ' + element['name'])
                    count += 1
                creature = encounter["combatants"][validintinput(0,count-1)]
            turn = {'turn_id': turnid}
            finalturn = False
            if option == '':
                print('Would you like to save first?? [Y/N]')
                option = input()
                if option in 'Y':
                    option = 'save'
                    finalturn = True
                elif option in 'N':
                    break
            if option in 'stats':
                for i in range(0, len(creature['stats'][1])):
                    print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(creature['stats'][2][i])) + '\t\t' + str(
                        creature['stats'][1][i]))
                print('AC : ' + str(creature["fullblock"]["armor_class"]))
                print('Current HP : ' + str(creature['hit_points']))
                turn['stat lookup'] = {'creature': creature['name']}
            elif option in 'changehp' or option in 'sethp':
                print('AC : ' + str(creature["fullblock"]["armor_class"]))
                print('Current HP : ' + str(creature['hit_points']))
                print('Enter HP change')
                hpchange = validintinput(-pow(2,16)+1,pow(2,16)-1)
                turn['hp changed'] = {'creature': creature['name'], 'old_hp': creature['hit_points']}
                if option in 'changehp':
                    creature['hit_points'] += int(hpchange)
                elif option in 'sethp':
                    creature['hit_points'] = int(hpchange)
                turn['hp changed']['new_hp'] = creature['hit_points']
            elif option in 'addnote':
                note = input()
                creature['notes'].append(note)
                turn['notes'] = note
            elif option in 'nextturn':
                turnid += 1
                encounter['initiativecount'] += 1
                if encounter['initiativecount'] >= len(encounter['initiative list'][0]):
                    encounter['initiativecount'] = 0
                print("TURN TO " + str(encounter['initiative list'][1][encounter['initiativecount']]))
                for element in encounter['combatants']:
                    if encounter['initiative list'][1][encounter['initiativecount']] == element['name']:
                        print(element['notes'])
                        break
            elif option in 'save':
                with open("./encounters/" + str(encname) + '.json', "w+") as f:
                    json.dump(encounter, f, sort_keys=True, indent=4, separators=(',', ': '))
                sincesave = 0
                print('Save successful.')
                if finalturn:
                    break
            elif option in 'actions':
                if creature['fullblock'].get('actions') is not None:
                    pprint.pprint(creature['fullblock'].get('actions'), indent=4)
            encounter['rounds'].append(turn)
            turnid += 1
            if sincesave > 9:
                print("PLEASE SAVE: HAVE NOT SAVED IN " + str(sincesave))


def stats(query, monsterList, inputneeded):
    found = False
    if inputneeded:
        print("Monster species?")
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
            return monstAttribs, element
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


def isFloat(isit):
    try:
        float(isit)
        return True
    except ValueError:
        return False


def validintinput(min,max):
    print('Give valid integer between ' + str(min) + ' and ' + str(max))
    inp = input()
    while not (isFloat(inp) and (max >= int(float(inp)) >= min)):
        print('Give valid integer between ' + str(min) + ' and ' + str(max))
        inp = input()
    return int(float(inp))

main()