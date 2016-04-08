#coding:utf-8
#File: imgformattrans.py
#Auth: lixp(@500wan.com)
#Date: 2015-11-11 10:48:28
#Desc: 

import os
import sys
from pytesser import *

fin = sys.argv[1]
fou = sys.argv[2]


image = Image.open(fin)
image.save(fou)
