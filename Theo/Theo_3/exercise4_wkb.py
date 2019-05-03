import numpy as np

a = 1
m = 1/2
k = 1.7480
h = 1

def E( n ):
    return 2*pow(
            a/(4*m**2) * ( np.pi * (n+0.5)*h/k)**4,
            1/3)

for n in range(10):
    print("E_{} = {:.3f}".format(n, E(n)))
