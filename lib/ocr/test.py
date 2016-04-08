#coding:utf-8
#File: ocr-test.py
#Auth: lixp(@500wan.com)
#Date: 2015-11-10 17:06:26
#Desc: 

from pytesser import *
import ImageEnhance

#image = Image.open("./test.tif")
image = Image.open("./login2.jpg")
enhancer = ImageEnhance.Contrast(image)
image_enhancer = enhancer.enhance(4)
print image_to_string(image_enhancer)
