#!usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import os
import time

def getPoem(url, path, snum, enum, startsearch, endsearch, searcha, replacea, searchb, replaceb, searchc, replacec):
    dump = 'temp/dump.html'

    for i in range(snum,enum+1):
        clink = url+str(i)+'/'
        cfile = os.path.split(os.path.dirname(url+str(i)+'/'))[1][2:]+'.txt'
        print(' [i] DOWNLOADING: '+clink+' TO: '+cfile) #get urls
        with open(dump, "w", encoding="utf-8") as fid:
            fid.write(requests.get(clink).text)
        with open(dump, "rt", encoding="utf-8") as fid:
            contents = fid.read()
            poem = (contents[contents.find(startsearch)+len(startsearch):contents.rfind(endsearch)]).replace(searcha, replacea).replace(searchb, replaceb).replace(searchc, replacec)
            with open(path+'/'+cfile, "w", encoding="utf-8") as file:
                file.write(poem.rstrip("\n\r"))
        time.sleep(1)

#getPoem('https://ganjoor.net/hafez/ghazal/sh', 'hafez-ghazal', 1, 495, '<div class="b"><div class="m1"><p>', '</article>', '</p></div><div class="m2"><p>', "\n", '<div class="b"><div class="m1"><p>', '', '</p></div></div>', '')
#getPoem('https://ganjoor.net/hafez/ghete/sh', 'hafez-ghete', 1, 34, '<div class="b"><div class="m1"><p>', '</article>', '</p></div><div class="m2"><p>', "\n", '<div class="b"><div class="m1"><p>', '', '</p></div></div>', '')
getPoem('https://ganjoor.net/hafez/robaee2/sh', 'hafez-robayi', 1, 42, '<div class="b"><div class="m1"><p>', '</p></div></div></article>', '</p></div><div class="m2">', '', '</p></div></div><div class="b"><div class="m1">', '', '<p>', '')
exit()