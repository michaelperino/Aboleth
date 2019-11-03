import os
import json
from generate_name_dict import generate_name_dict as namegen


def spellcheck(mystery_word, path, expected_loc):
    locdict = [[]]
    possibilities = []
    namepath = "./namelist.json"
    if not os.path.exists(path + namepath):
        namegen()
    with open(namepath, 'r') as f:
        filedict = json.load(f)
    for element in filedict[expected_loc]:
        locdict.append(element.split())
    locdict.remove([])
    count = 1
    #print(locdict)
    while count < len(mystery_word) + 1 and len(locdict) > 0:
        current = mystery_word[0:count].lower()
        for element1 in locdict:
            if element1 == ['Ancient', 'Black', 'Dragon']:
                print(count)
            valid = False
            for element2 in element1:
                if current == element2[0:count].lower():
                    valid = True
            if not valid:
                locdict.remove(element1)
        count += 1
    count = 0
    for element in locdict:
        quip = ' '.join(element)
        print(str(count) + ': ' + quip)
        count += 1
    choice = input()
    print('If these are all not intended options, just press enter')
    if choice.isnumeric():
        return(' '.join(locdict[int(choice)]))
    else:
        return None
