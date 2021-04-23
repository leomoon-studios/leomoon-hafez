import sys
import os
import os.path #file check
import platform #detect os platform
import re #sorting files
import zipfile
from natsort import natsorted #sort numbers properly

data = zipfile.ZipFile('audio.db', 'r')
data.setpassword(b'z!WbsdCkm#')
audio = natsorted([data.namelist()])

#audio = []
#for sfile in data.namelist():
#    if sfile.startswith('audio/'):
#        audio.append(sfile)
#audio = natsorted(audio)
#audio = audio[1:]
print(audio)
#print(data.read('robayi/رباعی شماره 9').decode("utf-8"))