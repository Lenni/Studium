#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 21:32:40 2019

@author: lennart
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy
from statistics import mean
from itertools import groupby


def func(x, x1, x2):
    x = np.array(x)/360*np.pi*2
    a = np.sin(x/2)
    res = x1 * np.sign(a) * (np.abs(a))**x2
    return np.log(res)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size = 15)

datafile = "rutherford.csv"

t = []
w = []
r = []

with open(datafile) as f:
    reader = csv.DictReader(f, delimiter=";")
    
    for row in reader:
        te = row["Messzeit [min]"]
        we = row["Winkel [deg]"]
        re = row["Rate [1/s]"]
        t.append(float(te.replace(",", ".")))
        w.append(float(we.replace(",", ".")))
        r.append(float(re.replace(",", ".")))

w_known = []
w_known.append(w[0])

temp = []

for i in range(len(w)):
    temp.append((w[i], r[i]))
    

temp.sort()

grouper = groupby(temp, key=lambda x: x[0])
L = [[x, mean(yi[1] for yi in y)] for x,y in grouper]

x = []
y = []

for item in L:
    x.append(item[0])
    y.append(item[1])

fig = plt.figure(figsize=(7, 5))


plt.plot(x, y)

plt.title("Zählraten Rutherford Experiment")
plt.xlabel(r"Winkel [$^\circ]$")
plt.ylabel(r"Zählrate [$\frac{1}{s}$]")


popt, pcov = scipy.optimize.curve_fit(func, x[1::], np.log(y[1::]))

plt.plot(x[1::], np.e**func(x[1::], *popt))

plt.yscale("log")

plt.savefig("plot.eps", bbox_inches = "tight")
plt.show()

print("x1 = {:.3}   x2 = {:.3}".format(popt[0], popt[1]))