# dnd runner
from PIL import ImageFont, Image, ImageDraw
import pprint
import os
import json
from Spellcheck import spellcheck, quickcheck, reloadnames
from generate_name_dict import generate_name_dict

# in the future, is there a better way to accomplish this? maybe a json file that labels what is what?
monsters = ["5e-SRD-Monsters.json", "Great-DND5e-Monster-Spreadsheet.json",
            "Great-DND5e-Monster-Spreadsheet-Homebrew.json", "players.json", "custom_monsters.json"]
skilldoc = "5e-SRD-Ability-Scores.json"
spelldoc = "5e-SRD-Spells.json"
cardfile = "./images/cardlayout.json"
path = '../open5e/'

jsondatabase = {} # stores all the json files to memory
attributes = [[], []] # stores all the skill names and abbreviations to memory
cardlayout = None # sets default cardlayout as None to avoid a try except loop
if os.path.exists(cardfile): # gets json layout of the card
    with open(cardfile, 'r') as f:
        cardlayout = json.load(f)
else:
    print('ERROR: No card layout detected. Unable to create stat cards.')


def main():
    for file in os.listdir(path):  # gets list of all the json files
        if file.endswith(".json"):
            with open(path + file, 'r') as f:
                jsondatabase[file] = json.load(f)  # subsequently loads those json files to memory
    if len(attributes[1]) < 3:  # tests if attributes have already been created by a previous call or import
        for element in jsondatabase[skilldoc]:
            attributes[0].append(element["full_name"])
            attributes[1].append(element["name"])
    print('Monster list?')
    count = 0
    for element in monsters:
        print(str(count) + ': ' + element)
        count += 1
    chosenlist = validintinput(0, len(monsters) - 1)  # validintinput gets an input between min and max (inclusive)
    print('Type "back" to choose a different monster list')
    monsterList = monsters[int(chosenlist)]  # defines which list we will use first
    while True:
        print('Options:', ['back', 'stats', 'encounter', 'addplayer', 'addmonster', 'spell', 'customrequest'])  # list of options
        stype = input().lower()  #
        if stype == "back":
            break
        if stype == "stats" or stype == "stat":  # puts monster stats onto card
            monststats = stats("", monsterList, True)
            if monststats is not None:
                monstAttribs, block = monststats
            else:
                monstAttribs, block = (None, None)
            if monstAttribs is not None:
                for i in range(0, len(monstAttribs[1])):
                    print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(monstAttribs[2][i])) + '\t\t' + str(
                        monstAttribs[1][i]))
        if stype == "encounter":  # starts encounter
            runencounter()
        if stype == "addplayer":  # adding a custom player
            addmonster('players.json')
        if stype == "addmonster":  # adding a custom monster
            addmonster('custom_monsters.json')
        if stype == "spell":
            spell = customrequest(file = spelldoc)
            pprint.pprint(spell, indent=2, sort_dicts=True)
        if stype == 'customrequest':
            block = customrequest()
            pprint.pprint(block, indent=4, sort_dicts=True)
        if stype == 'maintenance':
            print('Surprised you spelled it right')
            generate_name_dict()
            reloadnames()


def addmonster(file):
    newplayer = {}
    print("Please provide the following values (if multiple ex proficiencies/languages, separate with commas)")
    queries = ["name", "race", "size", "alignment", "armor_class", "hit_points", "hit_dice", "speed{", "walk", "swim", "fly",
               "climb", "}", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "skills",
               "senses", "languages", "challenge_rating/level", "description", 'class']
    indent = 0  # this is a rather hard to understand way of doing indentation, anything better?
    indentedel = 0
    for element in queries:
        print(element)  # prints what type of data we are looking for
        if indent == 0:
            if '{' not in element:  # checks if this data shouldn't be indented
                stat = input()
                if isInteger(stat):  # integers should not be stored as strings in the json file
                    newplayer[element] = int(stat)
                elif isFloat(stat):
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
            else:  #data should be indented
                newplayer[element.split("{")[0]] = {}  # dict to allow indented data
                indent += 1  # tells us to indent on next iteration
                indentedel = newplayer[element[0:-1]]  # element[0:-1] is probably the same as element.split("{")[0]
        else:
            if '}' not in element:  # remain indented
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
            else:  # escape indentation
                indentedel = 0  # possibly not necessary?
                indent -= 1  # sets up for double indented in the future though it probably won't work now
    newplayer['challenge_rating'] = newplayer["challenge_rating/level"]  # quick fix to meet standard
    newplayer.pop("challenge_rating/level")  # keeps it clean
    print('How many actions to add?')  # attacks, spells, etc
    actions = validintinput(0, 200)  # if they do more than 200 actions their fingers might fall off
    if actions > 0:
        newplayer["actions"] = []
    validkeys = {'attack_bonus': 0, 'desc': 0, 'name': 0}
    # these three lines could be made one declaration, but i think this adds clarity personally
    validkeys['damage'] = ['damage_bonus', 'damage_dice', 'damage_type']
    validkeys['dc'] = ['dc_type', 'dc_value', 'success_type']
    for i in range(0, actions):
        newplayer['actions'].append({})
        while True:
            print('Continue giving one of the following keys until satisfied. Enter empty line to go to next action.')
            print(validkeys.keys())  # gives user valid options
            level1 = input()
            if level1 == '':  #escape mechanism
                break
            if validkeys.get(level1) is not None and validkeys[level1] != 0:  # indented
                print('Second level key: ', validkeys[level1])  # gives indented options (currently no double indent support)
                level2 = input()
                if level2 in validkeys[level1]:
                    print('Value?')
                    value = input()
                    newplayer['actions'][-1].setdefault(level1, {})  # needs to happen once per indent
                    newplayer['actions'][-1][level1][level2] = value
            elif validkeys.get(level1) is not None:
                print('Value?')
                value = input()
                newplayer['actions'][-1][level1] = value
    playerscurr = []
    if os.path.exists(path + file):
        with open(path + file, "r") as f:  # i would like to keep my old customs too
            playerscurr = json.load(f)
    playerscurr.append(newplayer)
    json.dumps(playerscurr)
    with open(path + file, "w+") as f:
        # printed nicely incase i want to edit later manually
        json.dump(playerscurr, f, sort_keys=True, indent=4, separators=(',', ': '))
    print("If you are in custom monster list, back out and return before attempting to print cards or run encounters")
    generate_name_dict()  # spellcheck purposes
    reloadnames()  # allows spellcheck to work? maybe? it stays for now


def runencounter():
    print('New encounter or loaded? ("new" or "load")')
    combatants = []
    encounter = {}
    doload = input().lower()
    if doload in "new":
        print('Encounter name?')
        encname = input()
        if os.path.exists("./encounters/" + str(encname) + '.json'):  # we don't like overwriting files
            print("ERROR: FILE EXISTS")
            return None
        with open("./encounters/" + str(encname) + '.json', "w+") as f:  # now we know we can write to it
            while True:  # I might move file open to later in case there are errors in this part to avoid empty files
                print("Enter combatant species (empty line signals completion, will be spellchecked)")
                combatant_species = input()
                if combatant_species == '':
                    break
                print("Combatant source?")
                count = 0
                for element in monsters:
                    print(str(count) + " : " + element)
                    count += 1
                choice = validintinput(0, len(monsters) - 1)
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
                element["initiative"] = validintinput(-2000, 2000)
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
            print('Options: stats, changehp (gives ac), sethp, actions, addnote, nextturn, save, spell, customrequest')
            option = input()
            finalturn = False
            if option == '':
                print('Would you like to save first?? [Y/N]')
                option = input()
                if option in 'Y':
                    option = 'save'
                    finalturn = True
                elif option in 'N':
                    break
            count = 0
            needcreature = ['stats', 'changehp', 'sethp', 'addnote', 'actions']
            if option in needcreature:
                for element in encounter["combatants"]:
                    print(str(count) + ' : ' + element['name'])
                    count += 1
                creature = encounter["combatants"][validintinput(0, count - 1)]
            turn = {'turn_id': turnid}
            if option == 'stats' or option == 'stat':
                for i in range(0, len(creature['stats'][1])):
                    print(str(attributes[1][i]) + '  ' + '{0:+}'.format(int(creature['stats'][2][i])) + '\t\t' + str(
                        creature['stats'][1][i]))
                print('AC : ' + str(creature["fullblock"]["armor_class"]))
                print('Current HP : ' + str(creature['hit_points']))
                turn['stat lookup'] = {'creature': creature['name']}
            elif option  == 'changehp' or option == 'sethp':
                print('AC : ' + str(creature["fullblock"]["armor_class"]))
                print('Current HP : ' + str(creature['hit_points']))
                print('Enter HP change')
                hpchange = validintinput(-pow(2, 16) + 1, pow(2, 16) - 1)
                turn['hp changed'] = {'creature': creature['name'], 'old_hp': creature['hit_points']}
                if option == 'changehp':
                    creature['hit_points'] += int(hpchange)
                elif option == 'sethp':
                    creature['hit_points'] = int(hpchange)
                turn['hp changed']['new_hp'] = creature['hit_points']
                print(turn['hp changed'])
            elif option == 'addnote':
                note = input()
                creature['notes'].append(note)
                turn['notes'] = note
            elif option == 'nextturn':
                turnid += 1
                encounter['initiativecount'] += 1
                if encounter['initiativecount'] >= len(encounter['initiative list'][0]):
                    encounter['initiativecount'] = 0
                print("TURN TO " + str(encounter['initiative list'][1][encounter['initiativecount']]))
                for element in encounter['combatants']:
                    if encounter['initiative list'][1][encounter['initiativecount']] == element['name']:
                        print(element['notes'])
                        break
            elif option == 'spell':
                spell = customrequest(file=spelldoc)
                spell = {} if spell is None else spell
                turn['notes'] = 'Gave spell info for: ' + str(spell.get('name'))
                pprint.pprint(spell, indent=2, sort_dicts=True)
            elif option == 'save':
                with open("./encounters/" + str(encname) + '.json', "w+") as f:
                    json.dump(encounter, f, sort_keys=True, indent=4, separators=(',', ': '))
                sincesave = 0
                print('Save successful.')
                if finalturn:
                    break
            elif option == 'actions':
                if creature['fullblock'].get('actions') is not None:
                    pprint.pprint(creature['fullblock'].get('actions'), indent=4)
            elif option == 'customrequest':
                block = customrequest()
                pprint.pprint(block, indent = 4, sort_dicts = True)
            encounter['rounds'].append(turn)
            turnid += 1
            if sincesave > 9:
                print("PLEASE SAVE: HAVE NOT SAVED IN " + str(sincesave))


def customrequest(**kwargs):
    file = kwargs.get('file', None)
    count = 0
    files = list(jsondatabase.keys())
    if file is None:
        for i in range(0, len(files)):
            print(str(count) + " : " + str(files[count]))
            count += 1
        choice = validintinput(0, len(files) - 1)
    else:
        choice = int(files.index(file))
    try:
        jsondatabase[str(files[choice])][0]['name']
    except KeyError:
        print('BAD, that has no names')
        return None
    print('What are you looking for?')
    request = input()
    sendfile = str(files[choice])
    possiblerequest = quickcheck(request, path, sendfile)
    if possiblerequest is not None:
        possiblerequest = possiblerequest.lower()
    else:
        spell = spellcheck(request, path, sendfile)
        if spell is not None:
            possiblerequest = quickcheck(spell, path, sendfile)
            possiblerequest = possiblerequest.lower()
    for element in jsondatabase[sendfile]:
        if element['name'].lower() == possiblerequest:
            return element
    return None

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
        if 'name' in element:
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


def isInteger(isit):
    if isFloat(isit) and float(isit) % 1 < .00005:
        return True
    else:
        return False


def validintinput(min, max):
    print('Give valid integer between ' + str(min) + ' and ' + str(max))
    inp = input()
    while not (isFloat(inp) and (max >= int(float(inp)) >= min)):
        print('Give valid integer between ' + str(min) + ' and ' + str(max))
        inp = input()
    return int(float(inp))


while True:
    main()
