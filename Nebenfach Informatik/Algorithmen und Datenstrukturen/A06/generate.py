import os
import math

filename = "test"

file = open(filename, "wt")

i = 0

text = []

while i < 4* 10**6:
	text.append(str(i) + "\n")
	i = i + 1

file.write(str(text[::-1]))
file.close()