import numpy as np

a = 1
m = 1
k = 1.7480
h = 1

def E_wkb( n ):
    return pow(
            a/(4*m**2) * ( np.pi * (n+0.5)*h/k)**4,
            1/3)

def E_somm( n ):
    return pow(np.pi*h*n, 4/3) * pow(a/m**2, 1/3) *0.3

print("n\tE_n;wkb           \tE_n;somm")
for n in range(20):
    print("{0}\tE_{0};wkb = {1:2.3f}  \tE_{2};somm = {3:2.3f}".format(n, E_wkb(n), n, E_somm(n)))
