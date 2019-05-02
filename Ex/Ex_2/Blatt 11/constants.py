#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:35:06 2018

@author: lennart
"""

import scipy.constants as sc

dic = sc.physical_constants
suggestions = []
eingabe = input("Enter keyword of a Constant: ")

while eingabe != "ende":
    for key in dic.keys():
        if eingabe in key:
            suggestions.append(key)
            
            if eingabe == key:
                print("\n\n\n\n")
                print("{0} is {1} {2} with precision of {3}".format(key, dic[key][0], dic[key][1], dic[key][2]))
                suggestions = []
    
    if len(suggestions) != 0:
        print("Did you mean: ")
        for i, key in enumerate(suggestions):
            print("{0}. {1} {2}".format(i, key, dic[key]))
    eingabe = input("Enter keyword of a Constant: ")

