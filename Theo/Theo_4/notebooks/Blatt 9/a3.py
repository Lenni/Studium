from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

rand = np.random.Generator(np.random.MT19937())


def generate_lattice(size):
    lattice = np.random.randint(0, 2, (size, size))

    lattice[lattice == 0] = -1

    return lattice


def local_lattice_energy(lattice, i, j, J=1):
    en = 0
    if j + 1 >= lattice.shape[0]:
        en += lattice[i][j] * lattice[i][0]
    else:
        en += lattice[i][j] * lattice[i][j + 1]

    en += lattice[i][j] * lattice[i][j - 1]

    if i + 1 >= lattice.shape[0]:
        en += lattice[i][j] * lattice[0][j]
    else:
        en += lattice[i][j] * lattice[i + 1][j]

    en += lattice[i][j] * lattice[i - 1][j]

    return en


def lattice_energy(lattice, J=1):
    sum = 0

    for i in range(lattice.shape[0]):
        for j in range(lattice.shape[0]):
            en = local_lattice_energy(lattice, i, j, J=1)
            sum += en

    sum = sum * -J / 2

    return sum


def lattice_magnetization(lattice):
    spins = lattice.shape[0] ** 2

    spin_sum = np.sum(lattice) * 1.0

    return abs(spin_sum / spins)


def random_flip(k, T):
    k_p = np.copy(k)
    beta = 1 / T

    i = rand.integers(k.shape[0])
    j = rand.integers(k.shape[0])

    k_p[i][j] = -k_p[i][j]

    dE = local_lattice_energy(k, i, j)

    if dE < 0:
        return k_p
    else:
        if rand.random(1) < np.exp(-beta * dE):
            return k_p
        else:
            return k


def thermalize(lattice, temp, steps=3000):
    Es = []

    for i in range(steps):
        lattice = random_flip(lattice, temp)
        Es.append(lattice_energy(lattice))

    return Es, lattice


def mc_step(lattice, temp):
    for i in range(lattice.shape[0] ** 2):
        lattice = random_flip(lattice, temp)

    return lattice_magnetization(lattice), lattice_energy(lattice), lattice


def calculate_magnetization(lattice, temp):
    Ms = []

    for i in range(3000):
        M, E, k = mc_step(lattice, temp)
        Ms.append(M)

    mean = np.mean(Ms)
    std = np.std(Ms)

    return mean, std


def ising(temp):
    print("Running for T = {}".format(temp))
    Ms = []
    Ss = []

    for i in range(20):
        k = generate_lattice(8)
        print("Lattice initialized!")

        Energies, k = thermalize(k, temp)
        print("Lattice thermalized")

        M, S = calculate_magnetization(k, temp)
        Ms.append(M)
        Ss.append(S)

    M = np.sum(Ms) / len(Ms)
    sw = np.std(Ms) / np.sqrt((len(Ms)))

    print("{} +- {}".format(M, sw))

    fig = plt.figure(figsize=(16, 9))

    plt.plot(Ms)
    plt.ylim((-0.2, 1.2))

    plt.title("Temp = {}".format(temp))
    plt.savefig("{}.eps".format(temp))
    plt.close()

    return temp, M, sw


if __name__ == "__main__":
    temps = np.linspace(1, 5, 100)

    mean_M = []
    std_M = []
    ts = []
    pool = Pool()

    async_result = pool.map(ising, temps.tolist())

    pool.close()
    pool.join()

    for result in async_result:
        t, M, sw = result

        mean_M.append(M)
        std_M.append(sw)
        ts.append(t)

    fig = plt.figure(figsize=(16, 9))

    plt.errorbar(temps, mean_M, yerr=std_M, color="b", marker="o", label="Magnetisierung")

    plt.xlabel("Temperatur in J/k")
    plt.ylabel("Magnetisierung")

    plt.title("Magnetisierung eines 8x8 Gitters")

    np.save("mean", mean_M)
    np.save("std", std_M)
    plt.show()
