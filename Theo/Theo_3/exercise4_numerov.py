#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

m = 1
h = 1
a = 1


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
    f = [f0, f0 + f0p * step]
    xjp1 = 0

    while abs(f[-1]) < thres:
        # previous two values
        xjm1 = x[-2]
        gjm1 = eps - v(xjm1)
        hjm1 = 1. + gjm1 * step ** 2 / 12.
        fjm1 = f[-2]

        xj = x[-1]
        gj = eps - v(xj)
        hj = 1. + gj * step ** 2 / 12.
        fj = f[-1]

        # calculate next point
        xjp1 = xj + step
        gjp1 = eps - v(xjp1)
        hjp1 = 1. + gjp1 * step ** 2 / 12.
        fjp1 = ((12. - 10. * hj) * fj - hjm1 * fjm1) / hjp1

        # add the new point
        x.append(xjp1)
        f.append(fjp1)

    return x, f


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


def v(x):
    return a * np.array(x) ** 4


# hier kommt das eigentliche Programm, dass editiert werden muss
def main():
    # Energie
    eps = 0
    x = []

    eps_s_g = []
    len_s_g = []

    energies = np.linspace(0, 100, 1000)

    for eps in tqdm(energies):
        # gerade Wellenfunktion bestimmen
        x, f = numerov_g(eps, lambda x: 2 * m / h ** 2 * v(x))

        eps_s_g.append(eps)
        len_s_g.append(x[-1])

    peakind, _ = signal.find_peaks(len_s_g)

    eps_s_g_sub = []
    len_s_g_sub = []

    for ind in peakind:
        eps_s_g_sub.append(eps_s_g[ind])
        len_s_g_sub.append(len_s_g[ind])

    E_val_g = np.asarray(eps_s_g_sub)
    print(E_val_g)

    # ungerade Funktionen
    eps = 0
    x = []

    eps_s_u = []
    len_s_u = []

    for eps in tqdm(energies):
        # gerade Wellenfunktion bestimmen
        x, f = numerov_u(eps, lambda x: 2 * m / h ** 2 * v(x))

        eps_s_u.append(eps)
        len_s_u.append(x[-1])

    peakind, _ = signal.find_peaks(len_s_u)

    eps_s_u_sub = []
    len_s_u_sub = []

    for ind in peakind:
        eps_s_u_sub.append(eps_s_u[ind])
        len_s_u_sub.append(len_s_u[ind])

    E_val_u = np.asarray(eps_s_u_sub)
    print(E_val_u)

    fig = plt.figure(figsize=(7, 7))

    plt.plot(eps_s_g, len_s_g, label="Convergence Radius")
    plt.plot(eps_s_g_sub, len_s_g_sub, marker="o", linewidth=0, label="Peak")

    plt.plot(eps_s_u, len_s_u, label="Convergence Radius (uneven)")
    plt.plot(eps_s_u_sub, len_s_u_sub, marker="o", linewidth=0, label="Peak")

    plt.title("Finding Converging Eigenfunctions for a given Energy")

    plt.ylabel("Covergence Radius")
    plt.xlabel("Energy")

    plt.savefig("Convergence.eps")
    plt.show()

    # plot gerade

    for e in list(E_val_g):
        e_r = e
        le_g, f_g = numerov_g(e_r, lambda x: 2 * m / h ** 2 * v(x))

        fig = plt.figure(figsize=(7, 7))

        plt.plot(np.array(le_g), 100 * np.array(f_g) + e_r, label="Wave Function")
        plt.plot(le_g, v(le_g), label="Potential")
        plt.axhline(e, color="g", label="Energy of Particle")
        plt.title(r"E_{0}: {1:.3f}".format(list(E_val_g).index(e), e_r))
        plt.xlim(0, 3.5)
        plt.ylim(-100, 300)

        plt.legend()
        plt.ylabel("Energy")
        plt.xlabel("Position")

        plt.savefig("WF_E{0}.eps".format(list(E_val_g).index(e)))
        plt.show()

    # plot ungerade

    for e in list(E_val_u):
        e_r = e
        le_u, f_u = numerov_u(e_r, lambda x: 2 * m / h ** 2 * v(x))

        fig = plt.figure(figsize=(7, 7))

        plt.plot(np.array(le_u), 100 * np.array(f_u) + e_r, label="Wave Function")
        plt.plot(le_u, v(le_u), label="Potential")
        plt.axhline(e, color="g", label="Energy of Particle")
        plt.title(r"E_{0}: {1:.3f}".format(list(E_val_u).index(e), e_r))
        plt.xlim(0, 3.5)
        plt.ylim(-100, 300)

        plt.legend()
        plt.ylabel("Energy")
        plt.xlabel("Position")

        plt.savefig("WF_E{0}.eps".format(list(E_val_u).index(e)))
        plt.show()


if __name__ == '__main__':
    main()
