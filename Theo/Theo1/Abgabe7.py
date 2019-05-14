# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt, sin, cos


time = 300
x_0 = 0.4
dt = 0.001

l = cos(x_0)
ny = 0.05



def solve_eq(x_0, l, ny ,dt=0.001):
    
    def F(x):
        return -((l - cos(x))*(1-l*cos(x))/(sin(x)**3)) + ny*sin(x)

    def S(x):
        return ((l - cos(x))/((sin(x))**2)) 
    
    xs = [x_0]
    dxs = [0]
    ts = [0]
    phis = [0]
    
    for i in range(int(time/dt)):
        x = xs[i]
        dx = dxs[i]
        
        x_next = x + dx*dt + F(x)*((dt**2)*0.5)
        xs.append(x_next)
        
        dx_next = dx + (F(x_next) + F(x))*dt*0.5
        dxs.append(dx_next)
        
        ts.append(i*dt)
        
        phi_next = phis[i] + ((S(xs[i-1]) + S(xs[i]))*dt*0.5)
        phis.append(phi_next)
        
    return xs, dxs, ts, phis

def plot_data(t, xs, l, name, title = r"$\theta$"):
    for i, x in enumerate(xs):
        plt.plot(t, x, label = r"$\lambda = {:.3f}$".format(l[i]))
    
    plt.title(title)
    plt.xlabel(r"t in s")
    plt.ylabel(r"$\theta$ in rad")
    plt.legend()
    plt.savefig(name + ".eps")
    plt.show()


# Aufgabe Teil b

x_0s = [0.4, 0.4, 0.4, 0.664]
ls = [cos(0.4), 1.1*cos(0.4), 1.4*cos(0.4), 1.25]
nys = [0.05, 0.05, 0.05, 0.05] 

thetas = []
dthetas = []
phis = []
ts = []

for i in range(len(x_0s)):
    x, dx, t, phi = solve_eq(x_0s[i], ls[i], nys[i])
    
    thetas.append(x)
    dthetas.append(dx)
    phis.append(phi)
    ts.append(t)

plot_data(t, thetas, ls, "Aufgabe3_b_theta")
plot_data(t, dthetas, ls, "Aufgabe3_b_dtheta", title = r"$\dot{\theta}$")
plot_data(t, phis, ls, "Aufgabe3_b_phi", title = r"$\phi$")


# Aufgabe c

for i in range(len(x_0s)):
    
    l_v = (ls[i] - cos(thetas[i]))/(sin(thetas[i]))**2
    l_s = (1-ls[i]*cos(thetas[i]))/(sin(thetas[i]))**2
    l_senk = dthetas[i]

    plt.plot(t, l_v, label = r"$l_v$")
    plt.plot(t, l_s, label = r"$l_s$")
    plt.plot(t, l_senk, label = r"$l_{senk}$")
    
    plt.title(r"Kreiselsystem $\lambda = {:.3f}$".format(ls[i]))
    plt.xlabel("t in s")
    plt.legend()
    
    plt.savefig("Aufgabe3c_Kreisel_{}.eps".format(i))
    plt.show()    
    
    l_1 = sin(thetas[i])*cos(phis[i])*l_s - sin(phis[i])*l_senk
    l_2 = sin(thetas[i])*sin(phis[i])*l_s + cos(phis[i])*l_senk
    l_3 = cos(thetas[i])*l_s + l_v
    
    plt.plot(t, l_1, label = r"$l_1$")
    plt.plot(t, l_2, label = r"$l_2$")
    plt.plot(t, l_3, label = r"$l_3$")
    
    plt.title(r"Inertialsystem $\lambda = {:.3f}$".format(ls[i]))
    plt.xlabel("t in s")
    plt.legend()
    
    plt.savefig("Aufgabe3c_Inertial_{}.eps".format(i))
    plt.show()  

    plt.plot(l_1, l_2)
    
    plt.title("Trajektorie in xy-Ebene")
    
    plt.savefig("Aufgabe3c_Trajektorie_{}.eps".format(i))
    plt.show()
