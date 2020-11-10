import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

############# PROGRAMMEINSTELLUNGEN #############

M = 10000
N = 100
a = 2
b = 2
c = 2

################################################


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def get_y(numbers):
    y = np.sum(numbers)

    return y


def generate_xs(N, algo):
    xs = []

    for n in range(N):
        xs.append(algo())

    return xs

def central_limit_theorem(algo, title, filename = "plot"):

    ys = []

    for m in tqdm(range(M)):
        y = get_y(generate_xs(N, algo))
        ys.append(y)

    mean = np.mean(ys)
    std = np.std(ys)
    x = np.linspace(mean - 5*std, mean + 5*std, N)

    filtered = np.array(ys)
    filtered = filtered[filtered > mean-0.5]
    filtered = filtered[filtered < mean + 0.49]

    plt.hist(ys, bins=int(N))

    plt.plot(x, len(filtered)*gaussian(x, mean, std),
             label=r"Gaussian with $\mu$ = {mu:.2f} and $\sigma$ = {sig:.2f}".format(mu = mean, sig = std),
             color="r", linewidth = 2)

    plt.title(title)
    plt.legend()
    plt.savefig(filename + ".pdf", bbox_inches="tight")
    plt.show()


def run():

    rng = np.random.default_rng()

    central_limit_theorem(lambda: rng.choice([-int(a), int(a)]), "X from discrete Distribution", "discrete")

    central_limit_theorem(lambda : rng.uniform(-b, b), "X from Uniform Distribution", "uniform")

    central_limit_theorem(lambda: rng.poisson(lam=c), "X from Poisson Distribution", "poisson")


if __name__ == "__main__":
    run()
