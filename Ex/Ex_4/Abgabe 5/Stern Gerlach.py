#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 20:29:22 2019

@author: lennart
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as c
from scipy.stats import maxwell

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams.update({'font.size': 22})

def save():
        
    dB_dz = slider_dB_dz.get()
    T = slider_T.get()
    l = slider_l.get()
    d = slider_d.get()
    itas = slider_itas.get()
    blende = slider_b.get()
    
    plt.savefig("Histogramm_{}_{}_{}_{}_{}_{}.eps".format(dB_dz, T, l, d, itas, blende))

def refresh():
    
    dB_dz = slider_dB_dz.get()
    T = slider_T.get()
    l = slider_l.get()
    d = slider_d.get()
    itas = slider_itas.get()
    blende = slider_b.get()
    
    data = stern_gerlach(dB_dz=dB_dz, T=T, l=l, d=d, iterations=itas, blende = blende)
    ax.cla()
    
    sig = np.std(data)
    
    ax.hist(data, bins=1000, range=(-2*sig,2*sig), label=r"$\frac{{dB}}{{dz}} = {} \quad  T = {} \quad l = {}$".format(dB_dz, T, l))
    
    ax.set_title("Zoom in histogramm, between {:.2f} and {:.2f} m".format(-2*sig, 2*sig))
    ax.set_xlabel("z-position on screen in m")
    ax.legend()
    
    canvas.draw()

def stern_gerlach(dB_dz = 82, T = 190, l = 0.1, d = 0.32, iterations = 10000, blende = 0.00):
    T = T + 273
    
    
    mu_B = 9.72*(10**(-24))
    m_k = 6.492*(10**(-26)) 
    g_s = 2
    
    defs = []
    
    for i in range(iterations):
    
        if np.random.randint(1, 3) == 1:
            s = 0.5
        else:
            s = -0.5
        
        F = g_s*mu_B*s*dB_dz
        
        v = maxwell.rvs(scale= np.sqrt(c.k*T/m_k))
        
        t = l/v
        
        z = 0.5*F/m_k*t**2
        
        angle = np.arctan((F/m_k*t)/(v))
        angle += np.random.uniform(-3*blende, 3*blende)
        
        z_0 = np.random.uniform(-blende, blende)
        
        deflection = z_0 + z + d*(np.tan(angle))
        
        defs.append(deflection)
    
    return defs


data = stern_gerlach()

fig = plt.figure(figsize=(16, 9))

plt.hist(data, bins=1000)
plt.xlabel("z-position on screen in m")
plt.title("Full histogramm of z positions on the screen in simulation")

plt.show()

fig = plt.figure(figsize=(16, 9))
ax = plt.gca()
 
ax.hist(data, bins=1000, range=(-0.05,0.05))
ax.set_title("Zoom in histogramm, between -0,05 and 0,05 m")
ax.set_xlabel("z-position on screen in m")
plt.savefig("Histogramm.eps")

root = tk.Tk()
root.title("Stern Gerlach Experiment")


frame = tk.Frame(root)

button_refresh = tk.Button(frame, text="Refresh", command=refresh)
button_refresh.pack(side = "left")

button_save = tk.Button(frame, text="Save", command = save)
button_save.pack(side = "left")

slider_dB_dz = tk.Scale(frame, from_=0, to_=1000, label= "Magnetfeld")
slider_dB_dz.set(82)
slider_dB_dz.pack()

slider_T = tk.Scale(frame, from_=0, to_=500, label="Ofentemperatur")
slider_T.set(190)
slider_T.pack(side = "left")

slider_l = tk.Scale(frame, from_=0.1, to_=1, resolution=0.1, label = "Länge Magnetfeld")
slider_l.set(0.1)
slider_l.pack(side = "left")

slider_d = tk.Scale(frame, from_=0.1, to_=1, resolution=0.1, label = "Abstand Schirm")
slider_d.set(0.3)
slider_d.pack(side = "left")

slider_b = tk.Scale(frame, from_=0, to_=0.1, resolution=0.01, label = "Blendenöffnung (m)")
slider_b.set(0.0)
slider_b.pack(side = "left")

slider_itas = tk.Scale(frame, from_=0, to_=100000, label="Simulierte Teilchen")
slider_itas.set(10000)
slider_itas.pack(side = "left")

canvas = FigureCanvasTkAgg(fig, master = root)
canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand=1)

frame.pack()

root.mainloop()