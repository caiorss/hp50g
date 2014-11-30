#!/usr/bin/env python2

import sys
import os

filename = sys.argv[1]

txt = open(filename).read()

charmap = [
['\xab', '\<<'],
['\xbb', '\>>'],
['\x8d', '\->'],
['\x8e', '\<-'],
['\x8c', r'\alpha'],
['\x87', r'\pi'],
['\x8c', r'\alpha'],
['\x95', r'\theta'],
['\x97', r'\rho'],
['\x98', r'\sigma'],
['\x99', r'\tau'],
['\x9a', r'\omega'],
['\x85', r'\summation'],
['\x9b', r'\delta'],
['\x9c', r'\PI'],
['\x9d', r'\Omega'],
['\x93', r'\epsilon'],
['\xb5', r'\mi'],
['\xae', r'\copyright'],
['\xa9', r'\copyleft'],
]


def translate_hp2txt(hptxt):
    
    txt = hptxt
    
    for k, v in charmap:        
        txt = txt.replace(k, v)
    
    return txt

print translate_hp2txt(txt)

#print txt.replace('\xab', '<<').replace('\xab', '<<').replace('\x8d', '-->')


