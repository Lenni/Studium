#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 21:44:56 2019

@author: lennart
"""

def gaussian(x, a, b, E,mu, sig):
    return np.float64(a) + np.float64(b)*np.float64(x) + np.float64(E)*np.exp(-((x-mu)/sig)**2)

def lorentz(x, a, b, E, x_0, gamma):
    x = np.array(x)
    return np.float64(a) + np.float64(b)*np.float64(x) + np.float64(E)/np.float64((x**2 - x_0**2)**2 + gamma**2*x_0**2)

def gauss(x, A, mu, sig):
    return np.float64(A)*np.exp(-((x-mu)/sig)**2)

def function(x, a, b, A1, A2, A3, A4, mu1, sig1, mu2, sig2, mu3, sig3, mu4, sig4):
    return a+ b*x + gauss(x, A1, mu1, sig1) + gauss(x, A2, mu2, sig2) + gauss(x, A3, mu3, sig3) + gauss(x, A4, mu4, sig4)

def extract_subarray(array_x, array_y, min_value, max_value):
    result_x = []
    result_y = []
    
    for x in range(len(array_x)):
        if array_x[x] > min_value and array_x[x] < max_value:
            result_x.append(array_x[x])
            result_y.append(array_y[x])
    
    return result_x, result_y         
    
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import scipy.constants as constants

file = "DopplerfreieSpektroskopieRubidium.csv"


freq = []
v1 = []
v2 = []
v3 = []

with open(file) as f:
    reader = csv.DictReader(f)
    next(reader, None)
    for row in reader:
        freq.append(float(row["X"]))
        v1.append(float(row["CH1"]))
        v2.append(float(row["CH2"]))
        v3.append(float(row["CH3"]))

freq = np.array(freq)
freq = freq*0.016

fig = plt.figure(figsize=(10, 6))

plt.plot(freq, v1, linewidth = 0, marker = "o", label = "Data")

plt.xlabel("Frequency in GHz")
plt.ylabel("Intensity")
plt.legend()

plt.title("Recorded Data")

plt.show()

####Teil B

sub_f, sub_y = extract_subarray(freq, v1, 9.3, 10.8)

fig = plt.figure(figsize=(10, 6))

plt.plot(sub_f, sub_y, linewidth = 0, marker = "o", label= "Data")

popt, pcov = scipy.optimize.curve_fit(gaussian, sub_f, sub_y, p0=[0, 0, 3, 3, 7])

plt.plot(sub_f, gaussian(sub_f, *popt),label= "Gaussian Model")

popt, pcov = scipy.optimize.curve_fit(lorentz, sub_f, sub_y, p0=[0, 0, 3, 10, 0.1])

plt.plot(sub_f, lorentz(sub_f, *popt),label= "Lorentz Model")

plt.xlabel("Frequency in GHz")
plt.ylabel("Intensity")
plt.legend()
plt.title("Fitting of Models to Peak")

plt.show()

m_Rb = 1.4192e-25

T  = np.float64((popt[4]*10**9)**2/(popt[3]*10**9)**2)* constants.c**2 * np.float64(m_Rb/constants.k)

print("Lorentz - Curve seems to fit better -> Calculate Temperature")

print("Temperature:{:.3f} K".format(T))


#### Teil D

fig = plt.figure(figsize=(10, 6))

plt.plot(freq, v1, linewidth = 0, marker = "o", label = "Data")

popt, pcov = scipy.optimize.curve_fit(function, freq, v1, p0=[1, -0.1, -0.5, -0.5, -0.5, -0.5, 5.7, 0.5, 6.8, 0.5, 10.1, 0.5, 12.6, 0.8])

plt.plot(freq, function(freq, *popt),label= "Model")


plt.xlabel("Frequency in GHz")
plt.ylabel("Intensity")
plt.legend()

plt.title("Fit to all Data")

plt.show()

for i in range(1, 8, 2):    
    print("mu_{}: {:.3f}   sig_{}: {:.3f}".format(int(i/2)+1, popt[5 + i], int(i/2)+1, popt[5+(i+1)]))

