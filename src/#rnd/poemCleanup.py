#!usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import glob

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

cfolder = 'ghazal/'

print(os.listdir(cfolder))
for sfile in os.listdir(cfolder):
    print(cfolder+'/'+sfile[:-4])
    with open(cfolder+'/'+sfile, "rt", encoding="utf-8") as file:
        poem = ''
        for chunk in chunks(file.readlines(),2):
            poem += chunk[0]+chunk[1]+'\n'
        with open(cfolder+'/'+sfile[:-4]+'_clean.txt', "w", encoding="utf-8") as file:
            file.write(poem.rstrip("\n\r"))
#print(glob.glob("ghazal/*.txt"))
#for sfile in glob.glob("ghazal/*.txt"):
#    print(sfile)
#exit()


    #print(chunks(file.readlines(),5))
    #print('<p style="text-align:center; color:black;">'+file.read().replace('\n', '<br />')+'</p>')