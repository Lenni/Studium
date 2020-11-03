#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

datafile = "AbschirmungVonRoentgenstrahlung.csv"
settingsfile = "Settings.csv"


E = []
N1 = []
N2 = []
N3 = []
N4 = []
N5 = []
N6 = []
N7 = []
N8 = []
N9 = []
f = []

I = []
t = []
d = []

with open(settingsfile) as f:
    reader = csv.DictReader(f, delimiter=";")
    
    for row in reader:
        I.append(float(row["Roehrenstrom/mA"]))
        t.append(float(row["Messdauer/s"]))
        d.append(float(row["Aluminium Dicke/mm"]))

with open(datafile) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t');
    print(reader.fieldnames)
    for row in reader:
        N1.append(float(row["N_1"]))
        N2.append(float(row["N_2"]))
        N3.append(float(row["N_3"]))
        N4.append(float(row["N_4"]))
        N5.append(float(row["N_5"]))
        N6.append(float(row["N_6"]))
        N7.append(float(row["N_7"]))
        N8.append(float(row["N_8"]))
        N9.append(float(row["N_9"]))

Ns = [N1, N2, N3, N4, N5, N6, N7, N8, N9]
fig = plt.figure(figsize=(10, 8))

ks = []


for i in range(1, len(Ns)):
    
    N = Ns[i]
    
    
    N_norm = np.array(N) / (t[i] * I[i])
    
    N_norm = N_norm[10:150]
    
    peaks, _ = sig.find_peaks(N_norm, prominence = 60, height = 300)
    
    if len(peaks) == 2:
        print(peaks)
        dist = peaks[1] - peaks[0]
        
        k = (19.7 - 17.44)/(dist)
        ks.append(k)


k_mean = np.mean(ks)

for i in range(1, len(Ns)):
    
    N = Ns[i]
    
    
    N_norm = np.array(N) / (t[i] * I[i])
    
    N_norm = N_norm[10:150]
    
    
    for peak in peaks:
        plt.scatter(peak*k_mean, N_norm[peak])
    
    plt.plot(np.linspace(0, (k_mean*len(N_norm)), len(N_norm)) ,N_norm, label="Spektrum für N{}".format(i))
    
    plt.title("Spektren")
    
    plt.xlabel("Energy [keV]")
    plt.ylabel("Relative Intensität")
    
    plt.yscale("log")
    plt.ylim(10e-3, 10e4)

plt.legend()
plt.savefig("Roentgen.eps", bbox_inches="tight")
plt.show()

intens_1 = []
intens_2 = []
print("Steigung: {} keV/Bin".format(k_mean))





xs = np.linspace(0, (k_mean*140))

x_value_1 = min(xs, key=lambda x:abs(x-15))
index_1 = list(xs).index(x_value_1)

x_value_2 = min(xs, key=lambda x:abs(x-25))
index_2 = list(xs).index(x_value_2)


for i in range(0, len(Ns)):

    N = Ns[i]
    N_norm = np.array(N) / (t[i] * I[i])
    N_norm = N_norm[10:150]
    intens_1.append(N_norm[index_1])
    intens_2.append(N_norm[index_2])
    
    

for k, intensity in enumerate(intens_1):
    ab = abs(-np.log(intensity/intens_1[0])/(0.001*d[i]))
    print("Absorptionskoeffizient 15 keV N_{}: {:.3f}".format(k, ab))
    


for k, intensity in enumerate(intens_2):
    
    ab = abs(np.log(intensity/intens_2[0])/(0.001*d[i]))
    print("Absorptionskoeffizient 25 keV N_{}: {:.3f}".format(k, ab))