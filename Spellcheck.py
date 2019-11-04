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
    count = len(mystery_word)
    while count > 0 and len(possibilities) < 5:
        current = mystery_word[0:count].lower()
        for i in range(0, len(locdict)):
            valid = False
            for element2 in locdict[i]:
                if current in element2[0:count].lower():
                    valid = True
            if valid:
                possibilities.append(locdict[i])
        count -= 1
    count = 0
    for element in possibilities:
        result = ' '.join(element)
        print(str(count) + ': ' + result)
        count += 1
    print('If none of these are intended options, just press enter')
    choice = input()
    if choice.isnumeric() and int(choice) < len(possibilities):
        print(' '.join(possibilities[abs(int(choice))]))
        return ' '.join(possibilities[abs(int(choice))])
    else:
        return None
