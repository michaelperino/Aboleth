#Can a large set of cards create a clean template?
#This disfunctional program used median method image
#Stacking to test that. Mode didnt work much better
import sys
import os
from PIL import Image
from statistics import mode
from statistics import median
import statistics

count = 0
path = "K:\\virtualdisks\\temp\\dnd card\\"
for entry in os.scandir(path):
    if entry.path.split('.')[-1] == "png":
        count += 1
        try:
            k.append(0)
        except NameError:
            k = [0]
x = [0,0,0,0]
for entry in os.scandir(path):
    if entry.path.split('.')[-1] == "png":
        try:
            im.append(Image.open(entry.path))
        except NameError:
            im = [Image.open(entry.path)]
        try:
            data.append(im[-1].load())
        except NameError:
            data = [im[-1].load()]
            extra = im[-1].load()
for i in range(0,600):
    print(i)
    for j in range(0,800):
        for p in range(0,3):
            for t in range(0,count):
                k[t] = data[t][i,j][p]
            try:
                mo = mode(k)
                me = median(k)
                x[p] = int(mo if mo > me else me)
            except statistics.StatisticsError:
                x[p] = int(median(k))
        extra[i,j] = (x[0],x[1],x[2],255)
im[0].save('./test3.png')
