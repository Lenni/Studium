#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:24:25 2018

@author: lennart
"""

def h(a, b, x, d, e=4):
	return int(((a*x+b)%d)%e)

def table(limit):
	colls = 0
	functions = 0
	
	liney = ""
	
	headerx = "y x|    "
	
	for i in range(limit):
		headerx = headerx + "{}    |    ".format(i)
	
	print(headerx)
	
	for y in range(limit):
		liney = str(y) + "  |"
		for x in range(limit):
			functions = 0
			colls = 0
			for a in range(1, limit):
				for b in range(limit):
					functions += 1
					if h(a, b, x, limit) == h(a, b, y, limit):
						colls += 1
			liney = liney + "  {:01.3f}  |".format(colls/functions)
		print(liney)
	print("\n\n\n")

table(5)
table(6)
table(7)
table(8)
table(9)