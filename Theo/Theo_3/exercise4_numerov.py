#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

m = 1
h = 1

# Numerov Algorithmus
def numerov(eps, v, f0, f0p, step=0.001, thres=10.):
    """solves the equation -f''(x) + v(x) f(x) = eps f(x)
    starting with f(0) = f0 and f'(0) = f0p

    input:
        eps:   float
        v:     function float -> float
        f0:    float
        f0p:   float
        step:  float (stepsize)
        thres: fload (threshold on |f|)

    output:
        wave-function
        tuple (x, f)
        with x,f array of floats
    """

    # first two points
    x = [0., step]
    f = [f0, f0 + f0p*step]
    xjp1 = 0
    
    while abs(f[-1]) < thres:
        # previous two values
        xjm1 = x[-2]
        gjm1 = eps - v(xjm1)
        hjm1 = 1. + gjm1*step**2/12.
        fjm1 = f[-2]

        xj = x[-1]
        gj = eps - v(xj)
        hj = 1. + gj*step**2/12.
        fj = f[-1]

        # calculate next point
        xjp1 = xj + step
        gjp1 = eps - v(xjp1)
        hjp1 =1. + gjp1*step**2/12.
        fjp1 = ((12. - 10.*hj)*fj - hjm1*fjm1 )/hjp1


        # add the new point
        x.append(xjp1)
        f.append(fjp1)

    return (x,f)


def numerov_g(eps, v, step=0.001, thres=10.):
    """solves the equation -f''(x) + v(x) f(x) = eps f(x)
    starting with f(0) = 1. and f'(0) = 0.

    input:
        eps:   float
        v:     function float -> float
        step:  float (stepsize)
        thres: fload (threshold on |f|)

    output:
        wave-function
        tuple (x, f)
        with x,f array of floats
    """
    return numerov(eps, v, 1., 0., step, thres)


# ungerade Zustände
def numerov_u(eps, v, step=0.001, thres=10.):
    """solves the equation -f''(x) + v(x) f(x) = eps f(x)
    starting with f(0) = 0. and f'(0) = 1.

    input:
        eps:   float
        v:     function float -> float
        step:  float (stepsize)
        thres: fload (threshold on |f|)

    output:
        tuple (x, f):
            wave-function
            with x,f array of floats
    """
    return numerov(eps, v, 0., 1., step, thres)


# mittlere potentielle Energie
def v_av(eps, v, x, f):
    """calculates the average potential energy
            ∫ |f(x)|^2 v(x) dx /  ∫ |f(x)|^2 dx

    input:
        eps:    float
        v:      function float -> float
        x,f:    return values of numerov


    output:
        float:  average potential energy
    """

    vres = 0.
    norm = 0.

    for i in range(len(x)):
        vres += f[i]**2 * v(x[i])
        norm += f[i]**2

        # inside classical forbidden region
        if v(x[i]) > eps:
            # if abs(wavefunction) increases
            if abs(f[i]) > abs(f[i-1]):
                break

    return vres/norm



def num_derivative(x, f, delta_x = 0.05):
    return (f(x) - f(x+delta_x))/delta_x

def v(x):
    return np.array(x)**4

def func(x):
    l, _ = numerov_g(x, lambda x : 2*m/h**2 * v(x))
    return l[-1]

# hier kommt das eigentliche Programm, dass editiert werden muss
def main():
    # Energie
    eps = 0
    le = [2.5]
    delta_eps = 0.1

    eps_s = []
    len_s=[]
    peakind = [0]
    c = 0.01

    while (len(peakind) < 10):
        # gerade Wellenfunktion bestimmen
        le, f = numerov_g(eps, lambda x : 2*m/h**2 * v(x))
        df = abs(num_derivative(eps, func))
        
        if df != 0.0:
            if c/df < 10e-7:
                delta_eps = 0.01
            else:
                delta_eps = c/df

        eps += delta_eps

        eps_s.append(eps)
        len_s.append(le[-1])
        if eps > 400:
            break
        peakind, _ = signal.find_peaks(len_s)

    eps_s_sub = []
    len_s_sub = []

    for ind in peakind:
        eps_s_sub.append(eps_s[ind])
        len_s_sub.append(len_s[ind])

    E_val = np.asarray(eps_s_sub)
    E_val *= h**2/(2*m)
    print(E_val)
    
    fig = plt.figure(figsize=(7, 7))
    
    plt.plot(eps_s, len_s, label = "Convergence Radius")
    plt.plot(eps_s_sub, len_s_sub, marker = "o", linewidth = 0, label = "Peak")
    
    plt.title("Finding Converging Eigenfunctions for a given Energy")
    
    plt.ylabel("Covergence Radius")
    plt.xlabel("Energy")
    
    
    plt.savefig("Convergence.eps")
    plt.show()

    # alternativ: ungerade Wellenfunktion bestimmen
    #x, f = numerov_u(eps, v)
    
    for e in list(E_val):
        e_r = e
        le_g, f_g = numerov_g(2*m/h**2*e_r, lambda x : 2*m/h**2 * v(x))
        
        fig = plt.figure(figsize=(7, 7))
        
        plt.plot(np.array(le_g), 100*np.array(f_g) + e_r, label = "Wave Function")
        plt.plot(le_g, v(le_g), label = "Potential")
        plt.axhline(e, color="g", label = "Energy of Particle")
        plt.title(r"E_{0}: {1:.3f}".format(list(E_val).index(e), e_r))
        plt.xlim(0, 3.5)
        plt.ylim(-100, 300)
        
        plt.legend()
        plt.ylabel("Energy")
        plt.xlabel("Position")
        
        
        plt.savefig("WF_E{0}.eps".format(list(E_val).index(e)))
        plt.show()
        print('Erwartungswert v(x):', v_av(e, v, le, f))


    # mittlere potentielle Energie


if __name__ == '__main__':
    main()
