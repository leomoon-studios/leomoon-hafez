#!usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os.path #file check

path = 'audio'
files = os.listdir(path)
#print()

for sfile in files:
    os.rename(path+'/'+sfile, path+'/'+'غزل شماره '+sfile)