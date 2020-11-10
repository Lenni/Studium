import matplotlib.pyplot as plt
import random
import math
import numpy as np
from tqdm import tqdm


def approximatePI(N, printResult = False):
    n_kreis = 0
    n_quadrat = N

    for _ in range(0, N):
        x = random.random()
        y = random.random()

        if math.sqrt(x ** 2 + y ** 2) <= 1.0:
            n_kreis = n_kreis + 1


    pi = 4.0 * n_kreis / n_quadrat
    if printResult:
        print("Pi (" + str(N) + " steps): " + str(pi))
    return pi

def a():
    # AUFGABENTEIL A

    # Test fuer verschiedene N:
    print("Aufgabenteil a): Approximation (verschiedene N)")
    approximatePI(100, True)
    approximatePI(1000, True)
    approximatePI(10000, True)
    approximatePI(100000, True)
    approximatePI(1000000, True)

def b():

    def calcStandardDeviation(N):
        M = 500
        results = np.zeros(M)

        for i in range(0, M):
            results[i] = approximatePI(N)

        std = np.std(results)
        return std

    # Werte fuer N, die getestet werden sollen:
    n_values = np.array([10, 50, 100, 200, 400, 500, 1000, 2000, 3000, 4000, 5000, 7000, 8000, 10000])
    y = np.zeros(len(n_values))

    i = 0
    for val in tqdm(n_values):
        y[i] = calcStandardDeviation(val)
        i = i + 1

    # Plots erstellen

    fig, axs = plt.subplots(2)
    axs[0].set_title('Standardabweichung')
    axs[0].plot(n_values, y)

    axs[1].set_title('Standardabweichung (doppelt-logarithmisch)')
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')
    axs[1].plot(n_values, y)

    plt.show()
    fig.savefig("plot.pdf", bbox_inches = "tight")

def run():
    a()
    b()